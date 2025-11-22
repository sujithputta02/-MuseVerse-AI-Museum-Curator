"""Quick test to verify API key is working."""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("❌ ERROR: No API key found in .env file")
    exit(1)

print("✅ API key loaded from .env file")
print(f"   Key starts with: {api_key[:10]}...")

# Test the API key
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print("\n🧪 Testing API connection...")
    response = model.generate_content("Say 'Hello from MuseVerse!'")
    
    print("✅ API key is VALID and working!")
    print(f"   Response: {response.text}")
    print("\n🎉 Your setup is ready! You can now run:")
    print("   streamlit run app.py")
    
except Exception as e:
    print(f"\n❌ ERROR: API key test failed")
    print(f"   Error: {str(e)}")
    print("\n💡 Solutions:")
    print("   1. Check if your API key is correct")
    print("   2. Visit https://makersuite.google.com/app/apikey")
    print("   3. Create a new API key if needed")
    print("   4. Update the .env file with the new key")
