"""Configuration settings for AI Museum Curator."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model Configuration
MODEL_NAME = "gemini-2.5-flash"  # Latest stable model with high quota
TEMPERATURE = 0.8  # Increased for more creative outputs
MAX_TOKENS = 8192
REQUEST_DELAY = 1.0  # Delay between API calls to avoid rate limits

# Agent Configuration
MAX_RESEARCH_RESULTS = 15  # Increased for better research
MAX_EXHIBITS_PER_ROOM = 4  # Optimized for better distribution
MIN_QUALITY_SCORE = 0.70  # Slightly lowered for more flexibility
MAX_REFINEMENT_LOOPS = 3  # Increased refinement attempts

# Performance Mode
FAST_MODE = False  # Disable fast mode - use all features
SKIP_OPTIONAL_AGENTS = False  # Run all 14 agents

# Storage Configuration
DATABASE_PATH = "data/exhibitions.db"
CACHE_DIR = "data/cache"
LOGS_DIR = "logs"
EXHIBITIONS_DIR = "exhibitions"

# Evaluation Thresholds
ACCURACY_THRESHOLD = 0.85
NARRATIVE_THRESHOLD = 0.80
CULTURAL_SENSITIVITY_THRESHOLD = 0.90
COMPLETENESS_THRESHOLD = 0.85

# Success Rate Target
TARGET_SUCCESS_RATE = 0.97  # 97% target for agent success

# Image Generation Configuration
ENABLE_IMAGE_GENERATION = True  # Toggle image generation
IMAGE_GENERATION_SERVICE = "gemini"  # Options: "gemini", "imagen", "dalle", "stable-diffusion"
IMAGE_OUTPUT_DIR = "data/generated_images"
IMAGE_QUALITY = "standard"  # Options: "standard", "hd"
IMAGE_SIZE = "1792x1024"  # Landscape format for museum displays
