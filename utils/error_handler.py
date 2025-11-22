"""Centralized error handling for the AI Museum Curator."""
import traceback
from typing import Optional, Dict, Any
from functools import wraps
import logging

logger = logging.getLogger("AIMuseumCurator")

class MuseumCuratorError(Exception):
    """Base exception for Museum Curator errors."""
    pass

class APIError(MuseumCuratorError):
    """Error related to API calls."""
    pass

class AgentError(MuseumCuratorError):
    """Error related to agent execution."""
    pass

class ValidationError(MuseumCuratorError):
    """Error related to input validation."""
    pass

class ErrorHandler:
    """Centralized error handling and recovery."""
    
    @staticmethod
    def handle_api_error(error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Handle API-related errors with appropriate recovery.
        
        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
        
        Returns:
            Dictionary with error information and recovery suggestions
        """
        error_info = {
            'error_type': 'API Error',
            'message': str(error),
            'context': context,
            'recoverable': True,
            'suggestions': []
        }
        
        error_msg = str(error).lower()
        
        # Rate limiting
        if 'rate limit' in error_msg or '429' in error_msg:
            error_info['suggestions'] = [
                'Wait a few moments before retrying',
                'Consider reducing request frequency',
                'Check your API quota limits'
            ]
        
        # Authentication errors
        elif 'api key' in error_msg or '401' in error_msg or '403' in error_msg:
            error_info['suggestions'] = [
                'Verify your API key is correct',
                'Check if API key has necessary permissions',
                'Ensure API key is not expired'
            ]
            error_info['recoverable'] = False
        
        # Network errors
        elif 'connection' in error_msg or 'timeout' in error_msg:
            error_info['suggestions'] = [
                'Check your internet connection',
                'Retry the operation',
                'Check if the API service is available'
            ]
        
        # Quota exceeded
        elif 'quota' in error_msg or 'limit exceeded' in error_msg:
            error_info['suggestions'] = [
                'Wait until quota resets',
                'Upgrade your API plan if needed',
                'Optimize requests to use fewer API calls'
            ]
            error_info['recoverable'] = False
        
        else:
            error_info['suggestions'] = [
                'Check the error message for details',
                'Retry the operation',
                'Contact support if the issue persists'
            ]
        
        logger.error(f"API Error in {context}: {error}")
        return error_info
    
    @staticmethod
    def handle_agent_error(error: Exception, agent_name: str) -> Dict[str, Any]:
        """
        Handle agent execution errors.
        
        Args:
            error: The exception that occurred
            agent_name: Name of the agent that failed
        
        Returns:
            Dictionary with error information
        """
        error_info = {
            'error_type': 'Agent Error',
            'agent': agent_name,
            'message': str(error),
            'recoverable': True,
            'suggestions': [
                f'The {agent_name} encountered an issue',
                'The system will attempt to continue with available data',
                'Some features may be limited'
            ]
        }
        
        logger.error(f"Agent Error ({agent_name}): {error}")
        logger.debug(traceback.format_exc())
        
        return error_info
    
    @staticmethod
    def safe_execute(func, *args, default=None, error_handler=None, **kwargs):
        """
        Safely execute a function with error handling.
        
        Args:
            func: Function to execute
            *args: Positional arguments for the function
            default: Default value to return on error
            error_handler: Optional custom error handler function
            **kwargs: Keyword arguments for the function
        
        Returns:
            Function result or default value on error
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if error_handler:
                error_handler(e)
            else:
                logger.error(f"Error in {func.__name__}: {e}")
            return default

def retry_on_error(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator to retry function on error.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying...")
                        time.sleep(delay * (attempt + 1))  # Exponential backoff
                    else:
                        logger.error(f"All {max_retries} attempts failed for {func.__name__}")
            
            raise last_error
        
        return wrapper
    return decorator

def log_errors(func):
    """Decorator to log errors with full traceback."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            logger.debug(traceback.format_exc())
            raise
    
    return wrapper
