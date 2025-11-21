"""Demo script showcasing AI Museum Curator capabilities."""
from orchestrator import ExhibitionOrchestrator
import json
import time

def print_header(text):
    """Print formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_section(text):
    """Print formatted section."""
    print("\n" + "-"*70)
    print(f"  {text}")
    print("-"*70 + "\n")

def demo_single_exhibition():
    """Demonstrate single exhibition generation."""
    print_header("🏛️  AI MUSEUM CURATOR - DEMO")
    
    orchestrator = ExhibitionOrchestrator()
    
    # Demo topic
    topic = "Ancient Egyptian Mathematics"
    
    print(f"📚 Generating exhibition for: {topic}")
    print("⏳ This will take about 1-2 minutes...\n")
    
    start_time = time.time()
    
    try:
        result = orchestrator.generate_exhibition(topic)
        duration = time.time() - start_time
        
        print_section("✅ GENERATION COMPLETE")
        
        # Display metrics
        print_section("📊 METRICS")
        metrics = result['metrics']
        
        print(f"Overall Quality Score:    {metrics['overall_quality_score']:.1%}")
        print(f"Agent Success Rate:       {metrics['agent_success_rate']:.1%}")
        print(f"Narrative Quality:        {metrics['narrative_quality']:.1%}")
        print(f"Factual Quality:          {metrics['factual_quality']:.1%}")
        print(f"Cultural Sensitivity:     {metrics['cultural_sensitivity']:.1%}")
        print(f"Generation Time:          {duration:.2f} seconds")
        
        # Display exhibition info
        print_section("🎨 EXHIBITION DETAILS")
        exhibition = result['exhibition']
        
        print(f"Title: {exhibition.get('title', topic)}")
        print(f"Rooms: {len(exhibition.get('rooms', []))}")
        
        total_exhibits = sum(len(r.get('exhibits', [])) for r in exhibition.get('rooms', []))
        print(f"Total Exhibits: {total_exhibits}")
        print(f"Timeline Events: {len(exhibition.get('timeline', []))}")
        
        # Display rooms
        print_section("🚪 ROOMS")
        for i, room in enumerate(exhibition.get('rooms', []), 1):
            print(f"{i}. {room.get('title', 'Untitled')}")
            print(f"   Theme: {room.get('theme', 'N/A')}")
            print(f"   Exhibits: {len(room.get('exhibits', []))}")
        
        # Display curator notes preview
        print_section("📜 CURATOR'S NOTES (Preview)")
        curator_notes = exhibition.get('curator_notes', '')
        preview = curator_notes[:300] + "..." if len(curator_notes) > 300 else curator_notes
        print(preview)
        
        # System stats
        print_section("📈 SYSTEM STATISTICS")
        stats = orchestrator.get_system_stats()
        
        print(f"Overall Success Rate:     {stats['overall_success_rate']:.1%}")
        print(f"Target Success Rate:      {stats['target_success_rate']:.1%}")
        print(f"Meets Target:             {'✅ Yes' if stats['meets_target'] else '❌ No'}")
        print(f"Total Executions:         {stats['total_executions']}")
        print(f"Total Successes:          {stats['total_successes']}")
        
        # Save exhibition
        filename = f"demo_exhibition_{result.get('exhibition_id', 'export')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(exhibition, f, indent=2, ensure_ascii=False)
        
        print_section("💾 EXPORT")
        print(f"Exhibition saved to: {filename}")
        
        print_header("🎉 DEMO COMPLETE")
        print("\nTo explore the full exhibition, run:")
        print("  streamlit run app.py")
        print("\nOr view the saved JSON file:")
        print(f"  {filename}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def demo_multiple_topics():
    """Demonstrate multiple exhibition generation."""
    print_header("🏛️  AI MUSEUM CURATOR - MULTI-TOPIC DEMO")
    
    orchestrator = ExhibitionOrchestrator()
    
    topics = [
        "Renaissance Art",
        "Viking Navigation",
        "Aztec Astronomy"
    ]
    
    results = []
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] Generating: {topic}...")
        
        try:
            result = orchestrator.generate_exhibition(topic)
            results.append({
                'topic': topic,
                'success': True,
                'quality_score': result['metrics']['overall_quality_score'],
                'success_rate': result['metrics']['agent_success_rate'],
                'duration': result['metrics']['total_duration_seconds']
            })
            print(f"✅ Success - Quality: {result['metrics']['overall_quality_score']:.1%}")
        except Exception as e:
            results.append({
                'topic': topic,
                'success': False,
                'error': str(e)
            })
            print(f"❌ Failed: {str(e)}")
    
    # Summary
    print_section("📊 SUMMARY")
    
    successful = [r for r in results if r.get('success', False)]
    failed = [r for r in results if not r.get('success', False)]
    
    print(f"Total Topics:        {len(topics)}")
    print(f"Successful:          {len(successful)}")
    print(f"Failed:              {len(failed)}")
    print(f"Success Rate:        {len(successful)/len(topics):.1%}")
    
    if successful:
        avg_quality = sum(r['quality_score'] for r in successful) / len(successful)
        avg_duration = sum(r['duration'] for r in successful) / len(successful)
        print(f"\nAverage Quality:     {avg_quality:.1%}")
        print(f"Average Duration:    {avg_duration:.2f}s")
    
    # Final system stats
    print_section("📈 FINAL SYSTEM STATISTICS")
    stats = orchestrator.get_system_stats()
    
    print(f"Overall Success Rate: {stats['overall_success_rate']:.1%}")
    print(f"Target Success Rate:  {stats['target_success_rate']:.1%}")
    print(f"Status:               {'✅ TARGET MET' if stats['meets_target'] else '❌ BELOW TARGET'}")
    
    print_header("🎉 MULTI-TOPIC DEMO COMPLETE")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "multi":
        demo_multiple_topics()
    else:
        demo_single_exhibition()
        print("\nTip: Run 'python demo.py multi' for multi-topic demo")
