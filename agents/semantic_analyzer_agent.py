"""Semantic Analyzer Agent - Advanced topic analysis and connections."""
from typing import Dict, List
from agents.base_agent import BaseAgent
import json

class SemanticAnalyzerAgent(BaseAgent):
    """Agent that performs deep semantic analysis of topics."""
    
    def __init__(self):
        super().__init__("SemanticAnalyzerAgent")
    
    def _process(self, input_data: Dict) -> Dict:
        """
        Perform semantic analysis to find connections and themes.
        
        Args:
            input_data: Topic and research data
            
        Returns:
            Semantic analysis with connections and insights
        """
        topic = input_data.get("topic", "")
        research_summary = input_data.get("research_summary", "")
        
        # Analyze semantic connections
        connections = self._analyze_connections(topic, research_summary)
        
        # Extract key concepts
        concepts = self._extract_concepts(topic, research_summary)
        
        # Generate thematic insights
        insights = self._generate_insights(topic, connections, concepts)
        
        return {
            "topic": topic,
            "connections": connections,
            "key_concepts": concepts,
            "thematic_insights": insights,
            "semantic_score": self._calculate_semantic_score(connections, concepts)
        }
    
    def _analyze_connections(self, topic: str, research: str) -> List[Dict]:
        """Analyze semantic connections within the topic."""
        # Simplified prompt to reduce API calls
        prompt = f"""List 3 key connections for {topic}:
1. Historical connection
2. Cultural connection  
3. Conceptual connection

Format: type|connection|significance (one per line)"""

        try:
            response = self.generate_with_gemini(prompt, temperature=0.7)
            
            # Parse simple format
            connections = []
            for line in response.split('\n'):
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        connections.append({
                            "type": parts[0].strip(),
                            "connection": parts[1].strip(),
                            "significance": parts[2].strip()
                        })
            
            if connections:
                return connections
        except:
            pass
        
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        return [
            {"type": "historical", "connection": f"Historical context of {topic}", "significance": "Provides background"},
            {"type": "cultural", "connection": f"Cultural impact of {topic}", "significance": "Shows influence"}
        ]
    
    def _extract_concepts(self, topic: str, research: str) -> List[str]:
        """Extract key concepts from the topic."""
        prompt = f"""Extract 8-10 key concepts from this topic: {topic}

Research:
{research[:500]}

List the most important concepts, themes, and ideas.
Format: One concept per line, no numbering."""

        response = self.generate_with_gemini(prompt, temperature=0.6)
        concepts = [c.strip() for c in response.split('\n') if c.strip() and len(c.strip()) > 3]
        return concepts[:10]
    
    def _generate_insights(self, topic: str, connections: List[Dict], concepts: List[str]) -> str:
        """Generate thematic insights."""
        connections_text = "\n".join([f"- {c.get('type')}: {c.get('connection')}" for c in connections[:3]])
        concepts_text = ", ".join(concepts[:5])
        
        prompt = f"""Generate 2-3 unique thematic insights about {topic}.

Connections:
{connections_text}

Key Concepts: {concepts_text}

Write insights that reveal deeper meaning and unexpected connections.
Make them thought-provoking and educational."""

        return self.generate_with_gemini(prompt, temperature=0.8)
    
    def _calculate_semantic_score(self, connections: List[Dict], concepts: List[str]) -> float:
        """Calculate semantic richness score."""
        connection_score = min(1.0, len(connections) / 5.0)
        concept_score = min(1.0, len(concepts) / 8.0)
        return (connection_score + concept_score) / 2
