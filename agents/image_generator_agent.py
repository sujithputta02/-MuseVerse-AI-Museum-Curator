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
        """Generate images using Nano Banana (Gemini 2.5 Flash Image model)."""
        try:
            import google.generativeai as genai
            import config
            
            # Configure Gemini with API key
            genai.configure(api_key=config.GOOGLE_API_KEY)
            
            # Use Nano Banana model for image generation
            model = genai.GenerativeModel('gemini-2.5-flash-image')
            
            # Simplify prompt for image generation (Nano Banana has 32K token limit)
            # Extract main subject
            lines = prompt.split('\n')
            main_subject = lines[0] if lines else prompt[:200]
            clean_prompt = main_subject.replace('Create a museum-quality photograph of:', '').strip()
            clean_prompt = clean_prompt.replace('Create a professional museum exhibition poster for', '').strip()
            clean_prompt = clean_prompt.replace('Create a museum gallery room entrance view for', '').strip()
            
            # Keep it concise for better results
            simple_prompt = clean_prompt[:200]
            
            self.logger.logger.info(f"Generating image with Nano Banana: {simple_prompt[:50]}...")
            
            # Generate image using Nano Banana
            response = model.generate_content(simple_prompt)
            
            # Check if response contains image data
            if hasattr(response, 'parts') and response.parts:
                for part in response.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        # Compress and resize image for minimal storage
                        import base64
                        from PIL import Image
                        from io import BytesIO
                        
                        image_data = part.inline_data.data
                        
                        # Open image with PIL
                        original_image = Image.open(BytesIO(image_data))
                        original_size = len(image_data)
                        
                        # Resize to smaller dimensions (max 400x300 for thumbnails)
                        max_width = 400
                        max_height = 300
                        original_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                        
                        # Convert to RGB if necessary (for JPEG)
                        if original_image.mode in ('RGBA', 'LA', 'P'):
                            rgb_image = Image.new('RGB', original_image.size, (255, 255, 255))
                            if original_image.mode == 'P':
                                original_image = original_image.convert('RGBA')
                            rgb_image.paste(original_image, mask=original_image.split()[-1] if original_image.mode == 'RGBA' else None)
                            original_image = rgb_image
                        
                        # Save as compressed JPEG
                        output = BytesIO()
                        original_image.save(output, format='JPEG', quality=70, optimize=True)
                        compressed_data = output.getvalue()
                        
                        # Convert to base64 string
                        image_base64 = base64.b64encode(compressed_data).decode('utf-8')
                        
                        compression_ratio = (1 - len(compressed_data) / original_size) * 100
                        self.logger.logger.info(
                            f"Image compressed: {original_size} -> {len(compressed_data)} bytes "
                            f"({compression_ratio:.1f}% reduction), base64: {len(image_base64)} chars"
                        )
                        
                        return {
                            'prompt': simple_prompt,
                            'image_base64': image_base64,
                            'mime_type': 'image/jpeg',
                            'status': 'generated',
                            'model': 'nano-banana',
                            'size': f'{max_width}x{max_height}',
                            'note': f'Compressed thumbnail ({len(compressed_data)//1024}KB)'
                        }
            
            # If no image in response, log and fallback
            self.logger.logger.warning("Nano Banana did not return image data")
            return {
                'prompt': simple_prompt,
                'status': 'no_image',
                'note': 'Nano Banana did not generate an image'
            }
            
        except Exception as e:
            self.logger.logger.error(f"Nano Banana error: {e}")
            # Fallback to description only
            return {
                'prompt': prompt[:100],
                'status': 'error',
                'error': str(e),
                'note': 'Nano Banana generation failed'
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
