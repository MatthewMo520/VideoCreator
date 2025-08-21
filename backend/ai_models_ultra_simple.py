import os
import numpy as np
from PIL import Image, ImageDraw
import moviepy.editor as mp
import time
from typing import List, Optional

class AIVideoGenerator:
    def __init__(self):
        self.device = "cpu"
        
    async def text_to_video(self, prompt: str, duration: int, style: str) -> mp.VideoFileClip:
        """Generate video from text prompt using ultra simple method"""
        print(f"Generating ultra simple video for: {prompt}")
        return await self._create_simple_image_video(prompt, duration, style)
    
    async def _create_simple_image_video(self, prompt: str, duration: int, style: str) -> mp.VideoFileClip:
        """Create video from static images instead of animated frames"""
        
        # Style-specific color schemes
        style_colors = {
            'trendy': [(255, 20, 147), (138, 43, 226)],  # Pink to Purple
            'business': [(30, 144, 255), (0, 191, 255)],  # Blue gradient
            'lifestyle': [(50, 205, 50), (0, 250, 154)],  # Green gradient
            'tech': [(148, 0, 211), (75, 0, 130)],  # Purple gradient
            'finance': [(255, 215, 0), (255, 140, 0)],  # Gold gradient
            'fitness': [(220, 20, 60), (255, 69, 0)]  # Red gradient
        }
        
        colors = style_colors.get(style, style_colors['trendy'])
        
        # Create a simple gradient image
        width, height = 1080, 1920
        image = Image.new('RGB', (width, height))
        
        # Create gradient
        for y in range(height):
            ratio = y / height
            r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
            
            for x in range(width):
                image.putpixel((x, y), (r, g, b))
        
        # Save the image
        timestamp = int(time.time())
        os.makedirs("../temp", exist_ok=True)
        image_path = f"../temp/gradient_{timestamp}.jpg"
        image.save(image_path)
        
        # Create video clip from the static image
        video = mp.ImageClip(image_path, duration=duration)
        
        return video