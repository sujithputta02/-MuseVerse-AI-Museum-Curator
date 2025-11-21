"""Main orchestrator for multi-agent exhibition generation."""
import time
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from agents.topic_intake_agent import TopicIntakeAgent
from agents.research_agent import ResearchAgent
from agents.exhibit_generator_agent import ExhibitGeneratorAgent
from agents.exhibition_designer_agent import ExhibitionDesignerAgent
from agents.narrative_agent import NarrativeAgent
from agents.visual_context_agent import VisualContextAgent
from agents.evaluator_agent import EvaluatorAgent
from agents.loop_agent import LoopAgent
from agents.memory_bank_agent import MemoryBankAgent
from agents.semantic_analyzer_agent import SemanticAnalyzerAgent
from agents.interactive_guide_agent import InteractiveGuideAgent
from agents.multimedia_curator_agent import MultimediaCuratorAgent
from agents.accessibility_agent import AccessibilityAgent
from agents.image_generator_agent import ImageGeneratorAgent
from tools.timeline_generator import TimelineGenerator
from utils.logger import get_logger
import config

class ExhibitionOrchestrator:
    """Orchestrates multi-agent workflow for exhibition generation."""
    
    def __init__(self):
        self.logger = get_logger()
        
        # Initialize core agents
        self.topic_intake = TopicIntakeAgent()
        self.research = ResearchAgent()
        self.exhibit_generator = ExhibitGeneratorAgent()
        self.exhibition_designer = ExhibitionDesignerAgent()
        self.narrative = NarrativeAgent()
        self.visual_context = VisualContextAgent()
        self.evaluator = EvaluatorAgent()
        self.loop = LoopAgent()
        self.memory_bank = MemoryBankAgent()
        
        # Initialize advanced agents (NEW!)
        self.semantic_analyzer = SemanticAnalyzerAgent()
        self.interactive_guide = InteractiveGuideAgent()
        self.multimedia_curator = MultimediaCuratorAgent()
        self.accessibility = AccessibilityAgent()
        self.image_generator = ImageGeneratorAgent()
        
        # Tools
        self.timeline_generator = TimelineGenerator()
        
        self.agents = [
            self.topic_intake,
            self.research,
            self.exhibit_generator,
            self.exhibition_designer,
            self.narrative,
            self.visual_context,
            self.evaluator,
            self.loop,
            self.memory_bank,
            self.semantic_analyzer,
            self.interactive_guide,
            self.multimedia_curator,
            self.accessibility,
            self.image_generator
        ]
    
    def generate_exhibition(self, topic: str) -> Dict:
        """
        Generate complete exhibition using multi-agent workflow.
        
        Args:
            topic: Exhibition topic
            
        Returns:
            Complete exhibition with metadata
        """
        start_time = time.time()
        
        self.logger.logger.info(f"Starting exhibition generation for: {topic}")
        
        # Step 1: Topic Intake (Sequential)
        topic_data = self.topic_intake.execute(topic)
        
        # Step 2: Research & Visual Context (Parallel)
        research_data, visual_prep = self._parallel_research_phase(topic_data)
        
        # Step 3: Generate Exhibits (Sequential)
        exhibits = self.exhibit_generator.execute(research_data)
        
        # Step 4: Design Exhibition (Sequential)
        exhibition_structure = self.exhibition_designer.execute({
            "topic": topic_data.get("original_topic", topic),
            "exhibits": exhibits,
            "topic_data": topic_data
        })
        
        # Step 5: Add Narrative (Sequential)
        exhibition_with_narrative = self.narrative.execute(exhibition_structure)
        
        # Step 6: Enhance Visual Context (Sequential)
        exhibition_with_visuals = self.visual_context.execute(exhibition_with_narrative)
        
        # Step 7: Generate Timeline
        timeline = self.timeline_generator.generate_timeline(exhibits)
        exhibition_with_visuals["timeline"] = timeline
        
        # Step 8: Semantic Analysis (NEW!) - with error handling
        try:
            semantic_analysis = self.semantic_analyzer.execute({
                "topic": topic_data.get("original_topic", topic),
                "research_summary": research_data.get("research_summary", "")
            })
            exhibition_with_visuals["semantic_analysis"] = semantic_analysis
        except Exception as e:
            self.logger.logger.warning(f"Semantic analysis skipped: {str(e)}")
            exhibition_with_visuals["semantic_analysis"] = {
                "key_concepts": [],
                "connections": [],
                "thematic_insights": "Analysis unavailable",
                "semantic_score": 0.5
            }
        
        # Step 9: Add Interactive Elements (NEW!) - with error handling
        try:
            exhibition_with_interactive = self.interactive_guide.execute(exhibition_with_visuals)
        except Exception as e:
            self.logger.logger.warning(f"Interactive elements skipped: {str(e)}")
            exhibition_with_interactive = exhibition_with_visuals
            exhibition_with_interactive["quiz"] = {"title": "Quiz unavailable", "questions": []}
            exhibition_with_interactive["challenges"] = []
        
        # Step 10: Add Multimedia Recommendations (NEW!)
        exhibition_with_multimedia = self.multimedia_curator.execute(exhibition_with_interactive)
        
        # Step 11: Add Accessibility Features (NEW!)
        exhibition_with_accessibility = self.accessibility.execute(exhibition_with_multimedia)
        
        # Step 12: Generate AI Images (NEW!)
        try:
            exhibition_with_images = self.image_generator.execute({
                "exhibition": exhibition_with_accessibility
            })
            final_exhibition_data = exhibition_with_images.get("exhibition", exhibition_with_accessibility)
        except Exception as e:
            self.logger.logger.warning(f"Image generation skipped: {str(e)}")
            final_exhibition_data = exhibition_with_accessibility
        
        # Step 13: Evaluate (Sequential)
        evaluation = self.evaluator.execute(final_exhibition_data)
        
        # Step 14: Refinement Loop (if needed)
        final_exhibition = self._refinement_loop(final_exhibition_data, evaluation)
        
        # Step 15: Store in Memory Bank
        storage_result = self.memory_bank.execute({
            "exhibition": final_exhibition,
            "evaluation": evaluation
        })
        
        duration = time.time() - start_time
        
        # Log completion
        self.logger.log_exhibition_created(
            topic,
            str(storage_result.get("exhibition_id", "unknown"))
        )
        
        # Calculate metrics
        metrics = self._calculate_metrics(evaluation, duration)
        self.logger.log_metrics(metrics)
        
        return {
            "exhibition": final_exhibition,
            "evaluation": evaluation,
            "metrics": metrics,
            "exhibition_id": storage_result.get("exhibition_id"),
            "duration": duration
        }
    
    def _parallel_research_phase(self, topic_data: Dict) -> tuple:
        """Execute research and visual prep in parallel."""
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Submit parallel tasks
            research_future = executor.submit(self.research.execute, topic_data)
            visual_future = executor.submit(lambda: {"status": "prepared"})
            
            # Wait for completion
            research_data = research_future.result()
            visual_prep = visual_future.result()
        
        return research_data, visual_prep
    
    def _refinement_loop(self, exhibition: Dict, evaluation: Dict) -> Dict:
        """Refine exhibition if quality below threshold."""
        current_exhibition = exhibition
        current_evaluation = evaluation
        loops = 0
        
        # More aggressive refinement threshold
        while (current_evaluation.get("overall_score", 0) < 0.80 
               and loops < config.MAX_REFINEMENT_LOOPS):
            
            self.logger.logger.info(f"Refinement loop {loops + 1}")
            
            # Refine
            loop_result = self.loop.execute({
                "exhibition": current_exhibition,
                "evaluation": current_evaluation
            })
            
            if not loop_result.get("refined", False):
                break
            
            current_exhibition = loop_result["exhibition"]
            
            # Re-evaluate
            current_evaluation = self.evaluator.execute(current_exhibition)
            loops += 1
        
        return current_exhibition
    
    def _calculate_metrics(self, evaluation: Dict, duration: float) -> Dict:
        """Calculate overall system metrics."""
        # Agent success rates
        agent_stats = [agent.get_stats() for agent in self.agents]
        total_success_rate = sum(s["success_rate"] for s in agent_stats) / len(agent_stats)
        
        return {
            "overall_quality_score": evaluation.get("overall_score", 0.0),
            "completeness_score": evaluation.get("completeness_score", 0.0),
            "narrative_quality": evaluation.get("narrative_quality", 0.0),
            "factual_quality": evaluation.get("factual_quality", 0.0),
            "cultural_sensitivity": evaluation.get("cultural_sensitivity", 0.0),
            "agent_success_rate": total_success_rate,
            "total_duration_seconds": duration,
            "meets_quality_threshold": evaluation.get("meets_threshold", False)
        }
    
    def get_system_stats(self) -> Dict:
        """Get overall system statistics."""
        agent_stats = [agent.get_stats() for agent in self.agents]
        
        total_executions = sum(s["executions"] for s in agent_stats)
        total_successes = sum(s["successes"] for s in agent_stats)
        overall_success_rate = total_successes / total_executions if total_executions > 0 else 0
        
        return {
            "overall_success_rate": overall_success_rate,
            "total_executions": total_executions,
            "total_successes": total_successes,
            "agent_stats": agent_stats,
            "target_success_rate": config.TARGET_SUCCESS_RATE,
            "meets_target": overall_success_rate >= config.TARGET_SUCCESS_RATE
        }
