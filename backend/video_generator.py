import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import random
import time
from typing import List, Optional, Dict
import json

from ai_models_ultra_simple import AIVideoGenerator
from audio_processor import AudioProcessor
from text_overlay import TextOverlay

class VideoGenerator:
    def __init__(self):
        self.ai_generator = AIVideoGenerator()
        self.audio_processor = AudioProcessor()
        self.text_overlay = TextOverlay()
        
        # Ensure output directory exists
        os.makedirs("outputs", exist_ok=True)
        os.makedirs("temp", exist_ok=True)
    
    async def generate_reel(
        self,
        prompt: str,
        style: str = "trendy",
        duration: int = 15,
        image_paths: List[str] = [],
        audio_path: Optional[str] = None,
        trending_data: Optional[Dict] = None
    ) -> str:
        """Generate a complete reel video"""
        
        timestamp = int(time.time())
        output_filename = f"reel_{timestamp}.mp4"
        output_path = f"../outputs/{output_filename}"
        
        try:
            # Step 1: Generate base video content
            if image_paths:
                # Create video from images
                base_video = await self._create_video_from_images(
                    image_paths, duration, style
                )
            else:
                # Generate AI video from prompt
                base_video = await self.ai_generator.text_to_video(
                    prompt, duration, style
                )
            
            # Step 2: Skip text overlays for now (ImageMagick dependency)
            video_with_text = base_video
            
            # Step 3: Skip audio for now to avoid issues
            final_video = video_with_text
            
            # Step 4: Skip style effects for now
            styled_video = final_video
            
            # Step 5: Export final video
            styled_video.write_videofile(
                output_path,
                fps=15,  # Lower FPS for faster processing
                codec='libx264',
                verbose=False,
                logger=None
            )
            
            return output_path
            
        except Exception as e:
            print(f"Error generating reel: {e}")
            raise e
    
    async def _create_video_from_images(
        self, image_paths: List[str], duration: int, style: str
    ) -> VideoFileClip:
        """Create video from uploaded images"""
        
        clips = []
        duration_per_image = duration / len(image_paths)
        
        for i, img_path in enumerate(image_paths):
            # Load and resize image
            img = Image.open(img_path)
            
            # Convert to 9:16 aspect ratio (1080x1920)
            img_resized = self._resize_to_reel_format(img)
            
            # Save temp image
            temp_img_path = f"temp/temp_img_{i}.jpg"
            img_resized.save(temp_img_path)
            
            # Create video clip from image
            clip = mp.ImageClip(temp_img_path, duration=duration_per_image)
            
            # Add zoom effect based on style
            if style == "trendy":
                clip = clip.resize(lambda t: 1 + 0.1 * t)  # Slow zoom
            elif style == "business":
                clip = clip.crossfadein(0.5).crossfadeout(0.5)
            
            clips.append(clip)
        
        # Concatenate all clips
        final_clip = mp.concatenate_videoclips(clips)
        return final_clip
    
    def _resize_to_reel_format(self, img: Image.Image) -> Image.Image:
        """Resize image to 9:16 aspect ratio (1080x1920)"""
        target_width, target_height = 1080, 1920
        
        # Calculate scaling to fit image within target dimensions
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height
        
        if img_ratio > target_ratio:
            # Image is wider, scale by height
            new_height = target_height
            new_width = int(new_height * img_ratio)
        else:
            # Image is taller, scale by width
            new_width = target_width
            new_height = int(new_width / img_ratio)
        
        # Resize image
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create black background
        background = Image.new('RGB', (target_width, target_height), (0, 0, 0))
        
        # Center the image on the background
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        background.paste(img_resized, (x_offset, y_offset))
        
        return background
    
    async def _add_text_overlays(
        self, video: VideoFileClip, prompt: str, style: str, trending_data: Optional[Dict]
    ) -> VideoFileClip:
        """Add text overlays to video"""
        
        # Generate text based on prompt and trending data
        overlay_texts = self.text_overlay.generate_overlay_texts(
            prompt, style, trending_data
        )
        
        text_clips = []
        
        for i, text_data in enumerate(overlay_texts):
            text_clip = TextClip(
                text_data['text'],
                fontsize=text_data.get('fontsize', 60),
                color=text_data.get('color', 'white'),
                font=text_data.get('font', 'Arial-Bold'),
                stroke_color=text_data.get('stroke_color', 'black'),
                stroke_width=text_data.get('stroke_width', 2)
            ).set_position(text_data.get('position', 'center')).set_duration(
                text_data.get('duration', 3)
            ).set_start(text_data.get('start', i * 2))
            
            text_clips.append(text_clip)
        
        # Composite video with text
        final_video = CompositeVideoClip([video] + text_clips)
        return final_video
    
    async def _add_audio(
        self, video: VideoFileClip, audio_path: Optional[str], duration: int, style: str
    ) -> VideoFileClip:
        """Add audio to video"""
        
        if audio_path and os.path.exists(audio_path):
            # Use uploaded audio
            audio = AudioFileClip(audio_path)
        else:
            # Generate or select trending audio
            audio = await self.audio_processor.get_audio_for_style(style, duration)
        
        # Trim audio to video duration
        if audio.duration > duration:
            audio = audio.subclip(0, duration)
        elif audio.duration < duration:
            # Loop audio if it's shorter
            loops = int(duration / audio.duration) + 1
            audio = mp.concatenate_audioclips([audio] * loops).subclip(0, duration)
        
        # Set audio to video
        video_with_audio = video.set_audio(audio)
        return video_with_audio
    
    async def _apply_style_effects(
        self, video: VideoFileClip, style: str, trending_data: Optional[Dict]
    ) -> VideoFileClip:
        """Apply style-specific effects to video"""
        
        if style == "trendy":
            # Add quick cuts and zoom effects
            video = self._add_trendy_effects(video, trending_data)
        elif style == "business":
            # Add professional transitions
            video = self._add_business_effects(video)
        elif style == "finance":
            # Add stock market style effects
            video = self._add_finance_effects(video)
        
        return video
    
    def _add_trendy_effects(self, video: VideoFileClip, trending_data: Optional[Dict]) -> VideoFileClip:
        """Add trendy effects like quick cuts, zooms"""
        
        # Add subtle zoom effect throughout
        zoom_factor = 1.1
        video = video.resize(lambda t: 1 + (zoom_factor - 1) * t / video.duration)
        
        # Add flash transitions if trending data suggests it
        if trending_data and trending_data.get('effects', {}).get('flash_transitions'):
            # Implementation would add flash effects at beat points
            pass
        
        return video
    
    def _add_business_effects(self, video: VideoFileClip) -> VideoFileClip:
        """Add professional business-style effects"""
        
        # Add subtle fade effects
        video = video.crossfadein(0.5).crossfadeout(0.5)
        
        return video
    
    def _add_finance_effects(self, video: VideoFileClip) -> VideoFileClip:
        """Add finance/stock market style effects"""
        
        # Could add stock ticker overlay, chart animations, etc.
        return video