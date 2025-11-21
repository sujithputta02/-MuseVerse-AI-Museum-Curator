"""Interactive Guide Agent - Creates interactive elements and questions."""
from typing import Dict, List
from agents.base_agent import BaseAgent
import json

class InteractiveGuideAgent(BaseAgent):
    """Agent that creates interactive educational elements."""
    
    def __init__(self):
        super().__init__("InteractiveGuideAgent")
    
    def _process(self, input_data: Dict) -> Dict:
        """
        Create interactive elements for the exhibition.
        
        Args:
            input_data: Exhibition data
            
        Returns:
            Exhibition with interactive elements
        """
        exhibition = input_data.copy()
        
        # Add interactive questions for each room
        for room in exhibition.get("rooms", []):
            room["interactive_questions"] = self._generate_questions(room)
            room["discussion_prompts"] = self._generate_discussion_prompts(room)
        
        # Add overall quiz
        exhibition["quiz"] = self._generate_quiz(exhibition)
        
        # Add exploration challenges
        exhibition["challenges"] = self._generate_challenges(exhibition)
        
        return exhibition
    
    def _generate_questions(self, room: Dict) -> List[Dict]:
        """Generate interactive questions for a room."""
        room_title = room.get("title", "")
        theme = room.get("theme", "")
        
        # Use simpler format to reduce API load
        prompt = f"""Create 2 questions about: {room_title} ({theme})
Format: Q|purpose|hint (one per line)"""

        try:
            response = self.generate_with_gemini(prompt, temperature=0.8)
            
            questions = []
            for line in response.split('\n'):
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        questions.append({
                            "question": parts[0].strip(),
                            "purpose": parts[1].strip(),
                            "hint": parts[2].strip()
                        })
            
            if questions:
                return questions
        except:
            pass
        
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        return [
            {"question": f"What surprises you most about {room_title}?", "purpose": "Personal reflection", "hint": "Think about your expectations"}
        ]
    
    def _generate_discussion_prompts(self, room: Dict) -> List[str]:
        """Generate discussion prompts."""
        room_title = room.get("title", "")
        
        prompts = [
            f"How does {room_title} connect to modern life?",
            f"What questions would you ask someone from this period?",
            f"What can we learn from {room_title} today?"
        ]
        
        return prompts[:2]
    
    def _generate_quiz(self, exhibition: Dict) -> Dict:
        """Generate an interactive quiz."""
        topic = exhibition.get("topic", "")
        
        prompt = f"""Create a 5-question multiple choice quiz about {topic}.

Questions should be:
- Educational but fun
- Mix of difficulty levels
- Based on exhibition content
- Have clear correct answers

Format as JSON:
{{
  "title": "Quiz title",
  "questions": [
    {{
      "question": "Question text",
      "options": ["A", "B", "C", "D"],
      "correct": 0,
      "explanation": "Why this is correct"
    }}
  ]
}}

Provide ONLY the JSON."""

        response = self.generate_with_gemini(prompt, temperature=0.7)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        return {
            "title": f"Test Your Knowledge: {topic}",
            "questions": []
        }
    
    def _generate_challenges(self, exhibition: Dict) -> List[Dict]:
        """Generate exploration challenges."""
        return [
            {
                "title": "Timeline Detective",
                "description": "Find the oldest and newest items in the exhibition",
                "reward": "Discover how this topic evolved over time"
            },
            {
                "title": "Connection Finder",
                "description": "Identify 3 connections between different rooms",
                "reward": "See the bigger picture of how ideas relate"
            },
            {
                "title": "Modern Relevance",
                "description": "Find 3 ways this topic impacts your life today",
                "reward": "Understand why history matters now"
            }
        ]
