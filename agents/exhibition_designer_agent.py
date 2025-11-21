"""Exhibition Designer Agent - organizes exhibits into rooms."""
from typing import Dict, List
from agents.base_agent import BaseAgent
import config

class ExhibitionDesignerAgent(BaseAgent):
    """Agent that designs exhibition layout and room structure."""
    
    def __init__(self):
        super().__init__("ExhibitionDesignerAgent")
    
    def _process(self, input_data: Dict) -> Dict:
        """
        Design exhibition structure with themed rooms.
        
        Args:
            input_data: Topic data and exhibits
            
        Returns:
            Exhibition structure with rooms
        """
        topic = input_data.get("topic", "")
        exhibits = input_data.get("exhibits", [])
        topic_data = input_data.get("topic_data", {})
        
        # Design room structure
        rooms = self._design_rooms(topic, exhibits, topic_data)
        
        return {
            "topic": topic,
            "title": topic_data.get("title", topic),
            "overview": topic_data.get("overview", ""),
            "rooms": rooms
        }
    
    def _design_rooms(self, topic: str, exhibits: List[Dict], topic_data: Dict) -> List[Dict]:
        """Design themed rooms and assign exhibits."""
        # Optimize room count based on exhibits
        num_rooms = 4 if len(exhibits) >= 8 else 3
        
        prompt = f"""Design {num_rooms} themed rooms for a museum exhibition about: {topic}

Available exhibits: {len(exhibits)}

For each room, provide:
1. Room Title (engaging, thematic)
2. Theme (what aspect of the topic)
3. Description (2-3 sentences about what visitors will experience)

Format as:
ROOM 1: [Title]
THEME: [Theme]
DESCRIPTION: [Description]

ROOM 2: [Title]
...
"""

        response = self.generate_with_gemini(prompt, temperature=0.7)
        
        # Parse rooms
        rooms = self._parse_rooms(response)
        
        # Assign exhibits to rooms
        exhibits_per_room = len(exhibits) // len(rooms)
        for i, room in enumerate(rooms):
            start_idx = i * exhibits_per_room
            end_idx = start_idx + exhibits_per_room if i < len(rooms) - 1 else len(exhibits)
            room["exhibits"] = exhibits[start_idx:end_idx]
        
        return rooms
    
    def _parse_rooms(self, response: str) -> List[Dict]:
        """Parse room information from response."""
        rooms = []
        current_room = {}
        
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('ROOM'):
                if current_room:
                    rooms.append(current_room)
                title = line.split(':', 1)[1].strip() if ':' in line else f"Room {len(rooms) + 1}"
                current_room = {"title": title, "theme": "", "description": "", "exhibits": []}
            elif line.startswith('THEME:'):
                current_room["theme"] = line.replace('THEME:', '').strip()
            elif line.startswith('DESCRIPTION:'):
                current_room["description"] = line.replace('DESCRIPTION:', '').strip()
        
        if current_room:
            rooms.append(current_room)
        
        # Ensure we have at least 3 rooms
        while len(rooms) < 3:
            rooms.append({
                "title": f"Exhibition Room {len(rooms) + 1}",
                "theme": "General Exhibition",
                "description": "Additional exhibition space.",
                "exhibits": []
            })
        
        return rooms
