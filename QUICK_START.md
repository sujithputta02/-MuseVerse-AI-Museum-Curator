# 🚀 Quick Start Guide

Get MuseVerse AI Museum Curator up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Google AI API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/sujithputta02/-MuseVerse-AI-Museum-Curator.git
cd -MuseVerse-AI-Museum-Curator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_api_key_here
```

### 4. Test Your Setup

```bash
python test_api_key.py
```

You should see: ✅ API key is VALID and working!

### 5. Launch the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## First Exhibition

1. Enter a topic (e.g., "Ancient Rome", "Space Exploration")
2. Click "Generate Exhibition"
3. Wait 1-2 minutes for AI to create your museum
4. Explore rooms, exhibits, and interactive features!

## Features to Try

- 🎨 **AI-Generated Images** - Visual representations for each exhibit
- 📊 **Knowledge Graphs** - Interactive relationship visualizations
- ⏱️ **Timeline View** - Chronological exploration
- 📄 **PDF Export** - Download complete exhibition catalogs
- ♿ **Accessibility** - Screen reader support and alt text

## Troubleshooting

### API Key Issues
```bash
python check_google_models.py
```

### Database Issues
```bash
python check_database.py
```

### Need Help?
- Check [INSTALLATION.md](INSTALLATION.md) for detailed setup
- Review [SECURITY.md](SECURITY.md) for best practices
- See [ARCHITECTURE.md](ARCHITECTURE.md) for system design

## Next Steps

- Read [README.md](README.md) for full documentation
- Explore [IMAGE_GENERATION_GUIDE.md](IMAGE_GENERATION_GUIDE.md) for image features
- Check [UNIQUE_FEATURES.txt](UNIQUE_FEATURES.txt) for advanced capabilities

---

**Enjoy creating AI-powered museum exhibitions!** 🏛️✨
