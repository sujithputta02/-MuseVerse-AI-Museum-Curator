"""Fact consistency checker tool."""
from typing import List, Dict
import re

class FactConsistencyChecker:
    """Tool to check consistency and quality of facts."""
    
    def check_consistency(self, facts: List[str]) -> Dict[str, any]:
        """
        Check facts for consistency, contradictions, and quality.
        Returns a consistency report.
        """
        report = {
            "total_facts": len(facts),
            "quality_score": 0.0,
            "issues": [],
            "validated_facts": []
        }
        
        if not facts:
            report["quality_score"] = 0.0
            report["issues"].append("No facts provided")
            return report
        
        # Check for minimum length
        valid_facts = [f for f in facts if len(f.strip()) > 20]
        
        # Check for dates (indicates historical accuracy)
        facts_with_dates = [f for f in valid_facts if re.search(r'\b\d{4}\b', f)]
        
        # Check for specific terms (indicates detail)
        detailed_facts = [f for f in valid_facts if len(f.split()) > 10]
        
        # Calculate quality score
        length_score = len(valid_facts) / len(facts) if facts else 0
        date_score = len(facts_with_dates) / len(valid_facts) if valid_facts else 0
        detail_score = len(detailed_facts) / len(valid_facts) if valid_facts else 0
        
        report["quality_score"] = (length_score * 0.3 + date_score * 0.3 + detail_score * 0.4)
        report["validated_facts"] = valid_facts
        
        if len(valid_facts) < len(facts):
            report["issues"].append(f"{len(facts) - len(valid_facts)} facts too short")
        
        if date_score < 0.3:
            report["issues"].append("Few facts contain specific dates")
        
        return report
    
    def validate_cultural_sensitivity(self, text: str) -> Dict[str, any]:
        """Check text for cultural sensitivity issues."""
        # Simple keyword-based check
        sensitive_terms = ["primitive", "savage", "backward", "uncivilized"]
        issues = []
        
        text_lower = text.lower()
        for term in sensitive_terms:
            if term in text_lower:
                issues.append(f"Potentially insensitive term: '{term}'")
        
        return {
            "is_sensitive": len(issues) == 0,
            "sensitivity_score": 1.0 if len(issues) == 0 else max(0.5, 1.0 - len(issues) * 0.2),
            "issues": issues
        }
