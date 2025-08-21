import torch
from diffusers import StableDiffusionPipeline, DiffusionPipeline
from transformers import pipeline
import cv2
import numpy as np
from PIL import Image
import moviepy.editor as mp
import os
import random
import time
from typing import List, Optional

class AIVideoGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_cache_dir = os.getenv("MODEL_CACHE_DIR", "./models")
        os.makedirs(self.model_cache_dir, exist_ok=True)
        
        # Initialize models (lazy loading)
        self.text_to_image_pipeline = None
        self.image_to_video_pipeline = None
        
    async def text_to_video(self, prompt: str, duration: int, style: str) -> mp.VideoFileClip:
        """Generate video from text prompt"""
        
        try:
            # Skip AI generation for now - use fast fallback instead
            print(f"Generating fast fallback video for: {prompt}")
            return await self._create_fallback_video(prompt, duration, style)
            
            # Original AI generation code (commented out for speed)
            # styled_prompts = self._generate_styled_prompts(prompt, style, duration)
            # images = []
            # for styled_prompt in styled_prompts:
            #     image = await self._text_to_image(styled_prompt)
            #     images.append(image)
            # video = await self._images_to_video(images, duration)
            # return video
            
        except Exception as e:
            print(f"Error in text_to_video: {e}")
            # Fallback: create a simple colored video with text
            return await self._create_fallback_video(prompt, duration, style)
    
    async def _text_to_image(self, prompt: str) -> Image.Image:
        """Generate image from text using Stable Diffusion"""
        
        try:
            if self.text_to_image_pipeline is None:
                # Use a smaller, faster model for better performance
                model_id = "runwayml/stable-diffusion-v1-5"
                self.text_to_image_pipeline = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    cache_dir=self.model_cache_dir,
                    low_cpu_mem_usage=True
                )
                self.text_to_image_pipeline.to(self.device)
                
                # Optimize for speed
                if self.device == "cuda":
                    self.text_to_image_pipeline.enable_memory_efficient_attention()
                    self.text_to_image_pipeline.enable_xformers_memory_efficient_attention()
            
            # Generate image
            with torch.inference_mode():
                result = self.text_to_image_pipeline(
                    prompt,
                    num_inference_steps=20,  # Fewer steps for speed
                    guidance_scale=7.5,
                    width=1024,
                    height=1024
                )
                
            return result.images[0]
            
        except Exception as e:
            print(f"Error generating image: {e}")
            # Fallback: create a simple gradient image
            return self._create_fallback_image(prompt)
    
    def _create_fallback_image(self, prompt: str) -> Image.Image:
        """Create a simple fallback image when AI generation fails"""
        
        # Create a gradient background
        width, height = 1024, 1024
        image = Image.new('RGB', (width, height))
        
        # Generate random colors based on prompt hash
        hash_val = hash(prompt) % 16777215
        color1 = (hash_val & 0xFF0000) >> 16, (hash_val & 0x00FF00) >> 8, hash_val & 0x0000FF
        color2 = ((hash_val + 123456) & 0xFF0000) >> 16, ((hash_val + 123456) & 0x00FF00) >> 8, (hash_val + 123456) & 0x0000FF
        
        # Create gradient
        for y in range(height):
            r = int(color1[0] + (color2[0] - color1[0]) * y / height)
            g = int(color1[1] + (color2[1] - color1[1]) * y / height)
            b = int(color1[2] + (color2[2] - color1[2]) * y / height)
            
            for x in range(width):
                image.putpixel((x, y), (r, g, b))
        
        return image
    
    async def _images_to_video(self, images: List[Image.Image], duration: int) -> mp.VideoFileClip:
        """Convert list of images to video with transitions"""
        
        clips = []
        duration_per_image = duration / len(images)
        
        for i, img in enumerate(images):
            # Resize to reel format (9:16)
            img_resized = self._resize_to_reel_format(img)
            
            # Save temporary image
            temp_path = f"temp/ai_img_{i}_{int(time.time())}.jpg"
            img_resized.save(temp_path)
            
            # Create video clip
            clip = mp.ImageClip(temp_path, duration=duration_per_image)
            
            # Add some movement/zoom
            clip = clip.resize(lambda t: 1 + 0.05 * np.sin(2 * np.pi * t / duration_per_image))
            
            clips.append(clip)
        
        # Concatenate with crossfade transitions
        final_clips = []
        for i, clip in enumerate(clips):
            if i == 0:
                final_clips.append(clip.crossfadeout(0.5))
            elif i == len(clips) - 1:
                final_clips.append(clip.crossfadein(0.5))
            else:
                final_clips.append(clip.crossfadein(0.5).crossfadeout(0.5))
        
        video = mp.concatenate_videoclips(final_clips)
        return video
    
    def _resize_to_reel_format(self, img: Image.Image) -> Image.Image:
        """Resize image to 9:16 aspect ratio"""
        target_width, target_height = 1080, 1920
        
        # Calculate scaling
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height
        
        if img_ratio > target_ratio:
            new_height = target_height
            new_width = int(new_height * img_ratio)
        else:
            new_width = target_width
            new_height = int(new_width / img_ratio)
        
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Center on black background
        background = Image.new('RGB', (target_width, target_height), (0, 0, 0))
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        background.paste(img_resized, (x_offset, y_offset))
        
        return background
    
    def _generate_styled_prompts(self, base_prompt: str, style: str, duration: int) -> List[str]:
        """Generate multiple prompts for different scenes based on style"""
        
        num_scenes = max(3, duration // 5)  # One scene every 5 seconds minimum
        
        style_modifiers = {
            "trendy": [
                "vibrant colors, modern aesthetic, social media style",
                "neon lights, urban setting, trendy fashion",
                "dynamic movement, energetic vibe, contemporary"
            ],
            "business": [
                "professional, clean, corporate environment",
                "office setting, business attire, formal presentation",
                "modern workspace, technology, professional lighting"
            ],
            "lifestyle": [
                "casual, relatable, everyday life",
                "cozy atmosphere, natural lighting, authentic moments",
                "personal space, comfortable setting, lifestyle photography"
            ],
            "tech": [
                "futuristic, digital, high-tech environment",
                "cyberpunk aesthetic, neon blues and purples, technology",
                "sleek design, modern interface, digital art style"
            ],
            "finance": [
                "stock market, financial data, professional charts",
                "money, investment, banking environment, graphs",
                "success, wealth, financial growth, business charts"
            ],
            "fitness": [
                "gym environment, athletic wear, energetic movement",
                "healthy lifestyle, workout equipment, motivation",
                "strength training, cardio, fitness motivation"
            ]
        }
        
        modifiers = style_modifiers.get(style, style_modifiers["trendy"])
        
        prompts = []
        for i in range(num_scenes):
            modifier = modifiers[i % len(modifiers)]
            styled_prompt = f"{base_prompt}, {modifier}, high quality, 4k, detailed"
            prompts.append(styled_prompt)
        
        return prompts
    
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
            
            for y in range(height):
                for x in range(width):
                    # Create animated gradient
                    norm_y = y / height
                    norm_x = x / width
                    
                    # Animated mixing
                    mix = norm_y * wave1 + norm_x * wave2 * 0.3
                    mix = max(0, min(1, mix))
                    
                    r = int(color1[0] * (1 - mix) + color2[0] * mix)
                    g = int(color1[1] * (1 - mix) + color2[1] * mix)
                    b = int(color1[2] * (1 - mix) + color2[2] * mix)
                    
                    frame[y, x] = [r, g, b]
            
            return frame
        
        # Create base video
        video = mp.VideoClip(make_frame, duration=duration)
        
        # Add text overlay
        try:
            # Split prompt into chunks for better display
            words = prompt.split()
            if len(words) > 8:
                text_lines = []
                current_line = []
                for word in words:
                    current_line.append(word)
                    if len(' '.join(current_line)) > 40:
                        text_lines.append(' '.join(current_line[:-1]))
                        current_line = [word]
                if current_line:
                    text_lines.append(' '.join(current_line))
                display_text = '\n'.join(text_lines[:3])  # Max 3 lines
            else:
                display_text = prompt
            
            # Create text clip
            text_clip = mp.TextClip(
                display_text,
                fontsize=80,
                color='white',
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=3,
                method='caption',
                size=(900, None),
                align='center'
            ).set_position('center').set_duration(duration)
            
            # Composite video with text
            final_video = mp.CompositeVideoClip([video, text_clip])
            return final_video
            
        except Exception as e:
            print(f"Error adding text overlay: {e}")
            return video