"""Tests for agent functionality."""
import pytest
from agents.topic_intake_agent import TopicIntakeAgent
from agents.research_agent import ResearchAgent
from tools.fact_checker import FactConsistencyChecker
from tools.timeline_generator import TimelineGenerator

def test_topic_intake_agent():
    """Test topic intake agent."""
    agent = TopicIntakeAgent()
    result = agent.execute("Ancient Egypt")
    
    assert result is not None
    assert "original_topic" in result
    assert result["original_topic"] == "Ancient Egypt"
    assert "status" in result

def test_fact_consistency_checker():
    """Test fact consistency checker."""
    checker = FactConsistencyChecker()
    
    facts = [
        "The Great Pyramid was built around 2560 BCE.",
        "Ancient Egyptians used hieroglyphics for writing.",
        "The Nile River was central to Egyptian civilization."
    ]
    
    report = checker.check_consistency(facts)
    
    assert "quality_score" in report
    assert "validated_facts" in report
    assert report["quality_score"] > 0

def test_cultural_sensitivity():
    """Test cultural sensitivity validation."""
    checker = FactConsistencyChecker()
    
    # Good text
    good_text = "Ancient civilizations developed sophisticated technologies."
    result = checker.validate_cultural_sensitivity(good_text)
    assert result["is_sensitive"] == True
    
    # Problematic text
    bad_text = "These primitive people had backward customs."
    result = checker.validate_cultural_sensitivity(bad_text)
    assert result["is_sensitive"] == False

def test_timeline_generator():
    """Test timeline generation."""
    generator = TimelineGenerator()
    
    exhibits = [
        {
            "name": "Early Period",
            "time_period": "2000 BCE",
            "description": "The beginning of the civilization in 2000 BCE."
        },
        {
            "name": "Golden Age",
            "time_period": "1500 BCE",
            "description": "Peak of cultural development around 1500 BCE."
        }
    ]
    
    timeline = generator.generate_timeline(exhibits)
    
    assert len(timeline) > 0
    assert timeline[0]["year"] == "1500"  # Should be sorted
    assert timeline[1]["year"] == "2000"

if __name__ == "__main__":
    pytest.main([__file__])
