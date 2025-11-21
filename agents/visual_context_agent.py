"""Visual Context Agent - manages visual references."""
from typing import Dict, List
from agents.base_agent import BaseAgent
from tools.search_tool import GoogleSearchTool
import config

class VisualContextAgent(BaseAgent):
    """Agent that manages visual references and imagery context."""
    
    def __init__(self):
        super().__init__("VisualContextAgent")
        self.search_tool = GoogleSearchTool(config.GOOGLE_API_KEY)
    
    def _process(self, input_data: Dict) -> Dict:
        """
        Enhance exhibition with visual context.
        
        Args:
            input_data: Exhibition structure
            
        Returns:
            Exhibition with enhanced visual references
        """
        exhibition = input_data.copy()
        
        # Enhance visual references for each exhibit
        for room in exhibition.get("rooms", []):
            for exhibit in room.get("exhibits", []):
                self._enhance_visual_refs(exhibit, exhibition["topic"])
        
        return exhibition
    
    def _enhance_visual_refs(self, exhibit: Dict, topic: str):
        """Enhance visual references for an exhibit."""
        exhibit_name = exhibit.get("name", "")
        
        # Search for visual references
        search_query = f"{topic} {exhibit_name} museum artifact image"
        search_results = self.search_tool.search(search_query, num_results=3)
        
        # Add search URLs to visual references
        visual_refs = exhibit.get("visual_refs", [])
        for result in search_results:
            visual_refs.append({
                "description": result.get("title", ""),
                "source": result.get("link", ""),
                "type": "search_result"
            })
        
        exhibit["visual_refs"] = visual_refs
