"""Exhibit Generator Agent - creates individual exhibits."""
from typing import Dict, List
from agents.base_agent import BaseAgent
import json

class ExhibitGeneratorAgent(BaseAgent):
    """Agent that generates individual museum exhibits."""
    
    def __init__(self):
        super().__init__("ExhibitGeneratorAgent")
    
    def _process(self, input_data: Dict) -> List[Dict]:
        """
        Generate exhibits based on research data.
        
        Args:
            input_data: Research data and topic information
            
        Returns:
            List of exhibit dictionaries
        """
        topic = input_data.get("topic", "")
        research_summary = input_data.get("research_summary", "")
        facts = input_data.get("facts", [])
        
        # Generate exhibits using Gemini
        exhibits = self._generate_exhibits(topic, research_summary, facts)
        
        return exhibits
    
    def _generate_exhibits(self, topic: str, research_summary: str, facts: List[str]) -> List[Dict]:
        """Generate multiple exhibits for the topic."""
        facts_text = "\n".join([f"- {fact}" for fact in facts[:20]])
        
        prompt = f"""Create exactly 8 museum exhibits for an exhibition about: {topic}

Research Summary:
{research_summary}

Key Facts:
{facts_text}

For each exhibit, provide:
1. Name (engaging title)
2. Description (2-3 paragraphs, educational and engaging)
3. Time Period (specific dates or era)
4. Cultural Significance (why it matters)
5. Interesting Facts (3-5 bullet points)
6. Visual References (describe 2-3 images/artifacts that would accompany this exhibit)

Format as JSON array with this structure:
[
  {{
    "name": "Exhibit Name",
    "description": "Detailed description...",
    "time_period": "1400-1500 CE",
    "cultural_significance": "Why this matters...",
    "facts": ["Fact 1", "Fact 2", "Fact 3"],
    "visual_refs": ["Description of image 1", "Description of artifact 2"],
    "tags": ["tag1", "tag2"]
  }}
]

Provide ONLY the JSON array, no other text.

IMPORTANT: Generate exactly 8 exhibits with rich, detailed content."""

        response = self.generate_with_gemini(prompt, temperature=0.85)
        
        # Parse JSON response
        try:
            # Extract JSON from response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                exhibits = json.loads(json_str)
                return exhibits
            else:
                # Fallback: create basic exhibits
                return self._create_fallback_exhibits(topic)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return self._create_fallback_exhibits(topic)
    
    def _create_fallback_exhibits(self, topic: str) -> List[Dict]:
        """Create basic exhibits if JSON parsing fails."""
        return [
            {
                "name": f"{topic} - Origins",
                "description": f"Explore the origins and early history of {topic}.",
                "time_period": "Historical Period",
                "cultural_significance": f"Understanding the roots of {topic}.",
                "facts": [f"Key fact about {topic}"],
                "visual_refs": ["Historical artifact", "Period illustration"],
                "tags": ["origins", "history"]
            },
            {
                "name": f"{topic} - Development",
                "description": f"The evolution and development of {topic} over time.",
                "time_period": "Middle Period",
                "cultural_significance": f"How {topic} evolved and changed.",
                "facts": [f"Development fact about {topic}"],
                "visual_refs": ["Development artifact"],
                "tags": ["development", "evolution"]
            },
            {
                "name": f"{topic} - Legacy",
                "description": f"The lasting impact and legacy of {topic}.",
                "time_period": "Modern Era",
                "cultural_significance": f"The continuing influence of {topic}.",
                "facts": [f"Legacy fact about {topic}"],
                "visual_refs": ["Modern representation"],
                "tags": ["legacy", "impact"]
            }
        ]
