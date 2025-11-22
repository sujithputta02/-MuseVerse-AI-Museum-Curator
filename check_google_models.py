"""Check available Google AI models."""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

print("🔍 Checking available Google AI models...")
print("=" * 80)

# List all available models
models = genai.list_models()

print("\n📋 ALL AVAILABLE MODELS:\n")

text_models = []
image_models = []
other_models = []

for model in models:
    model_name = model.name
    supported_methods = [method for method in model.supported_generation_methods]
    
    print(f"Model: {model_name}")
    print(f"  Display Name: {model.display_name}")
    print(f"  Description: {model.description}")
    print(f"  Supported Methods: {supported_methods}")
    print(f"  Input Token Limit: {model.input_token_limit}")
    print(f"  Output Token Limit: {model.output_token_limit}")
    print("-" * 80)
    
    # Categorize models
    if 'generateContent' in supported_methods:
        if 'image' in model_name.lower() or 'vision' in model_name.lower() or 'imagen' in model_name.lower():
            image_models.append(model_name)
        else:
            text_models.append(model_name)
    else:
        other_models.append(model_name)

print("\n" + "=" * 80)
print("📊 SUMMARY:")
print("=" * 80)

print(f"\n💬 TEXT GENERATION MODELS ({len(text_models)}):")
for model in text_models:
    print(f"  - {model}")

print(f"\n🎨 IMAGE/VISION MODELS ({len(image_models)}):")
if image_models:
    for model in image_models:
        print(f"  - {model}")
else:
    print("  ❌ No image generation models found")

print(f"\n🔧 OTHER MODELS ({len(other_models)}):")
for model in other_models[:5]:  # Show first 5
    print(f"  - {model}")

print("\n" + "=" * 80)
print("🔍 SEARCHING FOR 'NANO' OR 'BANANA' MODELS:")
print("=" * 80)

nano_models = [m.name for m in genai.list_models() if 'nano' in m.name.lower() or 'banana' in m.name.lower()]
if nano_models:
    print("\n✅ Found models:")
    for model in nano_models:
        print(f"  - {model}")
else:
    print("\n❌ No models with 'nano' or 'banana' in the name found")

print("\n" + "=" * 80)
print("💡 RECOMMENDATION:")
print("=" * 80)
print("\nGoogle's Gemini API currently does NOT support image generation.")
print("Image generation is only available through:")
print("  1. Vertex AI Imagen (requires Google Cloud setup)")
print("  2. External services (DALL-E, Stable Diffusion, etc.)")
print("\nFor this project, we're using image descriptions instead.")
print("=" * 80)
