import os
import time
import numpy as np
import moviepy.editor as mp
from typing import Optional, Dict, List

class SimpleVideoGenerator:
    def __init__(self):
        pass
    
    async def generate_reel(
        self,
        prompt: str,
        style: str = "trendy",
        duration: int = 15,
        image_paths: List[str] = [],
        audio_path: Optional[str] = None,
        trending_data: Optional[Dict] = None
    ) -> str:
        """Generate a simple reel video without complex dependencies"""
        
        timestamp = int(time.time())
        output_filename = f"reel_{timestamp}.mp4"
        output_path = f"../outputs/{output_filename}"
        
        try:
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
                
                # Animated gradient with multiple effects
                color1 = colors[0]
                color2 = colors[1]
                
                # Multiple wave animations for more dynamic effect
                wave1 = 0.5 + 0.3 * np.sin(t * 1.5)
                wave2 = 0.5 + 0.2 * np.cos(t * 2.3 + 1)
                wave3 = 0.5 + 0.1 * np.sin(t * 0.8 + 3)
                
                # Create gradient using numpy operations (faster)
                y_vals = np.linspace(0, 1, height)
                x_vals = np.linspace(0, 1, width)
                Y, X = np.meshgrid(y_vals, x_vals, indexing='ij')
                
                # Complex gradient mixing with radial and linear components
                linear_gradient = Y
                radial_gradient = np.sqrt((X - 0.5)**2 + (Y - 0.5)**2)
                
                # Combine gradients with animation
                mix = (linear_gradient * wave1 + radial_gradient * wave2) * wave3
                mix = np.clip(mix, 0, 1)
                
                # Add some noise for texture
                noise = np.random.random((height, width)) * 0.05
                mix = np.clip(mix + noise, 0, 1)
                
                frame[:, :, 0] = color1[0] * (1 - mix) + color2[0] * mix
                frame[:, :, 1] = color1[1] * (1 - mix) + color2[1] * mix
                frame[:, :, 2] = color1[2] * (1 - mix) + color2[2] * mix
                
                return frame.astype(np.uint8)
            
            # Create video
            video = mp.VideoClip(make_frame, duration=duration)
            
            # Try to add text overlay
            try:
                # Split prompt into words for better display
                words = prompt.split()
                if len(words) > 6:
                    # Split into two lines
                    mid = len(words) // 2
                    line1 = ' '.join(words[:mid])
                    line2 = ' '.join(words[mid:])
                    display_text = f"{line1}\n{line2}"
                else:
                    display_text = prompt
                
                # Create text clip - try without complex settings first
                text_clip = mp.TextClip(
                    display_text.upper(),
                    fontsize=80,
                    color='white',
                    font='Arial-Bold'
                ).set_position('center').set_duration(duration)
                
                # Composite video with text
                final_video = mp.CompositeVideoClip([video, text_clip])
                print(f"Added text overlay: {display_text}")
                
            except Exception as e:
                print(f"Text overlay failed: {e}, using video without text")
                final_video = video
            
            # Add background music
            try:
                audio_clip = self._generate_background_music(style, duration)
                final_video = final_video.set_audio(audio_clip)
                print(f"Added background music for style: {style}")
            except Exception as e:
                print(f"Audio generation failed: {e}, using video without audio")
            
            # Write video with minimal settings
            print(f"Writing video to: {output_path}")
            final_video.write_videofile(
                output_path,
                fps=15,
                codec='libx264',
                verbose=False,
                logger=None
            )
            
            print(f"Video created successfully: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error generating reel: {e}")
            raise e
    
    def _generate_background_music(self, style: str, duration: int) -> mp.AudioClip:
        """Generate background music based on style"""
        import wave
        
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        # Style-specific music characteristics
        if style == 'trendy':
            # Upbeat electronic-style music
            audio = self._create_electronic_beat(samples, sample_rate)
        elif style == 'business':
            # Professional ambient music
            audio = self._create_ambient_music(samples, sample_rate)
        elif style == 'fitness':
            # High-energy workout music
            audio = self._create_workout_beat(samples, sample_rate)
        else:
            # Default chill music
            audio = self._create_chill_music(samples, sample_rate)
        
        # Save as temporary audio file
        timestamp = int(time.time())
        audio_path = f"../temp/audio_{timestamp}.wav"
        os.makedirs("../temp", exist_ok=True)
        
        # Convert to 16-bit PCM and save
        audio_16bit = (audio * 32767).astype(np.int16)
        
        with wave.open(audio_path, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_16bit.tobytes())
        
        return mp.AudioFileClip(audio_path)
    
    def _create_electronic_beat(self, samples: int, sample_rate: int) -> np.ndarray:
        """Create upbeat electronic music"""
        audio = np.zeros(samples)
        
        # Create kick drum pattern
        kick_interval = sample_rate // 2  # 120 BPM
        for i in range(0, samples, kick_interval):
            if i + 1000 < samples:
                kick_sound = np.sin(2 * np.pi * 60 * np.arange(1000) / sample_rate)
                kick_sound *= np.exp(-np.arange(1000) / 300)
                audio[i:i+1000] += kick_sound * 0.4
        
        # Add synth melody
        melody_freqs = [440, 523, 659, 784]  # A, C, E, G
        for i, freq in enumerate(melody_freqs):
            start = i * samples // 4
            end = (i + 1) * samples // 4
            if end <= samples:
                melody = np.sin(2 * np.pi * freq * np.arange(end - start) / sample_rate)
                audio[start:end] += melody * 0.2
        
        return np.clip(audio, -1, 1)
    
    def _create_ambient_music(self, samples: int, sample_rate: int) -> np.ndarray:
        """Create professional ambient music"""
        audio = np.zeros(samples)
        
        # Create ambient pad with multiple harmonics
        base_freq = 220  # A3
        for harmonic in [1, 0.5, 0.25]:
            freq = base_freq * harmonic
            wave = np.sin(2 * np.pi * freq * np.arange(samples) / sample_rate)
            # Add gentle modulation
            modulation = 1 + 0.1 * np.sin(2 * np.pi * 0.3 * np.arange(samples) / sample_rate)
            audio += wave * modulation * 0.15
        
        # Add gentle fade in/out
        fade_samples = sample_rate
        audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
        audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        return np.clip(audio, -1, 1)
    
    def _create_workout_beat(self, samples: int, sample_rate: int) -> np.ndarray:
        """Create high-energy workout music"""
        audio = np.zeros(samples)
        
        # Strong kick pattern
        kick_interval = sample_rate // 3  # 180 BPM - high energy
        for i in range(0, samples, kick_interval):
            if i + 800 < samples:
                kick_sound = np.sin(2 * np.pi * 50 * np.arange(800) / sample_rate)
                kick_sound *= np.exp(-np.arange(800) / 200)
                audio[i:i+800] += kick_sound * 0.5
        
        # Add driving synth line
        synth_freq = 440
        synth_wave = np.sin(2 * np.pi * synth_freq * np.arange(samples) / sample_rate)
        filter_sweep = np.linspace(0.2, 0.5, samples)
        audio += synth_wave * filter_sweep * 0.3
        
        return np.clip(audio, -1, 1)
    
    def _create_chill_music(self, samples: int, sample_rate: int) -> np.ndarray:
        """Create relaxed chill music"""
        audio = np.zeros(samples)
        
        # Create soft chord progression
        chord_freqs = [196, 294, 370, 440]  # G major chord
        for i, freq in enumerate(chord_freqs):
            wave = np.sin(2 * np.pi * freq * np.arange(samples) / sample_rate)
            # Add harmonics for warmth
            wave += 0.3 * np.sin(2 * np.pi * freq * 2 * np.arange(samples) / sample_rate)
            audio += wave * (0.15 - i * 0.02)
        
        return np.clip(audio, -1, 1)