"""Multimedia Curator Agent - Suggests rich media and interactive elements."""
from typing import Dict, List
from agents.base_agent import BaseAgent

class MultimediaCuratorAgent(BaseAgent):
    """Agent that curates multimedia recommendations."""
    
    def __init__(self):
        super().__init__("MultimediaCuratorAgent")
    
    def _process(self, input_data: Dict) -> Dict:
        """
        Add multimedia recommendations to exhibition.
        
        Args:
            input_data: Exhibition data
            
        Returns:
            Exhibition with multimedia elements
        """
        exhibition = input_data.copy()
        
        # Add multimedia for each exhibit
        for room in exhibition.get("rooms", []):
            for exhibit in room.get("exhibits", []):
                exhibit["multimedia"] = self._suggest_multimedia(exhibit)
                exhibit["sensory_elements"] = self._suggest_sensory(exhibit)
        
        # Add overall multimedia experience
        exhibition["virtual_tour"] = self._create_virtual_tour_guide(exhibition)
        exhibition["audio_guide"] = self._create_audio_guide(exhibition)
        
        return exhibition
    
    def _suggest_multimedia(self, exhibit: Dict) -> Dict:
        """Suggest multimedia elements for an exhibit."""
        name = exhibit.get("name", "")
        description = exhibit.get("description", "")[:200]
        
        return {
            "3d_model": f"Interactive 3D model of {name}",
            "video": f"Short documentary clip about {name}",
            "audio": f"Ambient sounds from the period of {name}",
            "ar_experience": f"Augmented reality overlay showing {name} in context",
            "interactive_map": f"Geographic visualization of {name}'s influence",
            "comparison_slider": f"Before/after or then/now comparison for {name}"
        }
    
    def _suggest_sensory(self, exhibit: Dict) -> Dict:
        """Suggest sensory elements."""
        return {
            "visual": "High-resolution images and detailed close-ups",
            "audio": "Period-appropriate music or ambient sounds",
            "tactile": "Replica objects visitors can touch",
            "spatial": "Room layout that guides natural flow"
        }
    
    def _create_virtual_tour_guide(self, exhibition: Dict) -> Dict:
        """Create virtual tour guide structure."""
        topic = exhibition.get("topic", "")
        rooms = exhibition.get("rooms", [])
        
        return {
            "introduction": f"Welcome to the {topic} exhibition. Let me guide you through this journey.",
            "room_transitions": [
                f"As we move to {room.get('title')}, notice how the theme evolves..."
                for room in rooms
            ],
            "highlights": "Don't miss these key exhibits...",
            "conclusion": "Thank you for exploring this exhibition with me."
        }
    
    def _create_audio_guide(self, exhibition: Dict) -> List[Dict]:
        """Create audio guide script."""
        audio_stops = []
        
        for i, room in enumerate(exhibition.get("rooms", []), 1):
            audio_stops.append({
                "stop_number": i,
                "location": room.get("title"),
                "duration": "3-5 minutes",
                "script_preview": f"In this room, we explore {room.get('theme')}...",
                "language_options": ["English", "Spanish", "French", "Mandarin"]
            })
        
        return audio_stops
