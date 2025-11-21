"""Simple CLI runner for testing the system."""
import sys
from orchestrator import ExhibitionOrchestrator
import json

def main():
    """Run exhibition generation from command line."""
    if len(sys.argv) < 2:
        print("Usage: python run.py <topic>")
        print("Example: python run.py 'Aztec Astronomy'")
        sys.exit(1)
    
    topic = " ".join(sys.argv[1:])
    
    print(f"\n🏛️  AI Museum Curator")
    print(f"{'=' * 60}")
    print(f"Generating exhibition for: {topic}")
    print(f"{'=' * 60}\n")
    
    orchestrator = ExhibitionOrchestrator()
    
    try:
        result = orchestrator.generate_exhibition(topic)
        
        print("\n✅ Exhibition Generated Successfully!\n")
        print(f"{'=' * 60}")
        print("METRICS")
        print(f"{'=' * 60}")
        
        metrics = result['metrics']
        print(f"Overall Quality Score: {metrics['overall_quality_score']:.1%}")
        print(f"Agent Success Rate: {metrics['agent_success_rate']:.1%}")
        print(f"Narrative Quality: {metrics['narrative_quality']:.1%}")
        print(f"Factual Quality: {metrics['factual_quality']:.1%}")
        print(f"Cultural Sensitivity: {metrics['cultural_sensitivity']:.1%}")
        print(f"Duration: {metrics['total_duration_seconds']:.2f}s")
        
        print(f"\n{'=' * 60}")
        print("EXHIBITION")
        print(f"{'=' * 60}\n")
        
        exhibition = result['exhibition']
        print(f"Title: {exhibition.get('title', topic)}")
        print(f"Rooms: {len(exhibition.get('rooms', []))}")
        
        total_exhibits = sum(len(r.get('exhibits', [])) for r in exhibition.get('rooms', []))
        print(f"Total Exhibits: {total_exhibits}")
        
        print(f"\nExhibition ID: {result.get('exhibition_id')}")
        
        # Save to file
        filename = f"exhibition_{result.get('exhibition_id')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(exhibition, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved to: {filename}")
        
        # System stats
        print(f"\n{'=' * 60}")
        print("SYSTEM STATISTICS")
        print(f"{'=' * 60}")
        
        stats = orchestrator.get_system_stats()
        print(f"Overall Success Rate: {stats['overall_success_rate']:.1%}")
        print(f"Total Executions: {stats['total_executions']}")
        print(f"Total Successes: {stats['total_successes']}")
        print(f"Target Success Rate: {stats['target_success_rate']:.1%}")
        print(f"Meets Target: {'✅ Yes' if stats['meets_target'] else '❌ No'}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
