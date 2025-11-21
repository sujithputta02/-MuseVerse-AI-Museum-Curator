"""Topic Intake Agent - validates and enriches user topics."""
from typing import Dict
from agents.base_agent import BaseAgent

class TopicIntakeAgent(BaseAgent):
    """Agent that processes and validates exhibition topics."""
    
    def __init__(self):
        super().__init__("TopicIntakeAgent")
    
    def _process(self, input_data: str) -> Dict[str, any]:
        """
        Process topic input and generate structured topic data.
        
        Args:
            input_data: Raw topic string from user
            
        Returns:
            Structured topic data with enriched information
        """
        topic = input_data.strip()
        
        # Generate enriched topic information using Gemini
        prompt = f"""You are a museum curator analyzing a topic for an exhibition.

Topic: {topic}

Provide a structured analysis in the following format:

TITLE: [Create an engaging exhibition title]
CATEGORY: [Historical/Cultural/Scientific/Artistic]
TIME_PERIOD: [Approximate time period or era]
REGIONS: [Geographic regions involved]
KEY_THEMES: [3-5 key themes to explore]
OVERVIEW: [2-3 sentence overview of the topic]
SUGGESTED_ROOMS: [3-5 thematic room titles]

Be specific, educational, and engaging."""

        response = self.generate_with_gemini(prompt, temperature=0.7)
        
        # Parse response
        result = {
            "original_topic": topic,
            "enriched_data": response,
            "status": "validated"
        }
        
        # Extract structured data
        lines = response.split('\n')
        for line in lines:
            if line.startswith('TITLE:'):
                result['title'] = line.replace('TITLE:', '').strip()
            elif line.startswith('CATEGORY:'):
                result['category'] = line.replace('CATEGORY:', '').strip()
            elif line.startswith('TIME_PERIOD:'):
                result['time_period'] = line.replace('TIME_PERIOD:', '').strip()
            elif line.startswith('OVERVIEW:'):
                result['overview'] = line.replace('OVERVIEW:', '').strip()
        
        return result
