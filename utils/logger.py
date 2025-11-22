"""Logging utilities with JSONL support and performance optimizations."""
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from functools import lru_cache

class JSONLLogger:
    """Logger that writes structured logs in JSONL format."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"exhibition_{timestamp}.jsonl"
        
        # Setup standard logger
        self.logger = logging.getLogger("AIMuseumCurator")
        self.logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler(self.log_dir / f"standard_{timestamp}.log")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def log_event(self, event_type: str, data: Dict[str, Any]):
        """Log an event in JSONL format with buffering for better performance."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        
        # Use buffered writing for better I/O performance
        with open(self.log_file, "a", encoding="utf-8", buffering=8192) as f:
            f.write(json.dumps(log_entry, separators=(',', ':')) + "\n")
        
        # Only log to console if not in production mode
        if os.getenv('LOG_LEVEL', 'INFO') != 'ERROR':
            self.logger.info(f"{event_type}: {json.dumps(data, indent=2)}")
    
    def log_agent_start(self, agent_name: str, input_data: Any):
        """Log agent execution start."""
        self.log_event("agent_start", {
            "agent": agent_name,
            "input": str(input_data)[:500]  # Truncate long inputs
        })
    
    def log_agent_complete(self, agent_name: str, output_data: Any, duration: float):
        """Log agent execution completion."""
        self.log_event("agent_complete", {
            "agent": agent_name,
            "duration_seconds": duration,
            "output_preview": str(output_data)[:500]
        })
    
    def log_agent_error(self, agent_name: str, error: str):
        """Log agent execution error."""
        self.log_event("agent_error", {
            "agent": agent_name,
            "error": error
        })
        self.logger.error(f"Agent {agent_name} error: {error}")
    
    def log_metrics(self, metrics: Dict[str, float]):
        """Log evaluation metrics."""
        self.log_event("metrics", metrics)
    
    def log_exhibition_created(self, topic: str, exhibition_id: str):
        """Log successful exhibition creation."""
        self.log_event("exhibition_created", {
            "topic": topic,
            "exhibition_id": exhibition_id
        })

# Global logger instance
_logger_instance = None

def get_logger() -> JSONLLogger:
    """Get or create global logger instance."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = JSONLLogger()
    return _logger_instance
