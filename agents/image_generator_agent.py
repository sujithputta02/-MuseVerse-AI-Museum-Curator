"""Image Generator Agent - Generates AI images for exhibits using Google Imagen."""
import os
import base64
import requests
from typing import Dict, List, Any
from agents.base_agent import BaseAgent
import config

class ImageGeneratorAgent(BaseAgent):
    """Agent that generates AI images for museum exhibits."""
    
    def __init__(self):
        super().__init__("ImageGeneratorAgent")
        self.image_dir = "data/generated_images"
        os.makedirs(self.image_dir, exist_ok=True)
        
    def _process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate images for exhibition exhibits and rooms."""
        exhibition = input_data.get('exhibition', {})
        
        # Generate exhibition poster
        poster_prompt = self._create_poster_prompt(exhibition)
        poster_url = self._generate_image_with_gemini(poster_prompt)
        exhibition['poster_image'] = poster_url
        
        # Generate images for each room and exhibit
        rooms = exhibition.get('rooms', [])
        for room in rooms:
            # Generate room entrance image
            room_prompt = self._create_room_prompt(room, exhibition.get('topic', ''))
            room['entrance_image'] = self._generate_image_with_gemini(room_prompt)
            
            # Generate images for exhibits in the room
            exhibits = room.get('exhibits', [])
            for exhibit in exhibits:
                exhibit_prompt = self._create_exhibit_prompt(exhibit, room.get('theme', ''))
                exhibit['generated_image'] = self._generate_image_with_gemini(exhibit_prompt)
        
        return {'exhibition': exhibition}
    
    def _create_poster_prompt(self, exhibition: Dict) -> str:
        """Create prompt for exhibition poster."""
        topic = exhibition.get('topic', 'Museum Exhibition')
        title = exhibition.get('title', topic)
        overview = exhibition.get('overview', '')[:200]
        
        prompt = f"""Create a professional museum exhibition poster for "{title}".

Theme: {topic}
Overview: {overview}

Style: Museum-quality poster with elegant typography, warm lighting, sophisticated composition.
Include: Key visual elements representing the exhibition theme, museum aesthetic, professional design.
Mood: Educational, inviting, culturally respectful, visually striking.
Format: Landscape poster suitable for museum display."""
        
        return prompt
    
    def _create_room_prompt(self, room: Dict, topic: str) -> str:
        """Create prompt for room entrance image."""
        room_title = room.get('title', 'Exhibition Room')
        theme = room.get('theme', '')
        description = room.get('description', '')[:200]
        
        prompt = f"""Create a museum gallery room entrance view for "{room_title}".

Theme: {theme}
Context: {topic}
Description: {description}

Style: Professional museum interior photography, warm gallery lighting, elegant display.
Include: Gallery walls, exhibit pedestals, museum atmosphere, welcoming entrance view.
Mood: Sophisticated, educational, inviting, museum-quality.
Perspective: Wide angle entrance view showing the gallery space."""
        
        return prompt
    
    def _create_exhibit_prompt(self, exhibit: Dict, room_theme: str) -> str:
        """Create prompt for individual exhibit image."""
        name = exhibit.get('name', 'Museum Artifact')
        description = exhibit.get('description', '')[:300]
        time_period = exhibit.get('time_period', '')
        
        prompt = f"""Create a museum-quality photograph of: {name}

Description: {description}
Time Period: {time_period}
Context: {room_theme}

Style: Professional museum artifact photography, dramatic lighting, clean background.
Include: Detailed artifact on museum pedestal, museum display aesthetic, professional presentation.
Mood: Educational, authentic, culturally respectful, museum-quality.
Lighting: Dramatic spotlighting with soft shadows, museum gallery lighting."""
        
        return prompt
    
    def _generate_image_with_gemini(self, prompt: str) -> str:
        """Generate image using Gemini's image generation capabilities."""
        try:
            # Generate enhanced description
            image_description = self.generate_with_gemini(
                f"Create a detailed visual description for an AI image generator:\n\n{prompt}\n\nProvide a concise, vivid description optimized for image generation (max 100 words).",
                temperature=0.9
            )
            
            # Option 1: Generate placeholder image URL (for demo)
            # Using a free placeholder service with custom text
            import urllib.parse
            text = prompt.split('\n')[0][:50]  # First line, max 50 chars
            encoded_text = urllib.parse.quote(text)
            placeholder_url = f"https://via.placeholder.com/800x600/8B4513/FFFFFF?text={encoded_text}"
            
            # Return with both description and placeholder
            return {
                'prompt': prompt,
                'enhanced_description': image_description,
                'placeholder_url': placeholder_url,
                'status': 'placeholder_generated',
                'note': 'Using placeholder image. Connect to Imagen/DALL-E for actual AI-generated images'
            }
            
        except Exception as e:
            self.logger.logger.error(f"Image generation error: {e}")
            return {
                'prompt': prompt,
                'status': 'error',
                'error': str(e)
            }
    
    def generate_with_imagen(self, prompt: str) -> str:
        """Generate image using Google Imagen API (requires Vertex AI setup)."""
        # Placeholder for Imagen integration
        # Requires: pip install google-cloud-aiplatform
        """
        from vertexai.preview.vision_models import ImageGenerationModel
        
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        response = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="16:9",
        )
        
        # Save image
        image = response.images[0]
        filename = f"{self.image_dir}/{hash(prompt)}.png"
        image.save(filename)
        return filename
        """
        pass
    
    def generate_with_dalle(self, prompt: str) -> str:
        """Generate image using DALL-E 3 API."""
        # Placeholder for DALL-E integration
        # Requires: pip install openai
        """
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Download and save
        img_data = requests.get(image_url).content
        filename = f"{self.image_dir}/{hash(prompt)}.png"
        with open(filename, 'wb') as f:
            f.write(img_data)
        
        return filename
        """
        pass
