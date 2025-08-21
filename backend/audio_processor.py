import os
import random
import requests
from gtts import gTTS
import moviepy.editor as mp
# from pydub import AudioSegment
# from pydub.generators import Sine, Square
import numpy as np
import time
from typing import Optional, Dict, List
import json

class AudioProcessor:
    def __init__(self):
        self.audio_cache_dir = "temp/audio_cache"
        os.makedirs(self.audio_cache_dir, exist_ok=True)
        
        # Pre-defined audio styles for different content types
        self.style_audio_configs = {
            "trendy": {
                "tempo": "fast",
                "energy": "high",
                "genres": ["electronic", "hip_hop", "pop"],
                "characteristics": ["upbeat", "energetic", "modern"]
            },
            "business": {
                "tempo": "medium",
                "energy": "medium",
                "genres": ["corporate", "ambient", "cinematic"],
                "characteristics": ["professional", "clean", "motivational"]
            },
            "lifestyle": {
                "tempo": "medium",
                "energy": "medium",
                "genres": ["acoustic", "indie", "chill"],
                "characteristics": ["relaxed", "authentic", "warm"]
            },
            "tech": {
                "tempo": "medium-fast",
                "energy": "medium-high",
                "genres": ["electronic", "synthwave", "ambient"],
                "characteristics": ["futuristic", "digital", "innovative"]
            },
            "finance": {
                "tempo": "medium",
                "energy": "medium-high",
                "genres": ["corporate", "electronic", "orchestral"],
                "characteristics": ["serious", "confident", "success-oriented"]
            },
            "fitness": {
                "tempo": "fast",
                "energy": "high",
                "genres": ["electronic", "rock", "hip_hop"],
                "characteristics": ["motivational", "energetic", "powerful"]
            }
        }
    
    async def get_audio_for_style(self, style: str, duration: int) -> mp.AudioFileClip:
        """Get appropriate audio for the given style and duration"""
        
        try:
            # Try to get trending audio first
            audio = await self._get_trending_audio(style, duration)
            
            if audio is None:
                # Fallback to generated audio
                audio = await self._generate_style_audio(style, duration)
            
            return audio
            
        except Exception as e:
            print(f"Error getting audio: {e}")
            # Final fallback: create simple background music
            return await self._create_simple_background_music(duration)
    
    async def _get_trending_audio(self, style: str, duration: int) -> Optional[mp.AudioFileClip]:
        """Try to get trending audio (would integrate with music APIs in production)"""
        
        # In production, this would connect to:
        # - Epidemic Sound API
        # - AudioJungle API
        # - Freesound API
        # - YouTube Audio Library
        
        # For now, we'll use pre-generated audio based on style
        cache_key = f"{style}_{duration}"
        cached_path = os.path.join(self.audio_cache_dir, f"{cache_key}.mp3")
        
        if os.path.exists(cached_path):
            return mp.AudioFileClip(cached_path)
        
        # Generate and cache audio
        audio = await self._generate_style_audio(style, duration)
        if audio:
            # Save to cache
            audio.write_audiofile(cached_path, logger=None)
            return mp.AudioFileClip(cached_path)
        
        return None
    
    async def _generate_style_audio(self, style: str, duration: int) -> mp.AudioFileClip:
        """Generate audio based on style characteristics"""
        
        config = self.style_audio_configs.get(style, self.style_audio_configs["trendy"])
        
        if style == "trendy":
            return await self._create_trendy_beat(duration)
        elif style == "business":
            return await self._create_corporate_music(duration)
        elif style == "lifestyle":
            return await self._create_chill_music(duration)
        elif style == "tech":
            return await self._create_tech_music(duration)
        elif style == "finance":
            return await self._create_finance_music(duration)
        elif style == "fitness":
            return await self._create_workout_music(duration)
        else:
            return await self._create_simple_background_music(duration)
    
    async def _create_trendy_beat(self, duration: int) -> mp.AudioFileClip:
        """Create a trendy upbeat audio track"""
        
        # Create a simple electronic beat pattern
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        # Create kick drum pattern (4/4 beat)
        kick_pattern = np.zeros(samples)
        beat_interval = sample_rate // 2  # 120 BPM
        
        for i in range(0, samples, beat_interval):
            if i + 1000 < samples:
                # Add kick drum sound (low frequency sine wave)
                kick_duration = 1000
                kick_freq = 60
                kick_sound = np.sin(2 * np.pi * kick_freq * np.arange(kick_duration) / sample_rate)
                kick_sound *= np.exp(-np.arange(kick_duration) / 500)  # Decay
                kick_pattern[i:i+kick_duration] += kick_sound * 0.5
        
        # Add hi-hat pattern
        hihat_pattern = np.zeros(samples)
        hihat_interval = sample_rate // 4  # Faster pattern
        
        for i in range(0, samples, hihat_interval):
            if i + 200 < samples:
                # High frequency noise burst
                hihat_duration = 200
                hihat_sound = np.random.normal(0, 0.1, hihat_duration)
                hihat_sound *= np.exp(-np.arange(hihat_duration) / 50)
                hihat_pattern[i:i+hihat_duration] += hihat_sound * 0.2
        
        # Combine patterns
        audio_data = kick_pattern + hihat_pattern
        
        # Normalize
        audio_data = audio_data / np.max(np.abs(audio_data)) * 0.8
        
        # Convert to audio clip
        return self._numpy_to_audio_clip(audio_data, sample_rate)
    
    async def _create_corporate_music(self, duration: int) -> mp.AudioFileClip:
        """Create professional corporate background music"""
        
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        # Create ambient pad sound
        frequencies = [220, 330, 440, 550]  # A minor chord
        audio_data = np.zeros(samples)
        
        for freq in frequencies:
            wave = np.sin(2 * np.pi * freq * np.arange(samples) / sample_rate)
            # Add some gentle modulation
            modulation = 1 + 0.1 * np.sin(2 * np.pi * 0.5 * np.arange(samples) / sample_rate)
            wave *= modulation
            audio_data += wave * 0.15
        
        # Add gentle fade in/out
        fade_samples = sample_rate // 2
        audio_data[:fade_samples] *= np.linspace(0, 1, fade_samples)
        audio_data[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        return self._numpy_to_audio_clip(audio_data, sample_rate)
    
    async def _create_chill_music(self, duration: int) -> mp.AudioFileClip:
        """Create relaxed chill background music"""
        
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        # Create soft acoustic-like sound
        frequencies = [196, 294, 370, 440]  # G major chord
        audio_data = np.zeros(samples)
        
        for i, freq in enumerate(frequencies):
            wave = np.sin(2 * np.pi * freq * np.arange(samples) / sample_rate)
            # Add harmonics for warmth
            wave += 0.3 * np.sin(2 * np.pi * freq * 2 * np.arange(samples) / sample_rate)
            # Gentle tremolo
            tremolo = 1 + 0.05 * np.sin(2 * np.pi * 3 * np.arange(samples) / sample_rate)
            wave *= tremolo
            audio_data += wave * (0.2 - i * 0.02)
        
        # Add gentle fade
        fade_samples = sample_rate
        audio_data[:fade_samples] *= np.linspace(0, 1, fade_samples)
        audio_data[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        return self._numpy_to_audio_clip(audio_data, sample_rate)
    
    async def _create_tech_music(self, duration: int) -> mp.AudioFileClip:
        """Create futuristic tech-style music"""
        
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        # Create digital/synthetic sounds
        audio_data = np.zeros(samples)
        
        # Base frequency sweep
        start_freq = 80
        end_freq = 160
        frequencies = np.linspace(start_freq, end_freq, samples)
        base_wave = np.sin(2 * np.pi * frequencies * np.arange(samples) / sample_rate)
        audio_data += base_wave * 0.3
        
        # Add digital arpeggios
        arp_freqs = [220, 277, 330, 415]  # A minor arpeggio
        for i, freq in enumerate(arp_freqs):
            start_sample = i * samples // 4
            end_sample = (i + 1) * samples // 4
            if end_sample <= samples:
                arp_wave = np.sin(2 * np.pi * freq * np.arange(end_sample - start_sample) / sample_rate)
                # Square wave for digital feel
                arp_wave = np.sign(arp_wave) * 0.2
                audio_data[start_sample:end_sample] += arp_wave
        
        return self._numpy_to_audio_clip(audio_data, sample_rate)
    
    async def _create_finance_music(self, duration: int) -> mp.AudioFileClip:
        """Create serious finance/business music"""
        
        # Similar to corporate but with more intensity
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        # Create building orchestral-like sound
        frequencies = [110, 165, 220, 275]  # A minor
        audio_data = np.zeros(samples)
        
        for i, freq in enumerate(frequencies):
            wave = np.sin(2 * np.pi * freq * np.arange(samples) / sample_rate)
            # Add building intensity
            intensity = np.linspace(0.1, 0.5, samples)
            wave *= intensity
            audio_data += wave * (0.25 - i * 0.03)
        
        # Add some percussion-like elements
        beat_interval = sample_rate
        for i in range(0, samples, beat_interval):
            if i + 500 < samples:
                beat_sound = np.sin(2 * np.pi * 100 * np.arange(500) / sample_rate)
                beat_sound *= np.exp(-np.arange(500) / 200)
                audio_data[i:i+500] += beat_sound * 0.3
        
        return self._numpy_to_audio_clip(audio_data, sample_rate)
    
    async def _create_workout_music(self, duration: int) -> mp.AudioFileClip:
        """Create energetic workout music"""
        
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        # Create driving beat
        audio_data = np.zeros(samples)
        
        # Strong kick pattern
        kick_interval = sample_rate // 2  # 120 BPM
        for i in range(0, samples, kick_interval):
            if i + 800 < samples:
                kick_sound = np.sin(2 * np.pi * 50 * np.arange(800) / sample_rate)
                kick_sound *= np.exp(-np.arange(800) / 300)
                audio_data[i:i+800] += kick_sound * 0.6
        
        # Add energetic synth line
        synth_freq = 440
        synth_wave = np.sin(2 * np.pi * synth_freq * np.arange(samples) / sample_rate)
        # Add filter sweep for energy
        filter_sweep = np.linspace(0.1, 0.4, samples)
        synth_wave *= filter_sweep
        audio_data += synth_wave * 0.3
        
        return self._numpy_to_audio_clip(audio_data, sample_rate)
    
    async def _create_simple_background_music(self, duration: int) -> mp.AudioFileClip:
        """Create simple background music as fallback"""
        
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        # Simple chord progression
        frequencies = [262, 330, 392]  # C major chord
        audio_data = np.zeros(samples)
        
        for freq in frequencies:
            wave = np.sin(2 * np.pi * freq * np.arange(samples) / sample_rate)
            audio_data += wave * 0.2
        
        # Add fade in/out
        fade_samples = sample_rate // 4
        audio_data[:fade_samples] *= np.linspace(0, 1, fade_samples)
        audio_data[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        return self._numpy_to_audio_clip(audio_data, sample_rate)
    
    def _numpy_to_audio_clip(self, audio_data: np.ndarray, sample_rate: int) -> mp.AudioFileClip:
        """Convert numpy array to MoviePy AudioClip"""
        
        # Ensure audio is in correct format
        audio_data = np.clip(audio_data, -1, 1)
        
        # Create temporary file
        temp_path = f"temp/generated_audio_{int(time.time())}.wav"
        
        # Create a simple wav file manually for now
        import wave
        
        # Convert to 16-bit PCM
        audio_16bit = (audio_data * 32767).astype(np.int16)
        
        with wave.open(temp_path, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_16bit.tobytes())
        
        # Return as MoviePy clip
        return mp.AudioFileClip(temp_path)
    
    async def generate_voiceover(self, text: str, language: str = "en") -> mp.AudioFileClip:
        """Generate voiceover from text using TTS"""
        
        try:
            # Generate speech using gTTS
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Save to temporary file
            temp_path = f"temp/voiceover_{int(time.time())}.mp3"
            tts.save(temp_path)
            
            return mp.AudioFileClip(temp_path)
            
        except Exception as e:
            print(f"Error generating voiceover: {e}")
            return None
    
    async def add_audio_effects(self, audio_clip: mp.AudioFileClip, style: str) -> mp.AudioFileClip:
        """Add audio effects based on style"""
        
        try:
            if style == "trendy":
                # Add some reverb effect (simplified)
                return audio_clip.fx(mp.afx.audio_fadein, 0.5).fx(mp.afx.audio_fadeout, 0.5)
            elif style == "business":
                # Clean, professional sound
                return audio_clip.fx(mp.afx.audio_normalize)
            else:
                return audio_clip
                
        except Exception as e:
            print(f"Error adding audio effects: {e}")
            return audio_clip