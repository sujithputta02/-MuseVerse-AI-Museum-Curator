"""Loop Agent - refines exhibitions based on evaluation."""
from typing import Dict
from agents.base_agent import BaseAgent
import config

class LoopAgent(BaseAgent):
    """Agent that refines exhibitions based on evaluation feedback."""
    
    def __init__(self):
        super().__init__("LoopAgent")
    
    def _process(self, input_data: Dict) -> Dict:
        """
        Refine exhibition based on evaluation.
        
        Args:
            input_data: Exhibition and evaluation report
            
        Returns:
            Refined exhibition or original if quality sufficient
        """
        exhibition = input_data.get("exhibition", {})
        evaluation = input_data.get("evaluation", {})
        
        # Check if refinement needed
        if evaluation.get("overall_score", 0) >= config.MIN_QUALITY_SCORE:
            return {
                "exhibition": exhibition,
                "refined": False,
                "reason": "Quality threshold met"
            }
        
        # Refine based on recommendations
        recommendations = evaluation.get("recommendations", [])
        refined_exhibition = self._refine_exhibition(exhibition, recommendations, evaluation)
        
        return {
            "exhibition": refined_exhibition,
            "refined": True,
            "improvements": recommendations
        }
    
    def _refine_exhibition(self, exhibition: Dict, recommendations: List[str], evaluation: Dict) -> Dict:
        """Refine exhibition based on recommendations."""
        refined = exhibition.copy()
        
        # Enhance curator notes if narrative quality low
        if evaluation.get("narrative_quality", 1.0) < 0.7:
            refined["curator_notes"] = self._enhance_curator_notes(
                exhibition.get("curator_notes", ""),
                exhibition.get("topic", "")
            )
        
        # Add more exhibits if needed
        if evaluation.get("validation", {}).get("total_exhibits", 0) < 5:
            self._add_exhibits(refined)
        
        return refined
    
    def _enhance_curator_notes(self, current_notes: str, topic: str) -> str:
        """Enhance curator notes with more detail."""
        prompt = f"""Enhance these curator notes for a museum exhibition about {topic}.

Current notes:
{current_notes}

Add more detail, context, and engagement while maintaining educational tone.
Target: 250-300 words."""

        return self.generate_with_gemini(prompt, temperature=0.7)
    
    def _add_exhibits(self, exhibition: Dict):
        """Add additional exhibits to rooms with few exhibits."""
        topic = exhibition.get("topic", "")
        
        for room in exhibition.get("rooms", []):
            if len(room.get("exhibits", [])) < 2:
                # Generate additional exhibit
                new_exhibit = self._generate_additional_exhibit(topic, room.get("title", ""))
                room["exhibits"].append(new_exhibit)
    
    def _generate_additional_exhibit(self, topic: str, room_title: str) -> Dict:
        """Generate an additional exhibit."""
        return {
            "name": f"Additional Exhibit: {room_title}",
            "description": f"Supplementary exhibit exploring aspects of {topic} related to {room_title}.",
            "time_period": "Historical Period",
            "cultural_significance": f"Provides additional context for understanding {topic}.",
            "facts": [f"Additional information about {topic}"],
            "visual_refs": ["Supplementary visual reference"],
            "tags": ["supplementary"]
        }
