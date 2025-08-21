import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp
import time
from typing import List, Optional

class AIVideoGenerator:
    def __init__(self):
        self.device = "cpu"  # No GPU needed for fallback
        
    async def text_to_video(self, prompt: str, duration: int, style: str) -> mp.VideoFileClip:
        """Generate video from text prompt using fast fallback"""
        print(f"Generating fast video for: {prompt}")
        return await self._create_fallback_video(prompt, duration, style)
    
    async def _create_fallback_video(self, prompt: str, duration: int, style: str) -> mp.VideoFileClip:
        """Create a fast, attractive fallback video with text and animations"""
        
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
        
        def make_frame(t):
            width, height = 1080, 1920
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Animated gradient with style-specific colors
            color1 = colors[0]
            color2 = colors[1]
            
            # Add time-based animation
            wave1 = 0.5 + 0.3 * np.sin(t * 0.8)
            wave2 = 0.5 + 0.3 * np.cos(t * 0.6 + 1)
            
            # Simple gradient without nested loops (faster)
            y_vals = np.linspace(0, 1, height)
            x_vals = np.linspace(0, 1, width)
            Y, X = np.meshgrid(y_vals, x_vals, indexing='ij')
            
            # Animated mixing
            mix = Y * wave1 + X * wave2 * 0.3
            mix = np.clip(mix, 0, 1)
            
            # Apply colors
            frame[:, :, 0] = color1[0] * (1 - mix) + color2[0] * mix
            frame[:, :, 1] = color1[1] * (1 - mix) + color2[1] * mix
            frame[:, :, 2] = color1[2] * (1 - mix) + color2[2] * mix
            
            return frame.astype(np.uint8)
        
        # Create base video
        video = mp.VideoClip(make_frame, duration=duration)
        
        # Skip text overlay for now to avoid ImageMagick dependency
        print(f"Created video for prompt: {prompt}")
        return video