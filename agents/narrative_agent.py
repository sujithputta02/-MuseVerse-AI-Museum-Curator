"""Narrative Agent - creates curator notes and storylines."""
from typing import Dict
from agents.base_agent import BaseAgent

class NarrativeAgent(BaseAgent):
    """Agent that creates narrative content and curator notes."""
    
    def __init__(self):
        super().__init__("NarrativeAgent")
    
    def _process(self, input_data: Dict) -> Dict:
        """
        Create narrative content for the exhibition.
        
        Args:
            input_data: Exhibition structure
            
        Returns:
            Exhibition with added narrative content
        """
        exhibition = input_data.copy()
        
        # Generate curator notes
        curator_notes = self._generate_curator_notes(exhibition)
        exhibition["curator_notes"] = curator_notes
        
        # Add room narratives
        for room in exhibition.get("rooms", []):
            room["narrative"] = self._generate_room_narrative(room, exhibition["topic"])
        
        return exhibition
    
    def _generate_curator_notes(self, exhibition: Dict) -> str:
        """Generate curator's introduction and notes."""
        topic = exhibition.get("topic", "")
        overview = exhibition.get("overview", "")
        rooms = exhibition.get("rooms", [])
        room_titles = [r.get("title", "") for r in rooms]
        
        prompt = f"""Write curator's notes for a museum exhibition about: {topic}

Overview: {overview}

Exhibition Rooms: {', '.join(room_titles)}

Write a 4-paragraph curator's introduction that:
1. Welcomes visitors and introduces the topic
2. Explains why this exhibition matters today
3. Highlights what visitors will discover
4. Provides context for understanding the exhibits

Tone: Educational, welcoming, engaging. Avoid jargon.

Write in a warm, accessible style that makes visitors excited to explore."""

        return self.generate_with_gemini(prompt, temperature=0.85)
    
    def _generate_room_narrative(self, room: Dict, topic: str) -> str:
        """Generate narrative for a specific room."""
        room_title = room.get("title", "")
        theme = room.get("theme", "")
        exhibits = room.get("exhibits", [])
        exhibit_names = [e.get("name", "") for e in exhibits[:5]]
        
        prompt = f"""Write a brief narrative introduction for this museum room:

Room: {room_title}
Theme: {theme}
Exhibition Topic: {topic}
Key Exhibits: {', '.join(exhibit_names)}

Write 2-3 sentences that:
- Set the scene for visitors entering this room
- Connect the exhibits to the overall theme
- Create anticipation for what they'll discover

Tone: Engaging, educational, inviting."""

        return self.generate_with_gemini(prompt, temperature=0.7)
