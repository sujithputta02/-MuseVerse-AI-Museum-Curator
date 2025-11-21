"""Quick demo of Image Generation feature."""
import json
from agents.image_generator_agent import ImageGeneratorAgent

print("🎨 AI Museum Curator - Image Generation Demo")
print("=" * 70)
print()

# Sample mini exhibition
mini_exhibition = {
    "topic": "Renaissance Art",
    "title": "Masters of the Renaissance",
    "overview": "Explore the artistic revolution of 15th century Italy",
    "rooms": [
        {
            "title": "The Florentine Masters",
            "theme": "Birth of Renaissance art in Florence",
            "description": "Discover the pioneering artists of Florence",
            "exhibits": [
                {
                    "name": "Mona Lisa Study",
                    "description": "Leonardo da Vinci's masterpiece of portraiture",
                    "time_period": "1503-1519",
                    "cultural_significance": "Revolutionary use of sfumato technique"
                }
            ]
        }
    ]
}

print("📚 Sample Exhibition: Renaissance Art")
print(f"   Rooms: {len(mini_exhibition['rooms'])}")
print(f"   Exhibits: {sum(len(r['exhibits']) for r in mini_exhibition['rooms'])}")
print()

# Initialize agent
print("🤖 Initializing Image Generator Agent...")
agent = ImageGeneratorAgent()
print("   ✅ Agent ready!")
print()

# Generate images
print("🎨 Generating AI image descriptions...")
print("   (This uses Gemini to create optimized prompts)")
print()

try:
    result = agent.execute({"exhibition": mini_exhibition})
    exhibition_with_images = result.get("exhibition", {})
    
    print("✅ Generation Complete!")
    print("=" * 70)
    print()
    
    # Show poster
    if exhibition_with_images.get('poster_image'):
        print("🖼️  EXHIBITION POSTER")
        poster = exhibition_with_images['poster_image']
        print(f"   Status: {poster.get('status', 'N/A')}")
        print(f"   Note: {poster.get('note', 'N/A')}")
        print()
    
    # Show room images
    for room in exhibition_with_images.get('rooms', []):
        print(f"🚪 ROOM: {room.get('title', 'Untitled')}")
        if room.get('entrance_image'):
            entrance = room['entrance_image']
            print(f"   Entrance Image: {entrance.get('status', 'N/A')}")
        
        # Show exhibit images
        for exhibit in room.get('exhibits', []):
            print(f"   🎨 {exhibit.get('name', 'Untitled')}")
            if exhibit.get('generated_image'):
                img = exhibit['generated_image']
                print(f"      Image: {img.get('status', 'N/A')}")
        print()
    
    # Stats
    stats = agent.get_stats()
    print("=" * 70)
    print("📊 AGENT STATISTICS")
    print(f"   Success Rate: {stats['success_rate']*100:.0f}%")
    print(f"   Duration: {stats['total_duration']:.2f}s")
    print()
    
    print("=" * 70)
    print("✨ WHAT'S NEW:")
    print("   • 14th specialized agent added!")
    print("   • Exhibition posters generated")
    print("   • Room entrance visuals created")
    print("   • Individual exhibit images produced")
    print("   • Ready to integrate with Imagen/DALL-E")
    print()
    print("💡 NEXT STEPS:")
    print("   1. Add API key for Imagen or DALL-E")
    print("   2. Uncomment integration code in image_generator_agent.py")
    print("   3. Run streamlit app to see visual exhibitions!")
    print()
    print("📖 See IMAGE_GENERATION_GUIDE.md for full details")
    print("=" * 70)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print()
print("🎉 Demo complete!")
