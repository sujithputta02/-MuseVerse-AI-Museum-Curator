"""Research Agent - conducts research using search tools."""
from typing import Dict, List
from agents.base_agent import BaseAgent
from tools.search_tool import GoogleSearchTool
from tools.fact_checker import FactConsistencyChecker
import config

class ResearchAgent(BaseAgent):
    """Agent that researches topics using search tools."""
    
    def __init__(self):
        super().__init__("ResearchAgent")
        self.search_tool = GoogleSearchTool(config.GOOGLE_API_KEY)
        self.fact_checker = FactConsistencyChecker()
    
    def _process(self, input_data: Dict) -> Dict[str, any]:
        """
        Research the topic and extract key information.
        
        Args:
            input_data: Topic data from TopicIntakeAgent
            
        Returns:
            Research results with facts and sources
        """
        topic = input_data.get("original_topic", "")
        
        # Generate research queries
        queries = self._generate_research_queries(topic)
        
        # Conduct searches
        all_results = []
        for query in queries[:3]:  # Limit to 3 queries
            results = self.search_tool.search(query, num_results=3)
            all_results.extend(results)
        
        # Extract facts
        facts = self.search_tool.extract_facts(all_results)
        
        # Use Gemini to synthesize research
        research_summary = self._synthesize_research(topic, facts)
        
        # Check fact consistency
        consistency_report = self.fact_checker.check_consistency(facts)
        
        return {
            "topic": topic,
            "search_queries": queries,
            "search_results": all_results,
            "facts": facts,
            "research_summary": research_summary,
            "consistency_report": consistency_report,
            "quality_score": consistency_report.get("quality_score", 0.0)
        }
    
    def _generate_research_queries(self, topic: str) -> List[str]:
        """Generate search queries for the topic."""
        prompt = f"""Generate 5 specific search queries to research this museum exhibition topic: {topic}

Queries should cover:
1. Historical background
2. Cultural significance
3. Key figures or artifacts
4. Timeline and events
5. Modern relevance

Format: One query per line, no numbering."""

        response = self.generate_with_gemini(prompt, temperature=0.5)
        queries = [q.strip() for q in response.split('\n') if q.strip()]
        return queries[:5]
    
    def _synthesize_research(self, topic: str, facts: List[str]) -> str:
        """Synthesize research findings into coherent summary."""
        facts_text = "\n".join([f"- {fact}" for fact in facts[:10]])
        
        prompt = f"""Synthesize these research findings about {topic} into a coherent 3-paragraph summary suitable for a museum exhibition:

Facts:
{facts_text}

Create an educational, engaging summary that:
- Provides historical context
- Highlights cultural significance
- Maintains factual accuracy
- Uses accessible language"""

        return self.generate_with_gemini(prompt, temperature=0.6)
