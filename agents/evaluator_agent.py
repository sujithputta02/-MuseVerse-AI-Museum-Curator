"""Evaluator Agent - evaluates exhibition quality."""
from typing import Dict
from agents.base_agent import BaseAgent
from tools.fact_checker import FactConsistencyChecker
from tools.exhibit_formatter import ExhibitFormatter
import config

class EvaluatorAgent(BaseAgent):
    """Agent that evaluates exhibition quality and completeness."""
    
    def __init__(self):
        super().__init__("EvaluatorAgent")
        self.fact_checker = FactConsistencyChecker()
        self.formatter = ExhibitFormatter()
    
    def _process(self, input_data: Dict) -> Dict:
        """
        Evaluate exhibition quality.
        
        Args:
            input_data: Complete exhibition
            
        Returns:
            Evaluation report with scores
        """
        exhibition = input_data
        
        # Validate structure
        validation = self.formatter.validate_exhibition(exhibition)
        
        # Evaluate content quality
        content_scores = self._evaluate_content(exhibition)
        
        # Check cultural sensitivity
        sensitivity_score = self._evaluate_cultural_sensitivity(exhibition)
        
        # Calculate overall score with adjusted weights
        overall_score = (
            validation["completeness_score"] * 0.30 +
            content_scores["narrative_quality"] * 0.25 +
            content_scores["factual_quality"] * 0.20 +
            sensitivity_score * 0.25
        )
        
        report = {
            "overall_score": overall_score,
            "completeness_score": validation["completeness_score"],
            "narrative_quality": content_scores["narrative_quality"],
            "factual_quality": content_scores["factual_quality"],
            "cultural_sensitivity": sensitivity_score,
            "validation": validation,
            "meets_threshold": overall_score >= config.MIN_QUALITY_SCORE,
            "recommendations": self._generate_recommendations(overall_score, validation)
        }
        
        return report
    
    def _evaluate_content(self, exhibition: Dict) -> Dict:
        """Evaluate content quality."""
        # Check narrative quality
        curator_notes = exhibition.get("curator_notes", "")
        narrative_quality = min(1.0, len(curator_notes.split()) / 200)  # Target 200+ words
        
        # Check factual quality
        all_facts = []
        for room in exhibition.get("rooms", []):
            for exhibit in room.get("exhibits", []):
                all_facts.extend(exhibit.get("facts", []))
        
        fact_report = self.fact_checker.check_consistency(all_facts)
        factual_quality = fact_report.get("quality_score", 0.5)
        
        return {
            "narrative_quality": narrative_quality,
            "factual_quality": factual_quality
        }
    
    def _evaluate_cultural_sensitivity(self, exhibition: Dict) -> float:
        """Evaluate cultural sensitivity of content."""
        # Check all text content
        all_text = exhibition.get("curator_notes", "")
        
        for room in exhibition.get("rooms", []):
            all_text += " " + room.get("description", "")
            for exhibit in room.get("exhibits", []):
                all_text += " " + exhibit.get("description", "")
        
        sensitivity_report = self.fact_checker.validate_cultural_sensitivity(all_text)
        return sensitivity_report.get("sensitivity_score", 1.0)
    
    def _generate_recommendations(self, score: float, validation: Dict) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        if score < config.MIN_QUALITY_SCORE:
            recommendations.append("Overall quality below threshold - consider refinement")
        
        if validation.get("issues"):
            for issue in validation["issues"]:
                recommendations.append(f"Structure: {issue}")
        
        if validation.get("total_exhibits", 0) < 5:
            recommendations.append("Add more exhibits for richer content")
        
        return recommendations
