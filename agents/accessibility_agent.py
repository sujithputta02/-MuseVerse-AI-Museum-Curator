"""Accessibility Agent - Ensures inclusive exhibition design."""
from typing import Dict, List
from agents.base_agent import BaseAgent

class AccessibilityAgent(BaseAgent):
    """Agent that adds accessibility features."""
    
    def __init__(self):
        super().__init__("AccessibilityAgent")
    
    def _process(self, input_data: Dict) -> Dict:
        """
        Add accessibility features to exhibition.
        
        Args:
            input_data: Exhibition data
            
        Returns:
            Exhibition with accessibility enhancements
        """
        exhibition = input_data.copy()
        
        # Add accessibility metadata
        exhibition["accessibility"] = {
            "visual": self._add_visual_accessibility(exhibition),
            "auditory": self._add_auditory_accessibility(exhibition),
            "cognitive": self._add_cognitive_accessibility(exhibition),
            "physical": self._add_physical_accessibility(exhibition),
            "language": self._add_language_accessibility(exhibition)
        }
        
        # Add alternative formats
        for room in exhibition.get("rooms", []):
            room["alt_formats"] = self._create_alternative_formats(room)
        
        return exhibition
    
    def _add_visual_accessibility(self, exhibition: Dict) -> Dict:
        """Add visual accessibility features."""
        return {
            "screen_reader_compatible": True,
            "high_contrast_mode": "Available",
            "text_descriptions": "Detailed alt text for all images",
            "large_print_option": "Available for all text",
            "audio_descriptions": "Available for visual exhibits",
            "tactile_graphics": "3D printed models available"
        }
    
    def _add_auditory_accessibility(self, exhibition: Dict) -> Dict:
        """Add auditory accessibility features."""
        return {
            "captions": "All audio/video content captioned",
            "transcripts": "Full transcripts available",
            "sign_language": "ASL interpretation videos",
            "visual_alerts": "Visual cues for audio content"
        }
    
    def _add_cognitive_accessibility(self, exhibition: Dict) -> Dict:
        """Add cognitive accessibility features."""
        return {
            "simplified_text": "Plain language summaries available",
            "clear_navigation": "Intuitive room flow and signage",
            "rest_areas": "Quiet spaces for breaks",
            "sensory_friendly": "Low-stimulation options available",
            "time_flexibility": "Self-paced exploration encouraged"
        }
    
    def _add_physical_accessibility(self, exhibition: Dict) -> Dict:
        """Add physical accessibility features."""
        return {
            "wheelchair_accessible": "All areas accessible",
            "seating": "Benches in every room",
            "exhibit_height": "Adjustable viewing heights",
            "wide_pathways": "Easy navigation for mobility devices"
        }
    
    def _add_language_accessibility(self, exhibition: Dict) -> Dict:
        """Add language accessibility features."""
        return {
            "languages": ["English", "Spanish", "French", "Mandarin", "Arabic", "Hindi"],
            "translation_quality": "Professional translations",
            "cultural_adaptation": "Culturally appropriate content",
            "reading_level": "Multiple reading levels available"
        }
    
    def _create_alternative_formats(self, room: Dict) -> Dict:
        """Create alternative format options."""
        return {
            "audio_tour": "Available in 6 languages",
            "braille_guide": "Braille descriptions available",
            "large_print": "Large print guide available",
            "digital_guide": "Mobile app with customization",
            "simplified_guide": "Easy-read version available"
        }
