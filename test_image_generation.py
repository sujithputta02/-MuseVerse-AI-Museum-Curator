"""Test script for Image Generator Agent."""
from agents.image_generator_agent import ImageGeneratorAgent
import json

def test_image_generation():
    """Test the image generation agent."""
    print("🎨 Testing Image Generator Agent...")
    print("=" * 60)
    
    # Initialize agent
    agent = ImageGeneratorAgent()
    
    # Sample exhibition data
    test_exhibition = {
        "topic": "Ancient Egyptian Astronomy",
        "title": "Stars of the Pharaohs: Ancient Egyptian Astronomy",
        "overview": "Explore how ancient Egyptians mapped the heavens",
        "rooms": [
            {
                "title": "The Celestial Calendar",
                "theme": "Egyptian astronomical observations",
                "description": "Discover how Egyptians tracked time using the stars",
                "exhibits": [
                    {
                        "name": "The Dendera Zodiac",
                        "description": "A celestial map carved in stone showing constellations",
                        "time_period": "50 BCE",
                        "cultural_significance": "One of the most complete ancient star maps"
                    },
                    {
                        "name": "Merkhet Astronomical Tool",
                        "description": "Ancient Egyptian sighting tool for tracking stars",
                        "time_period": "600 BCE",
                        "cultural_significance": "Used to align pyramids with celestial north"
                    }
                ]
            }
        ]
    }
    
    # Test image generation
    print("\n📸 Generating images for exhibition...")
    result = agent.execute({"exhibition": test_exhibition})
    
    exhibition_with_images = result.get("exhibition", {})
    
    # Display results
    print("\n✅ Image Generation Complete!")
    print("=" * 60)
    
    # Poster
    if exhibition_with_images.get('poster_image'):
        print("\n🎨 EXHIBITION POSTER:")
        poster = exhibition_with_images['poster_image']
        print(f"  Status: {poster.get('status', 'N/A')}")
        if poster.get('enhanced_description'):
            print(f"  Description: {poster['enhanced_description'][:100]}...")
    
    # Rooms and exhibits
    for i, room in enumerate(exhibition_with_images.get('rooms', []), 1):
        print(f"\n🚪 ROOM {i}: {room.get('title', 'Untitled')}")
        
        if room.get('entrance_image'):
            entrance = room['entrance_image']
            print(f"  Entrance Image Status: {entrance.get('status', 'N/A')}")
            if entrance.get('enhanced_description'):
                print(f"  Description: {entrance['enhanced_description'][:80]}...")
        
        for j, exhibit in enumerate(room.get('exhibits', []), 1):
            print(f"\n  🎨 Exhibit {j}: {exhibit.get('name', 'Untitled')}")
            if exhibit.get('generated_image'):
                img = exhibit['generated_image']
                print(f"    Image Status: {img.get('status', 'N/A')}")
                if img.get('enhanced_description'):
                    print(f"    Description: {img['enhanced_description'][:80]}...")
    
    # Agent stats
    print("\n" + "=" * 60)
    print("📊 AGENT STATISTICS:")
    stats = agent.get_stats()
    print(f"  Executions: {stats['executions']}")
    print(f"  Success Rate: {stats['success_rate']*100:.1f}%")
    print(f"  Duration: {stats['total_duration']:.2f}s")
    
    # Save result
    output_file = "test_image_generation_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(exhibition_with_images, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Full output saved to: {output_file}")
    print("\n✅ Test completed successfully!")
    print("\n💡 Note: To generate actual images, integrate with:")
    print("   - Google Imagen API (via Vertex AI)")
    print("   - OpenAI DALL-E 3 API")
    print("   - Stability AI API")
    
    return exhibition_with_images

if __name__ == "__main__":
    test_image_generation()
