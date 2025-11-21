"""Test PDF export functionality."""
from utils.pdf_generator import ExhibitionPDFGenerator
import json

print("📕 Testing PDF Export...")
print("=" * 60)

# Load sample exhibition
try:
    with open('demo_exhibition_1.json', 'r', encoding='utf-8') as f:
        exhibition = json.load(f)
    print("✅ Loaded sample exhibition")
except:
    # Create minimal test exhibition
    exhibition = {
        "topic": "Ancient Egypt",
        "title": "Treasures of Ancient Egypt",
        "overview": "Explore the wonders of ancient Egyptian civilization",
        "curator_notes": "Welcome to this fascinating journey through ancient Egypt...",
        "rooms": [
            {
                "title": "The Pharaohs",
                "theme": "Royal power and divine kingship",
                "description": "Discover the rulers of ancient Egypt",
                "narrative": "The pharaohs were considered living gods...",
                "exhibits": [
                    {
                        "name": "Golden Mask of Tutankhamun",
                        "description": "The iconic golden death mask",
                        "time_period": "1332-1323 BCE",
                        "cultural_significance": "Symbol of ancient Egyptian artistry",
                        "facts": [
                            "Made of 11 kg of solid gold",
                            "Discovered in 1922 by Howard Carter"
                        ]
                    }
                ]
            }
        ],
        "timeline": [
            {
                "year": "3100 BCE",
                "event": "Unification of Egypt",
                "description": "Upper and Lower Egypt united under one ruler"
            }
        ]
    }
    print("✅ Created test exhibition")

# Sample metrics
metrics = {
    "overall_quality_score": 0.92,
    "agent_success_rate": 0.98,
    "narrative_quality": 0.89,
    "cultural_sensitivity": 0.95
}

print("\n📄 Generating HTML/PDF...")
try:
    pdf_gen = ExhibitionPDFGenerator()
    html_content = pdf_gen.generate_pdf(exhibition, metrics)
    
    # Save to file
    output_file = "test_exhibition.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML generated successfully!")
    print(f"📁 Saved to: {output_file}")
    print(f"📊 File size: {len(html_content)} bytes")
    print(f"\n💡 To convert to PDF:")
    print(f"   1. Open {output_file} in your browser")
    print(f"   2. Press Ctrl+P (or Cmd+P on Mac)")
    print(f"   3. Select 'Save as PDF' as the printer")
    print(f"   4. Click Save")
    
    print("\n" + "=" * 60)
    print("✨ PDF Export Features:")
    print("   • Professional museum-style layout")
    print("   • Title page with metrics")
    print("   • Curator's notes section")
    print("   • Detailed room and exhibit descriptions")
    print("   • Historical timeline")
    print("   • Color-coded sections")
    print("   • Ready for printing or sharing")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 Test complete!")
