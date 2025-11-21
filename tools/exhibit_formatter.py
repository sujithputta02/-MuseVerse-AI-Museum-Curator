"""Exhibit template formatter tool."""
from typing import Dict, List
import json

class ExhibitFormatter:
    """Tool to format exhibits into structured templates."""
    
    def format_exhibit(self, exhibit_data: Dict) -> Dict:
        """Format exhibit data into standard template."""
        template = {
            "name": exhibit_data.get("name", "Untitled Exhibit"),
            "description": exhibit_data.get("description", ""),
            "time_period": exhibit_data.get("time_period", "Unknown"),
            "cultural_significance": exhibit_data.get("cultural_significance", ""),
            "facts": exhibit_data.get("facts", []),
            "visual_refs": exhibit_data.get("visual_refs", []),
            "tags": exhibit_data.get("tags", [])
        }
        return template
    
    def format_room(self, room_data: Dict) -> Dict:
        """Format room data into standard template."""
        template = {
            "title": room_data.get("title", "Untitled Room"),
            "theme": room_data.get("theme", ""),
            "description": room_data.get("description", ""),
            "exhibits": [self.format_exhibit(e) for e in room_data.get("exhibits", [])]
        }
        return template
    
    def format_exhibition(self, exhibition_data: Dict) -> Dict:
        """Format complete exhibition into standard template."""
        template = {
            "topic": exhibition_data.get("topic", ""),
            "title": exhibition_data.get("title", ""),
            "overview": exhibition_data.get("overview", ""),
            "rooms": [self.format_room(r) for r in exhibition_data.get("rooms", [])],
            "timeline": exhibition_data.get("timeline", []),
            "curator_notes": exhibition_data.get("curator_notes", ""),
            "metadata": {
                "created_at": exhibition_data.get("created_at", ""),
                "total_exhibits": sum(len(r.get("exhibits", [])) for r in exhibition_data.get("rooms", [])),
                "total_rooms": len(exhibition_data.get("rooms", []))
            }
        }
        return template
    
    def validate_exhibition(self, exhibition: Dict) -> Dict[str, any]:
        """Validate exhibition structure and completeness."""
        issues = []
        
        if not exhibition.get("topic"):
            issues.append("Missing topic")
        
        if not exhibition.get("rooms"):
            issues.append("No rooms defined")
        
        rooms = exhibition.get("rooms", [])
        for i, room in enumerate(rooms):
            if not room.get("exhibits"):
                issues.append(f"Room {i+1} has no exhibits")
        
        total_exhibits = sum(len(r.get("exhibits", [])) for r in rooms)
        if total_exhibits < 3:
            issues.append("Too few exhibits (minimum 3)")
        
        completeness_score = 1.0
        if issues:
            completeness_score = max(0.5, 1.0 - len(issues) * 0.15)
        
        return {
            "is_valid": len(issues) == 0,
            "completeness_score": completeness_score,
            "issues": issues,
            "total_exhibits": total_exhibits,
            "total_rooms": len(rooms)
        }
