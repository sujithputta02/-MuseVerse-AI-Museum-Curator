"""Base agent class with common functionality."""
import time
from typing import Any, Dict
from utils.logger import get_logger
import google.generativeai as genai
import config

class BaseAgent:
    """Base class for all agents."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger()
        
        # Configure Gemini
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(config.MODEL_NAME)
        
        self.execution_count = 0
        self.success_count = 0
        self.total_duration = 0.0
    
    def execute(self, input_data: Any) -> Any:
        """Execute agent logic with logging and error handling."""
        self.execution_count += 1
        start_time = time.time()
        
        self.logger.log_agent_start(self.name, input_data)
        
        try:
            result = self._process(input_data)
            duration = time.time() - start_time
            self.total_duration += duration
            self.success_count += 1
            
            self.logger.log_agent_complete(self.name, result, duration)
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            self.total_duration += duration
            self.logger.log_agent_error(self.name, str(e))
            raise
    
    def _process(self, input_data: Any) -> Any:
        """Override this method in subclasses."""
        raise NotImplementedError("Subclasses must implement _process method")
    
    def get_success_rate(self) -> float:
        """Calculate agent success rate."""
        if self.execution_count == 0:
            return 0.0
        return self.success_count / self.execution_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent execution statistics."""
        return {
            "name": self.name,
            "executions": self.execution_count,
            "successes": self.success_count,
            "success_rate": self.get_success_rate(),
            "total_duration": self.total_duration,
            "avg_duration": self.total_duration / self.execution_count if self.execution_count > 0 else 0
        }
    
    def generate_with_gemini(self, prompt: str, temperature: float = None) -> str:
        """Generate text using Gemini model with retry logic and rate limiting."""
        import time
        
        temp = temperature if temperature is not None else config.TEMPERATURE
        
        generation_config = genai.types.GenerationConfig(
            temperature=temp,
            max_output_tokens=config.MAX_TOKENS,
            top_p=0.95,
            top_k=40
        )
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Add delay to respect rate limits
                if hasattr(config, 'REQUEST_DELAY'):
                    time.sleep(config.REQUEST_DELAY)
                
                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                
                return response.text
            except Exception as e:
                error_str = str(e)
                
                # Handle rate limit errors
                if "429" in error_str or "quota" in error_str.lower():
                    wait_time = 10 * (attempt + 1)  # Exponential backoff
                    self.logger.logger.warning(f"Rate limit hit, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                elif attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                else:
                    raise
        
        return ""
