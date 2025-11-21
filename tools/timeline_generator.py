"""Timeline generator tool."""
from typing import List, Dict
import re
from datetime import datetime

class TimelineGenerator:
    """Tool to generate chronological timelines from exhibits."""
    
    def extract_dates(self, text: str) -> List[str]:
        """Extract year dates from text."""
        # Match 4-digit years
        years = re.findall(r'\b(\d{4})\b', text)
        return years
    
    def generate_timeline(self, exhibits: List[Dict]) -> List[Dict]:
        """Generate timeline from exhibits."""
        timeline_events = []
        
        for exhibit in exhibits:
            # Extract dates from time_period and description
            time_period = exhibit.get("time_period", "")
            description = exhibit.get("description", "")
            
            dates = self.extract_dates(time_period + " " + description)
            
            if dates:
                # Use first date found
                year = dates[0]
                timeline_events.append({
                    "year": year,
                    "event": exhibit.get("name", "Unknown Event"),
                    "description": description[:200] + "..." if len(description) > 200 else description
                })
        
        # Sort by year
        timeline_events.sort(key=lambda x: x["year"])
        
        return timeline_events
    
    def format_timeline_text(self, timeline: List[Dict]) -> str:
        """Format timeline as readable text."""
        if not timeline:
            return "No timeline events available."
        
        text = "TIMELINE\n" + "="*50 + "\n\n"
        for event in timeline:
            text += f"{event['year']}: {event['event']}\n"
            text += f"   {event['description']}\n\n"
        
        return text
