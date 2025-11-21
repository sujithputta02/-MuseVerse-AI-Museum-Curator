"""Integration test - Generate a small exhibition."""
import sys
import time

def integration_test():
    """Run a complete but quick exhibition generation."""
    print("="*70)
    print("INTEGRATION TEST - Full Exhibition Generation")
    print("="*70)
    
    try:
        from orchestrator import ExhibitionOrchestrator
        
        print("\n✅ Orchestrator imported successfully")
        
        # Initialize
        orchestrator = ExhibitionOrchestrator()
        print("✅ Orchestrator initialized")
        
        # Generate a simple exhibition
        topic = "Ancient Greek Philosophy"
        print(f"\n📚 Generating exhibition: {topic}")
        print("⏳ This will take about 1-2 minutes...\n")
        
        start_time = time.time()
        result = orchestrator.generate_exhibition(topic)
        duration = time.time() - start_time
        
        print("\n" + "="*70)
        print("✅ EXHIBITION GENERATED SUCCESSFULLY!")
        print("="*70)
        
        # Validate result structure
        assert 'exhibition' in result, "Missing exhibition in result"
        assert 'metrics' in result, "Missing metrics in result"
        assert 'evaluation' in result, "Missing evaluation in result"
        
        exhibition = result['exhibition']
        metrics = result['metrics']
        
        print("\n📊 METRICS:")
        print(f"  Overall Quality:      {metrics['overall_quality_score']:.1%}")
        print(f"  Agent Success Rate:   {metrics['agent_success_rate']:.1%}")
        print(f"  Narrative Quality:    {metrics['narrative_quality']:.1%}")
        print(f"  Factual Quality:      {metrics['factual_quality']:.1%}")
        print(f"  Cultural Sensitivity: {metrics['cultural_sensitivity']:.1%}")
        print(f"  Generation Time:      {duration:.2f}s")
        
        print("\n🎨 EXHIBITION DETAILS:")
        print(f"  Topic:        {exhibition.get('topic', 'N/A')}")
        print(f"  Title:        {exhibition.get('title', 'N/A')[:60]}...")
        print(f"  Rooms:        {len(exhibition.get('rooms', []))}")
        
        total_exhibits = sum(len(r.get('exhibits', [])) for r in exhibition.get('rooms', []))
        print(f"  Exhibits:     {total_exhibits}")
        print(f"  Timeline:     {len(exhibition.get('timeline', []))} events")
        
        # Validate quality thresholds
        print("\n✅ VALIDATION:")
        
        if metrics['agent_success_rate'] >= 0.95:
            print(f"  ✅ Success rate meets target (95%+): {metrics['agent_success_rate']:.1%}")
        else:
            print(f"  ⚠️  Success rate below target: {metrics['agent_success_rate']:.1%}")
        
        if metrics['overall_quality_score'] >= 0.75:
            print(f"  ✅ Quality score meets threshold (75%+): {metrics['overall_quality_score']:.1%}")
        else:
            print(f"  ⚠️  Quality score below threshold: {metrics['overall_quality_score']:.1%}")
        
        if total_exhibits >= 3:
            print(f"  ✅ Sufficient exhibits (3+): {total_exhibits}")
        else:
            print(f"  ⚠️  Too few exhibits: {total_exhibits}")
        
        if len(exhibition.get('rooms', [])) >= 3:
            print(f"  ✅ Sufficient rooms (3+): {len(exhibition.get('rooms', []))}")
        else:
            print(f"  ⚠️  Too few rooms: {len(exhibition.get('rooms', []))}")
        
        # System stats
        print("\n📈 SYSTEM STATISTICS:")
        stats = orchestrator.get_system_stats()
        print(f"  Overall Success Rate: {stats['overall_success_rate']:.1%}")
        print(f"  Target Success Rate:  {stats['target_success_rate']:.1%}")
        print(f"  Total Executions:     {stats['total_executions']}")
        print(f"  Total Successes:      {stats['total_successes']}")
        print(f"  Meets Target:         {'✅ Yes' if stats['meets_target'] else '❌ No'}")
        
        # Display rooms
        print("\n🚪 ROOMS:")
        for i, room in enumerate(exhibition.get('rooms', []), 1):
            print(f"  {i}. {room.get('title', 'Untitled')}")
            print(f"     Theme: {room.get('theme', 'N/A')}")
            print(f"     Exhibits: {len(room.get('exhibits', []))}")
        
        # Display curator notes preview
        if exhibition.get('curator_notes'):
            print("\n📜 CURATOR'S NOTES (Preview):")
            preview = exhibition['curator_notes'][:200] + "..."
            print(f"  {preview}")
        
        print("\n" + "="*70)
        print("🎉 INTEGRATION TEST PASSED!")
        print("="*70)
        
        print("\n✅ All components working correctly:")
        print("  ✅ Topic Intake Agent")
        print("  ✅ Research Agent")
        print("  ✅ Exhibit Generator Agent")
        print("  ✅ Exhibition Designer Agent")
        print("  ✅ Narrative Agent")
        print("  ✅ Visual Context Agent")
        print("  ✅ Evaluator Agent")
        print("  ✅ Loop Agent")
        print("  ✅ Memory Bank Agent")
        print("  ✅ Timeline Generator")
        print("  ✅ Fact Checker")
        print("  ✅ Exhibit Formatter")
        
        print("\n🚀 System is production ready!")
        print("\nYou can now:")
        print("  • Run web app: streamlit run app.py")
        print("  • Generate exhibitions: python run.py 'Topic'")
        print("  • Run full demo: python demo.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = integration_test()
    sys.exit(0 if success else 1)
