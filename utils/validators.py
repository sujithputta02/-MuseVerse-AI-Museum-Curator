"""Input validation utilities for the AI Museum Curator."""
import re
from typing import Dict, List, Optional, Tuple

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class InputValidator:
    """Validates user inputs and API responses."""
    
    # Topic validation rules
    MIN_TOPIC_LENGTH = 3
    MAX_TOPIC_LENGTH = 200
    FORBIDDEN_PATTERNS = [
        r'<script',
        r'javascript:',
        r'onerror=',
        r'onclick=',
    ]
    
    @staticmethod
    def validate_topic(topic: str) -> Tuple[bool, Optional[str]]:
        """
        Validate exhibition topic input.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not topic or not isinstance(topic, str):
            return False, "Topic must be a non-empty string"
        
        topic = topic.strip()
        
        # Length validation
        if len(topic) < InputValidator.MIN_TOPIC_LENGTH:
            return False, f"Topic must be at least {InputValidator.MIN_TOPIC_LENGTH} characters"
        
        if len(topic) > InputValidator.MAX_TOPIC_LENGTH:
            return False, f"Topic must not exceed {InputValidator.MAX_TOPIC_LENGTH} characters"
        
        # Security validation - check for malicious patterns
        for pattern in InputValidator.FORBIDDEN_PATTERNS:
            if re.search(pattern, topic, re.IGNORECASE):
                return False, "Topic contains forbidden content"
        
        # Check for reasonable content (at least one letter)
        if not re.search(r'[a-zA-Z]', topic):
            return False, "Topic must contain at least one letter"
        
        return True, None
    
    @staticmethod
    def validate_api_key(api_key: str) -> Tuple[bool, Optional[str]]:
        """
        Validate Google API key format.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not api_key or not isinstance(api_key, str):
            return False, "API key must be a non-empty string"
        
        api_key = api_key.strip()
        
        # Basic format validation for Google API keys
        if not api_key.startswith('AIza'):
            return False, "Invalid API key format (should start with 'AIza')"
        
        if len(api_key) < 30:
            return False, "API key appears to be too short"
        
        # Check for valid characters (alphanumeric, dash, underscore)
        if not re.match(r'^[A-Za-z0-9_-]+$', api_key):
            return False, "API key contains invalid characters"
        
        return True, None
    
    @staticmethod
    def validate_exhibition_data(exhibition: Dict) -> Tuple[bool, List[str]]:
        """
        Validate exhibition data structure.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Required fields
        required_fields = ['topic', 'title', 'overview', 'rooms']
        for field in required_fields:
            if field not in exhibition:
                errors.append(f"Missing required field: {field}")
        
        # Validate rooms
        if 'rooms' in exhibition:
            if not isinstance(exhibition['rooms'], list):
                errors.append("Rooms must be a list")
            elif len(exhibition['rooms']) == 0:
                errors.append("Exhibition must have at least one room")
            else:
                for i, room in enumerate(exhibition['rooms']):
                    if not isinstance(room, dict):
                        errors.append(f"Room {i} must be a dictionary")
                        continue
                    
                    # Validate room structure
                    if 'exhibits' not in room:
                        errors.append(f"Room {i} missing exhibits")
                    elif not isinstance(room['exhibits'], list):
                        errors.append(f"Room {i} exhibits must be a list")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize text input by removing potentially harmful content.
        
        Args:
            text: Input text to sanitize
            max_length: Optional maximum length to truncate to
        
        Returns:
            Sanitized text
        """
        if not isinstance(text, str):
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove control characters except newlines and tabs
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        # Truncate if needed
        if max_length and len(text) > max_length:
            text = text[:max_length] + "..."
        
        return text.strip()
    
    @staticmethod
    def validate_file_path(file_path: str, allowed_extensions: Optional[List[str]] = None) -> Tuple[bool, Optional[str]]:
        """
        Validate file path for security.
        
        Args:
            file_path: Path to validate
            allowed_extensions: List of allowed file extensions (e.g., ['.json', '.pdf'])
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not file_path or not isinstance(file_path, str):
            return False, "File path must be a non-empty string"
        
        # Check for path traversal attempts
        if '..' in file_path or file_path.startswith('/'):
            return False, "Invalid file path (potential security risk)"
        
        # Validate extension if specified
        if allowed_extensions:
            if not any(file_path.lower().endswith(ext) for ext in allowed_extensions):
                return False, f"File must have one of these extensions: {', '.join(allowed_extensions)}"
        
        return True, None

# Convenience functions
def validate_topic(topic: str) -> None:
    """Validate topic and raise ValidationError if invalid."""
    is_valid, error = InputValidator.validate_topic(topic)
    if not is_valid:
        raise ValidationError(error)

def validate_api_key(api_key: str) -> None:
    """Validate API key and raise ValidationError if invalid."""
    is_valid, error = InputValidator.validate_api_key(api_key)
    if not is_valid:
        raise ValidationError(error)

def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize text input."""
    return InputValidator.sanitize_text(text, max_length)
