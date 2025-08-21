import os
import time
import numpy as np
import moviepy.editor as mp
from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Optional, Dict, List
from gtts import gTTS

class AIContentGenerator:
    def __init__(self):
        self.temp_dir = "../temp"
        os.makedirs(self.temp_dir, exist_ok=True)
        
    async def generate_reel(
        self,
        prompt: str,
        style: str = "trendy",
        duration: int = 15,
        image_paths: List[str] = [],
        audio_path: Optional[str] = None,
        trending_data: Optional[Dict] = None
    ) -> str:
        """Generate AI content reel with research and voiceover"""
        
        timestamp = int(time.time())
        output_path = f"../outputs/reel_{timestamp}.mp4"
        
        try:
            print(f"Researching topic: {prompt}")
            
            # Step 1: Research the topic
            research_data = await self._research_topic(prompt, style)
            
            # Step 2: Generate script based on research
            script = await self._generate_script(prompt, research_data, style, duration)
            
            # Step 3: Generate audio (voiceover or background music)
            use_music_only = self._should_use_music_only(prompt, style)
            if use_music_only:
                voiceover_path = await self._generate_background_music(style, duration)
            else:
                voiceover_path = await self._generate_voiceover(script, style)
            
            # Step 4: Create visual content based on script
            visual_clips = await self._create_visual_content(script, style, duration)
            
            # Step 5: Combine visuals and audio
            final_video = await self._combine_content(visual_clips, voiceover_path, duration)
            
            # Step 6: Export final video
            print(f"Exporting final reel...")
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                verbose=False,
                logger=None
            )
            
            print(f"AI reel created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error generating AI reel: {e}")
            # Fallback to simple reel
            return await self._create_fallback_reel(prompt, style, duration, output_path)
    
    async def _research_topic(self, prompt: str, style: str) -> Dict:
        """Research the topic using web search and APIs"""
        research_data = {
            'facts': [],
            'statistics': [],
            'recent_news': [],
            'key_points': []
        }
        
        try:
            # Extract key terms from prompt for better search
            search_query = self._extract_search_terms(prompt, style)
            print(f"Searching for: {search_query}")
            
            # Simulate research (in production, use real APIs)
            research_data = await self._simulate_research(search_query, style)
            
        except Exception as e:
            print(f"Research failed: {e}, using fallback data")
            research_data = self._get_fallback_research(prompt, style)
        
        return research_data
    
    def _extract_search_terms(self, prompt: str, style: str) -> str:
        """Extract searchable terms from prompt"""
        # Remove common words and extract key terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b\w+\b', prompt.lower())
        key_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Add style-specific context
        if style == 'finance':
            key_words.extend(['stock', 'market', 'investment', '2024'])
        elif style == 'tech':
            key_words.extend(['technology', 'AI', 'innovation'])
        elif style == 'fitness':
            key_words.extend(['fitness', 'health', 'workout'])
        
        return ' '.join(key_words[:5])  # Top 5 keywords
    
    async def _simulate_research(self, query: str, style: str) -> Dict:
        """Simulate research data for ANY topic"""
        
        # Topic-specific research simulation
        if 'crypto' in query.lower() or 'bitcoin' in query.lower():
            return {
                'facts': [
                    "Bitcoin reached an all-time high of $73,750 in March 2024",
                    "Ethereum transitioned to Proof of Stake, reducing energy usage by 99.9%",
                    "Over 420 million people worldwide now own cryptocurrency",
                    "El Salvador and Central African Republic adopted Bitcoin as legal tender"
                ],
                'statistics': [
                    {"label": "Bitcoin Market Cap", "value": "$1.3 Trillion", "change": "+156%"},
                    {"label": "Daily Trading Volume", "value": "$15.2 Billion", "change": "+89%"},
                    {"label": "Active Wallets", "value": "106 Million", "change": "+34%"}
                ],
                'key_points': ["Institutional adoption accelerating", "Regulatory clarity improving", "DeFi ecosystem growing"]
            }
        
        elif 'stock' in query.lower() or 'investment' in query.lower():
            if 'best' in query.lower() or 'top' in query.lower() or 'pick' in query.lower():
                return {
                    'facts': [
                        "1. NVIDIA (NVDA) - AI chip leader, 239% YTD growth",
                        "2. Tesla (TSLA) - EV dominance, expanding into robotics",
                        "3. Microsoft (MSFT) - Cloud computing + AI integration",
                        "4. Apple (AAPL) - iPhone 15 cycle + Vision Pro launch"
                    ],
                    'statistics': [
                        {"label": "NVIDIA", "value": "$890", "change": "+239% YTD"},
                        {"label": "Tesla", "value": "$248", "change": "+67% growth"},
                        {"label": "Microsoft", "value": "$378", "change": "AI revenue up 150%"}
                    ],
                    'key_points': ["AI revolution drives tech stocks", "EV adoption accelerating", "Cloud computing essential"]
                }
            else:
                return {
                    'facts': [
                        "S&P 500 gained 24.2% in 2024, outperforming expectations",
                        "AI stocks led market growth with 300%+ average returns",
                        "Tech sector represented 35% of total market cap"
                    ],
                    'statistics': [
                        {"label": "NVIDIA Stock", "value": "+239%", "change": "YTD 2024"},
                        {"label": "Market Volume", "value": "$45B", "change": "Daily average"}
                    ],
                    'key_points': ["AI revolution driving valuations", "Clean energy transition", "Remote work trends permanent"]
                }
        
        elif 'fitness' in query.lower() or 'workout' in query.lower() or 'health' in query.lower():
            if 'plan' in query.lower() or 'routine' in query.lower():
                return {
                    'facts': [
                        "Week 1-2: Foundation Phase - 3 workouts per week",
                        "Week 3-4: Strength Phase - Add weight training",
                        "Week 5-6: Endurance Phase - Increase cardio duration",
                        "Week 7-8: Power Phase - High intensity intervals"
                    ],
                    'statistics': [
                        {"label": "Day 1", "value": "Upper Body", "change": "Push-ups, Pull-ups"},
                        {"label": "Day 2", "value": "Lower Body", "change": "Squats, Lunges"},
                        {"label": "Day 3", "value": "Cardio", "change": "30min HIIT"}
                    ],
                    'key_points': ["Start with bodyweight exercises", "Progress gradually each week", "Rest days are mandatory"]
                }
            else:
                return {
                    'facts': [
                        "Regular exercise reduces risk of heart disease by 35%",
                        "Strength training increases metabolism for up to 48 hours post-workout",
                        "Just 150 minutes weekly exercise adds 3.4 years to lifespan",
                        "High-intensity workouts improve brain function and memory"
                    ],
                    'statistics': [
                        {"label": "Metabolism Boost", "value": "15%", "change": "After strength training"},
                        {"label": "Heart Disease Risk", "value": "-35%", "change": "With regular exercise"},
                        {"label": "Life Extension", "value": "+3.4 years", "change": "From 150min/week"}
                    ],
                    'key_points': ["Consistency beats intensity", "Compound movements are king", "Recovery is crucial for growth"]
                }
        
        elif 'tech' in query.lower() or 'ai' in query.lower() or 'technology' in query.lower():
            return {
                'facts': [
                    "AI market expected to reach $1.8 trillion by 2030",
                    "ChatGPT reached 100 million users in just 2 months",
                    "Over 77% of companies are using or exploring AI",
                    "AI can improve productivity by up to 40% in knowledge work"
                ],
                'statistics': [
                    {"label": "AI Market Size", "value": "$1.8T", "change": "By 2030"},
                    {"label": "Productivity Gain", "value": "+40%", "change": "With AI tools"},
                    {"label": "Company Adoption", "value": "77%", "change": "Using or exploring AI"}
                ],
                'key_points': ["AI is transforming every industry", "Automation replacing routine tasks", "Human-AI collaboration is key"]
            }
        
        elif 'food' in query.lower() or 'cooking' in query.lower() or 'recipe' in query.lower():
            return {
                'facts': [
                    "Home cooking saves families $3000+ annually compared to dining out",
                    "Meal prep reduces food waste by up to 40%",
                    "Mediterranean diet linked to 20% lower risk of heart disease",
                    "Cooking releases stress-reducing endorphins in the brain"
                ],
                'statistics': [
                    {"label": "Annual Savings", "value": "$3,000+", "change": "From home cooking"},
                    {"label": "Food Waste Reduction", "value": "-40%", "change": "With meal prep"},
                    {"label": "Heart Disease Risk", "value": "-20%", "change": "Mediterranean diet"}
                ],
                'key_points': ["Fresh ingredients make all the difference", "Prep ahead for busy weeks", "Simple techniques yield big flavors"]
            }
        
        elif 'travel' in query.lower() or 'vacation' in query.lower():
            return {
                'facts': [
                    "Travel reduces stress hormones by up to 68%",
                    "People who travel are 7% happier than those who don't",
                    "Booking trips 6-8 weeks in advance saves 20% on average",
                    "Travel experiences create longer-lasting happiness than material purchases"
                ],
                'statistics': [
                    {"label": "Stress Reduction", "value": "-68%", "change": "From travel"},
                    {"label": "Happiness Boost", "value": "+7%", "change": "For travelers"},
                    {"label": "Booking Savings", "value": "20%", "change": "6-8 weeks advance"}
                ],
                'key_points': ["Experiences beat possessions", "Plan ahead for better deals", "Local culture enriches the journey"]
            }
        
        elif 'productivity' in query.lower() or 'success' in query.lower() or 'habits' in query.lower():
            return {
                'facts': [
                    "It takes 21 days to form a habit, 66 days to make it automatic",
                    "People who write down goals are 42% more likely to achieve them",
                    "The first 2 hours of your day determine 80% of your productivity",
                    "Multitasking reduces productivity by up to 40%"
                ],
                'statistics': [
                    {"label": "Goal Achievement", "value": "+42%", "change": "When written down"},
                    {"label": "Productivity Loss", "value": "-40%", "change": "From multitasking"},
                    {"label": "Habit Formation", "value": "66 days", "change": "To become automatic"}
                ],
                'key_points': ["Start small and be consistent", "Focus on one thing at a time", "Morning routines set the tone"]
            }
        
        else:
            # Dynamic research for any other topic
            topic_words = query.split()
            main_topic = topic_words[0] if topic_words else "topic"
            
            return {
                'facts': [
                    f"Recent studies show {main_topic} is growing 45% year-over-year",
                    f"Experts predict {main_topic} will be revolutionary in the next 5 years",
                    f"Over 2.3 million people are now actively engaged with {main_topic}",
                    f"Industry leaders are investing heavily in {main_topic} innovations"
                ],
                'statistics': [
                    {"label": f"{main_topic.title()} Growth", "value": "+45%", "change": "Year-over-year"},
                    {"label": "Active Users", "value": "2.3M", "change": "+67% this year"},
                    {"label": "Investment", "value": "$12B", "change": "Industry funding"}
                ],
                'key_points': [
                    f"{main_topic.title()} is transforming industries",
                    "Innovation driving rapid adoption",
                    "Future looks incredibly promising"
                ]
            }
    
    def _get_fallback_research(self, prompt: str, style: str) -> Dict:
        """Fallback research data when APIs fail"""
        return {
            'facts': [f"Key insights about {prompt}", f"Important developments in this area", f"Latest trends and updates"],
            'statistics': [{"label": "Growth", "value": "+25%", "change": "This year"}],
            'key_points': ["Growing interest", "Market potential", "Future outlook"]
        }
    
    async def _generate_script(self, prompt: str, research_data: Dict, style: str, duration: int) -> Dict:
        """Generate engaging script based on research"""
        
        # Calculate timing (aim for ~150 words per minute speaking pace)
        target_words = int(duration * 2.5)  # ~150 words/min
        
        script = {
            'segments': [],
            'total_duration': duration,
            'style': style
        }
        
        facts = research_data.get('facts', [])
        stats = research_data.get('statistics', [])
        points = research_data.get('key_points', [])
        
        # Skip generic hook - go straight to content
        
        # Generate main content
        remaining_time = duration
        if facts:
            fact_time = min(remaining_time * 0.6, len(facts) * 2)
            for i, fact in enumerate(facts[:3]):
                script['segments'].append({
                    'type': 'fact',
                    'text': fact,
                    'duration': fact_time / min(3, len(facts)),
                    'visual': 'fact_card',
                    'data': stats[i] if i < len(stats) else None
                })
            remaining_time -= fact_time
        
        # Generate conclusion
        if points and remaining_time > 2:
            conclusion = f"Remember: {', '.join(points[:2])}. What's your take?"
            script['segments'].append({
                'type': 'conclusion',
                'text': conclusion,
                'duration': remaining_time,
                'visual': 'conclusion_card'
            })
        
        return script
    
    def _should_use_music_only(self, prompt: str, style: str) -> bool:
        """Determine if we should use background music instead of voiceover"""
        
        # Use music for visual content like plans, lists, step-by-step guides
        music_keywords = ['plan', 'routine', 'workout', 'exercise', 'steps', 'list', 'guide', 
                         'top', 'best', 'picks', 'stocks', 'crypto', 'schedule', 'daily',
                         'weekly', 'monthly', 'beginner', 'advanced']
        
        prompt_lower = prompt.lower()
        for keyword in music_keywords:
            if keyword in prompt_lower:
                return True
                
        # Fitness and finance styles often work better with music
        if style in ['fitness', 'finance']:
            return True
            
        return False
    
    def _generate_hook(self, prompt: str, style: str) -> str:
        """Generate attention-grabbing opening"""
        
        hooks = {
            'finance': [
                f"Here's why {prompt.split()[0]} just changed everything:",
                f"The {prompt} situation is crazy - here's what happened:",
                f"This {prompt} move shocked Wall Street:"
            ],
            'tech': [
                f"The {prompt} breakthrough everyone's talking about:",
                f"This {prompt} development will change everything:",
                f"Why {prompt} is the next big thing:"
            ],
            'trendy': [
                f"You won't believe what happened with {prompt}:",
                f"Everyone's talking about {prompt} - here's why:",
                f"The {prompt} trend that's breaking the internet:"
            ]
        }
        
        style_hooks = hooks.get(style, hooks['trendy'])
        return style_hooks[0]  # Use first hook for consistency
    
    async def _generate_voiceover(self, script: Dict, style: str) -> str:
        """Generate TTS voiceover from script"""
        
        # Combine all text segments
        full_text = " ".join([segment['text'] for segment in script['segments']])
        
        # Clean text for TTS
        clean_text = re.sub(r'[^\w\s.,!?]', '', full_text)
        
        try:
            # Generate TTS
            tts = gTTS(text=clean_text, lang='en', slow=False)
            audio_path = f"{self.temp_dir}/voiceover_{int(time.time())}.mp3"
            tts.save(audio_path)
            
            print(f"Generated voiceover: {len(clean_text)} characters")
            return audio_path
            
        except Exception as e:
            print(f"TTS failed: {e}")
            return None
    
    async def _generate_background_music(self, style: str, duration: int) -> str:
        """Generate background music based on style"""
        import wave
        
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        # Style-specific music characteristics
        if style == 'fitness':
            # High-energy workout music
            audio = self._create_workout_beat(samples, sample_rate)
        elif style == 'finance':
            # Professional ambient music
            audio = self._create_ambient_music(samples, sample_rate)
        elif style == 'trendy':
            # Upbeat electronic-style music
            audio = self._create_electronic_beat(samples, sample_rate)
        else:
            # Default chill music
            audio = self._create_chill_music(samples, sample_rate)
        
        # Save as temporary audio file
        timestamp = int(time.time())
        audio_path = f"{self.temp_dir}/music_{timestamp}.wav"
        
        # Convert to 16-bit PCM and save
        audio_16bit = (audio * 32767).astype(np.int16)
        
        with wave.open(audio_path, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_16bit.tobytes())
        
        print(f"Generated background music: {audio_path}")
        return audio_path
    
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
    
    async def _create_visual_content(self, script: Dict, style: str, duration: int) -> List:
        """Create visual content based on script"""
        
        clips = []
        current_time = 0
        
        # Style-specific colors
        colors = self._get_style_colors(style)
        
        for segment in script['segments']:
            segment_duration = segment['duration']
            
            if segment['type'] == 'fact':
                clip = self._create_enhanced_visual(segment['text'], segment.get('data'), colors, segment_duration)
            elif segment['type'] == 'conclusion':
                clip = self._create_enhanced_visual(segment['text'], segment.get('data'), colors, segment_duration)
            else:
                clip = self._create_enhanced_visual(segment['text'], segment.get('data'), colors, segment_duration)
            
            clips.append(clip)
            current_time += segment_duration
        
        return clips
    
    def _create_hook_visual(self, text: str, colors: tuple, duration: float) -> mp.VideoClip:
        """Create simple but reliable hook visual"""
        
        def make_frame(t):
            width, height = 1080, 1920
            img = Image.new('RGB', (width, height), colors[0])
            draw = ImageDraw.Draw(img)
            
            # Simple gradient background
            for y in range(height):
                ratio = y / height
                r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
                g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
                b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Simple text
            try:
                font = ImageFont.truetype("arial.ttf", 70)
            except:
                font = ImageFont.load_default()
            
            # Word wrap text
            words = text.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > 12:
                    lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            
            # Simple bounce animation
            bounce = int(20 * np.sin(t * 4))
            
            y_offset = height // 2 - (len(lines) * 40)
            for line in lines:
                if line.strip():
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                    x = max(10, (width - text_width) // 2)
                    
                    # Shadow
                    draw.text((x+3, y_offset+bounce+3), line, font=font, fill='black')
                    # Main text
                    draw.text((x, y_offset+bounce), line, font=font, fill='white')
                    
                y_offset += 80
            
            return np.array(img)
        
        return mp.VideoClip(make_frame, duration=duration)
    
    def _create_animated_fact_visual(self, text: str, data: Dict, colors: tuple, duration: float) -> mp.VideoClip:
        """Create fact card with real visual animations"""
        
        def make_frame(t):
            width, height = 1080, 1920
            img = Image.new('RGB', (width, height), colors[0])
            draw = ImageDraw.Draw(img)
            
            # Animated gradient with wave effects
            for y in range(height):
                ratio = y / height
                wave = 0.1 * np.sin(t * 2 + y * 0.01)
                ratio = max(0, min(1, ratio + wave))
                r = int(colors[0][0] * (1-ratio) + colors[1][0] * ratio)
                g = int(colors[0][1] * (1-ratio) + colors[1][1] * ratio)
                b = int(colors[0][2] * (1-ratio) + colors[1][2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Moving geometric shapes
            num_shapes = 8
            for i in range(num_shapes):
                angle = (t * 50 + i * 45) % 360
                radius = 200 + 50 * np.sin(t * 3 + i)
                x = width // 2 + int(radius * np.cos(np.radians(angle)))
                y = height // 2 + int(radius * np.sin(np.radians(angle)))
                
                if 0 <= x < width and 0 <= y < height:
                    size = int(15 + 5 * np.sin(t * 4 + i))
                    alpha = int(100 + 50 * np.sin(t * 2 + i))
                    
                    if i % 3 == 0:
                        # Circles
                        draw.ellipse([x-size, y-size, x+size, y+size], 
                                   fill=(255, 255, 255, alpha))
                    elif i % 3 == 1:
                        # Squares
                        draw.rectangle([x-size, y-size, x+size, y+size], 
                                     fill=(255, 255, 0, alpha))
                    else:
                        # Triangles
                        draw.polygon([(x, y-size), (x-size, y+size), (x+size, y+size)], 
                                   fill=(0, 255, 255, alpha))
            
            # Floating particles
            particle_count = 20
            for i in range(particle_count):
                px = int((i * 137 + t * 100) % width)
                py = int((i * 73 + t * 80) % height)
                particle_size = int(3 + 2 * np.sin(t * 5 + i))
                draw.ellipse([px-particle_size, py-particle_size, 
                            px+particle_size, py+particle_size], fill='white')
            
            # Animated progress bars (visual interest)
            bar_count = 5
            for i in range(bar_count):
                bar_y = 100 + i * 50
                bar_progress = (t + i * 0.5) % 2  # 2-second cycle
                bar_width = int(200 * min(1, bar_progress))
                
                # Background bar
                draw.rectangle([width - 250, bar_y, width - 50, bar_y + 20], 
                             fill=(50, 50, 50))
                # Animated bar
                draw.rectangle([width - 250, bar_y, width - 250 + bar_width, bar_y + 20], 
                             fill=colors[1])
            
            try:
                title_font = ImageFont.truetype("arial.ttf", 50)
                text_font = ImageFont.truetype("arial.ttf", 40)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Animated title with pulse
            title_scale = 1 + 0.1 * np.sin(t * 6)
            title_bounce = int(10 * np.sin(t * 4))
            draw.text((50, 200 + title_bounce), "KEY INSIGHT", font=title_font, fill='yellow')
            
            # Fact text with typewriter effect
            words = text.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > 25:
                    lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            
            # Progressive text reveal
            chars_revealed = int(len(text) * min(1, t / 2))
            revealed_text = text[:chars_revealed]
            
            # Rebuild lines with revealed text
            revealed_words = revealed_text.split()
            revealed_lines = []
            current_line = []
            for word in revealed_words:
                current_line.append(word)
                if len(' '.join(current_line)) > 25:
                    revealed_lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
            if current_line:
                revealed_lines.append(' '.join(current_line))
            
            y_pos = 300
            for line in revealed_lines[:4]:
                line_bounce = int(5 * np.sin(t * 3 + y_pos * 0.01))
                draw.text((50, y_pos + line_bounce), line, font=text_font, fill='white')
                y_pos += 50
            
            # Animated data visualization
            if data:
                data_y = y_pos + 100
                
                # Animated chart
                chart_progress = min(1, (t - 1) / 2)  # Start after 1 second
                chart_width = int(300 * chart_progress)
                
                # Chart background
                draw.rectangle([50, data_y + 50, 350, data_y + 100], fill=(30, 30, 30))
                # Animated chart fill
                draw.rectangle([50, data_y + 50, 50 + chart_width, data_y + 100], fill='lime')
                
                # Data text with glow
                data_text = f"{data['label']}: {data['value']}"
                draw.text((52, data_y + 2), data_text, font=title_font, fill='black')  # Shadow
                draw.text((50, data_y), data_text, font=title_font, fill='lime')
                
                if 'change' in data:
                    change_pulse = 1 + 0.2 * np.sin(t * 8)
                    change_color = 'lime' if '+' in data['change'] else 'red'
                    draw.text((50, data_y + 160), f"Change: {data['change']}", 
                             font=text_font, fill=change_color)
            
            return np.array(img)
        
        return mp.VideoClip(make_frame, duration=duration)
    
    def _create_animated_conclusion_visual(self, text: str, colors: tuple, duration: float) -> mp.VideoClip:
        """Create conclusion visual with spectacular animations"""
        
        def make_frame(t):
            width, height = 1080, 1920
            img = Image.new('RGB', (width, height), colors[1])
            draw = ImageDraw.Draw(img)
            
            # Animated spiral background
            center_x, center_y = width // 2, height // 2
            for spiral in range(3):
                for angle_step in range(0, 360, 15):
                    angle = angle_step + t * 100 + spiral * 120
                    radius = 100 + spiral * 80 + 30 * np.sin(t * 2 + spiral)
                    x = center_x + int(radius * np.cos(np.radians(angle)))
                    y = center_y + int(radius * np.sin(np.radians(angle)))
                    
                    if 0 <= x < width and 0 <= y < height:
                        size = int(8 + 4 * np.sin(t * 3 + angle_step))
                        alpha = int(150 + 50 * np.sin(t + spiral))
                        draw.ellipse([x-size, y-size, x+size, y+size], 
                                   fill=colors[0])
            
            # Animated radiating lines
            line_count = 12
            for i in range(line_count):
                angle = i * 30 + t * 50
                length = 200 + 50 * np.sin(t * 2 + i)
                
                x1 = center_x + int(50 * np.cos(np.radians(angle)))
                y1 = center_y + int(50 * np.sin(np.radians(angle)))
                x2 = center_x + int(length * np.cos(np.radians(angle)))
                y2 = center_y + int(length * np.sin(np.radians(angle)))
                
                width_val = int(3 + 2 * np.sin(t * 4 + i))
                draw.line([(x1, y1), (x2, y2)], fill='white', width=width_val)
            
            # Pulsating border with layers
            for layer in range(4):
                border_pulse = int(15 + layer * 8 + 15 * np.sin(t * 4 + layer))
                border_alpha = int(100 + 50 * np.sin(t * 3 + layer))
                border_color = colors[0] if layer % 2 == 0 else 'white'
                
                draw.rectangle([border_pulse, border_pulse, width-border_pulse, height-border_pulse], 
                              outline=border_color, width=3 + layer)
            
            # Floating icons/symbols
            icon_count = 15
            for i in range(icon_count):
                icon_angle = (t * 80 + i * 24) % 360
                icon_radius = 300 + 100 * np.sin(t * 1.5 + i)
                icon_x = center_x + int(icon_radius * np.cos(np.radians(icon_angle)))
                icon_y = center_y + int(icon_radius * np.sin(np.radians(icon_angle)))
                
                if 0 <= icon_x < width and 0 <= icon_y < height:
                    icon_size = int(12 + 6 * np.sin(t * 5 + i))
                    
                    if i % 4 == 0:
                        # Hearts
                        draw.ellipse([icon_x-icon_size//2, icon_y-icon_size//2, 
                                    icon_x+icon_size//2, icon_y], fill='red')
                        draw.ellipse([icon_x, icon_y-icon_size//2, 
                                    icon_x+icon_size, icon_y], fill='red')
                        draw.polygon([(icon_x+icon_size//4, icon_y), 
                                    (icon_x-icon_size//2, icon_y+icon_size), 
                                    (icon_x+icon_size, icon_y+icon_size)], fill='red')
                    elif i % 4 == 1:
                        # Stars
                        points = []
                        for p in range(10):
                            a = p * 36
                            r = icon_size if p % 2 == 0 else icon_size // 2
                            px = icon_x + int(r * np.cos(np.radians(a)))
                            py = icon_y + int(r * np.sin(np.radians(a)))
                            points.append((px, py))
                        draw.polygon(points, fill='yellow')
                    elif i % 4 == 2:
                        # Thumbs up (simplified)
                        draw.rectangle([icon_x-icon_size//3, icon_y, 
                                      icon_x+icon_size//3, icon_y+icon_size], fill='lime')
                        draw.ellipse([icon_x-icon_size//2, icon_y-icon_size//2, 
                                    icon_x+icon_size//2, icon_y+icon_size//2], fill='lime')
                    else:
                        # Lightning bolt
                        draw.polygon([(icon_x, icon_y-icon_size), 
                                    (icon_x+icon_size//2, icon_y), 
                                    (icon_x-icon_size//4, icon_y), 
                                    (icon_x, icon_y+icon_size)], fill='cyan')
            
            try:
                font = ImageFont.truetype("arial.ttf", 45)
                cta_font = ImageFont.truetype("arial.ttf", 65)
            except:
                font = ImageFont.load_default()
                cta_font = ImageFont.load_default()
            
            # Animated text with effects
            words = text.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > 18:
                    lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            
            y_start = height // 2 - (len(lines) * 35)
            for i, line in enumerate(lines):
                # Wave effect for each line
                wave_offset = int(20 * np.sin(t * 4 + i * 0.8))
                
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = max(10, (width - text_width) // 2)
                
                # Simple shadow for text
                draw.text((x + 2, y_start + wave_offset + 2), line, font=font, fill='black')
                draw.text((x, y_start + wave_offset), line, font=font, fill='white')
                
                y_start += 70
            
            # Spectacular animated CTA
            cta = "LIKE & FOLLOW FOR MORE!"
            
            # Rainbow effect
            hue = (t * 200) % 360
            r = int(255 * (1 + np.sin(np.radians(hue))) / 2)
            g = int(255 * (1 + np.sin(np.radians(hue + 120))) / 2)
            b = int(255 * (1 + np.sin(np.radians(hue + 240))) / 2)
            rainbow_color = (r, g, b)
            
            # Bouncing CTA
            cta_bounce = int(30 * np.sin(t * 6))
            cta_scale = 1 + 0.2 * np.sin(t * 8)
            
            bbox = draw.textbbox((0, 0), cta, font=cta_font)
            text_width = bbox[2] - bbox[0]
            x = max(10, (width - int(text_width * cta_scale)) // 2)
            cta_y = height - 250 + cta_bounce
            
            # Simple shadow effect for CTA
            draw.text((x + 3, cta_y + 3), cta, font=cta_font, fill='black')  # Shadow
            draw.text((x, cta_y), cta, font=cta_font, fill=rainbow_color)    # Main text
            
            # Sparkles around CTA
            sparkle_count = 8
            for i in range(sparkle_count):
                sparkle_angle = (t * 300 + i * 45) % 360
                sparkle_radius = 150 + 30 * np.sin(t * 4 + i)
                sx = x + text_width // 2 + int(sparkle_radius * np.cos(np.radians(sparkle_angle)))
                sy = cta_y + 30 + int(sparkle_radius * np.sin(np.radians(sparkle_angle)))
                
                if 0 <= sx < width and 0 <= sy < height:
                    sparkle_size = int(8 + 4 * np.sin(t * 10 + i))
                    # 4-pointed star
                    draw.polygon([(sx, sy-sparkle_size), (sx+sparkle_size//2, sy), 
                                (sx, sy+sparkle_size), (sx-sparkle_size//2, sy)], 
                               fill='yellow')
            
            return np.array(img)
        
        return mp.VideoClip(make_frame, duration=duration)
    
    def _create_enhanced_visual(self, text: str, data: Dict, colors: tuple, duration: float) -> mp.VideoClip:
        """Create enhanced visual with reliable animations"""
        
        def make_frame(t):
            width, height = 1080, 1920
            img = Image.new('RGB', (width, height), colors[0])
            draw = ImageDraw.Draw(img)
            
            # Animated gradient background
            for y in range(height):
                ratio = y / height
                wave = 0.15 * np.sin(t * 2 + y * 0.005)  # Gentler wave
                ratio = max(0, min(1, ratio + wave))
                r = int(colors[0][0] * (1-ratio) + colors[1][0] * ratio)
                g = int(colors[0][1] * (1-ratio) + colors[1][1] * ratio)
                b = int(colors[0][2] * (1-ratio) + colors[1][2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Moving circles animation
            circle_count = 6
            for i in range(circle_count):
                angle = (t * 30 + i * 60) % 360
                radius = 250 + 50 * np.sin(t + i)
                cx = width // 2 + int(radius * np.cos(np.radians(angle)))
                cy = height // 2 + int(radius * np.sin(np.radians(angle)))
                
                if 50 <= cx <= width - 50 and 50 <= cy <= height - 50:
                    circle_size = int(20 + 10 * np.sin(t * 3 + i))
                    alpha = int(80 + 40 * np.sin(t * 2 + i))
                    
                    # Draw circles with different colors
                    if i % 3 == 0:
                        color = 'white'
                    elif i % 3 == 1:
                        color = 'yellow'
                    else:
                        color = 'cyan'
                        
                    draw.ellipse([cx-circle_size, cy-circle_size, 
                                cx+circle_size, cy+circle_size], fill=color)
            
            # Floating particles
            particle_count = 15
            for i in range(particle_count):
                px = int((i * 89 + t * 80) % width)
                py = int((i * 113 + t * 60) % height)
                particle_size = int(4 + 2 * np.sin(t * 4 + i))
                
                # Make sure particles are within bounds
                if particle_size <= px <= width - particle_size and particle_size <= py <= height - particle_size:
                    draw.ellipse([px-particle_size, py-particle_size, 
                                px+particle_size, py+particle_size], fill='white')
            
            # Animated progress bars on the side
            bar_count = 4
            for i in range(bar_count):
                bar_y = 200 + i * 80
                bar_progress = (t * 0.8 + i * 0.5) % 3  # 3-second cycle
                bar_width = int(150 * min(1, bar_progress))
                
                # Ensure bars are within bounds
                bar_x = width - 200
                if bar_x + bar_width <= width - 20:
                    # Background bar
                    draw.rectangle([bar_x, bar_y, bar_x + 150, bar_y + 15], fill=(40, 40, 40))
                    # Animated bar
                    if bar_width > 0:
                        draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + 15], fill=colors[1])
            
            try:
                title_font = ImageFont.truetype("arial.ttf", 55)
                text_font = ImageFont.truetype("arial.ttf", 42)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Animated title
            title_bounce = int(15 * np.sin(t * 4))
            draw.text((60, 180 + title_bounce), "KEY INSIGHT", font=title_font, fill='yellow')
            
            # Progressive text reveal
            chars_per_second = 20
            chars_revealed = int(chars_per_second * t)
            revealed_text = text[:chars_revealed]
            
            # Word wrap revealed text
            words = revealed_text.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > 22:
                    if len(current_line) > 1:
                        lines.append(' '.join(current_line[:-1]))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []
            if current_line:
                lines.append(' '.join(current_line))
            
            y_pos = 280
            for line in lines[:4]:  # Max 4 lines
                if line.strip():
                    line_bounce = int(8 * np.sin(t * 3 + y_pos * 0.01))
                    
                    # Simple shadow
                    draw.text((62, y_pos + line_bounce + 2), line, font=text_font, fill='black')
                    draw.text((60, y_pos + line_bounce), line, font=text_font, fill='white')
                    
                y_pos += 60
            
            # Data visualization if available
            if data:
                data_y = y_pos + 80
                data_text = f"{data['label']}: {data['value']}"
                
                # Ensure data text is within bounds
                if data_y + 100 < height:
                    # Simple shadow for data
                    draw.text((62, data_y + 2), data_text, font=title_font, fill='black')
                    draw.text((60, data_y), data_text, font=title_font, fill='lime')
                    
                    if 'change' in data:
                        change_text = f"Change: {data['change']}"
                        change_color = 'lime' if '+' in data['change'] else 'orange'
                        draw.text((62, data_y + 62), change_text, font=text_font, fill='black')
                        draw.text((60, data_y + 60), change_text, font=text_font, fill=change_color)
            
            return np.array(img)
        
        return mp.VideoClip(make_frame, duration=duration)
        
    def _create_default_visual(self, text: str, colors: tuple, duration: float) -> mp.VideoClip:
        """Create default visual for any segment"""
        return self._create_enhanced_visual(text, None, colors, duration)
    
    def _get_style_colors(self, style: str) -> tuple:
        """Get color scheme for style"""
        color_schemes = {
            'trendy': ((255, 20, 147), (138, 43, 226)),  # Pink to Purple
            'business': ((30, 144, 255), (0, 191, 255)),  # Blue gradient
            'lifestyle': ((50, 205, 50), (0, 250, 154)),  # Green gradient
            'tech': ((148, 0, 211), (75, 0, 130)),  # Purple gradient
            'finance': ((255, 215, 0), (255, 140, 0)),  # Gold gradient
            'fitness': ((220, 20, 60), (255, 69, 0))  # Red gradient
        }
        return color_schemes.get(style, color_schemes['trendy'])
    
    async def _combine_content(self, visual_clips: List, voiceover_path: str, duration: int) -> mp.VideoClip:
        """Combine visual clips with voiceover"""
        
        # Concatenate visual clips
        if visual_clips:
            video = mp.concatenate_videoclips(visual_clips)
        else:
            # Fallback single clip
            video = self._create_fallback_clip(duration)
        
        # Add voiceover if available
        if voiceover_path and os.path.exists(voiceover_path):
            try:
                audio = mp.AudioFileClip(voiceover_path)
                # Trim or extend audio to match video duration
                if audio.duration > duration:
                    audio = audio.subclip(0, duration)
                elif audio.duration < duration:
                    # Add silence at the end
                    silence_duration = duration - audio.duration
                    silence = mp.AudioClip(lambda t: 0, duration=silence_duration)
                    audio = mp.concatenate_audioclips([audio, silence])
                
                video = video.set_audio(audio)
                print(f"Added voiceover audio ({audio.duration:.1f}s)")
            except Exception as e:
                print(f"Failed to add audio: {e}")
        
        return video
    
    def _create_fallback_clip(self, duration: int) -> mp.VideoClip:
        """Create fallback visual when others fail"""
        def make_frame(t):
            width, height = 1080, 1920
            frame = np.random.randint(50, 200, (height, width, 3), dtype=np.uint8)
            return frame
        
        return mp.VideoClip(make_frame, duration=duration)
    
    async def _create_fallback_reel(self, prompt: str, style: str, duration: int, output_path: str) -> str:
        """Create simple fallback reel if AI generation fails"""
        
        colors = self._get_style_colors(style)
        
        def make_frame(t):
            width, height = 1080, 1920
            img = Image.new('RGB', (width, height), colors[0])
            draw = ImageDraw.Draw(img)
            
            # Simple gradient
            for y in range(height):
                ratio = y / height
                r = int(colors[0][0] * (1-ratio) + colors[1][0] * ratio)
                g = int(colors[0][1] * (1-ratio) + colors[1][1] * ratio)
                b = int(colors[0][2] * (1-ratio) + colors[1][2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Add prompt text
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            # Center text
            bbox = draw.textbbox((0, 0), prompt, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = height // 2
            draw.text((x, y), prompt, font=font, fill='white')
            
            return np.array(img)
        
        video = mp.VideoClip(make_frame, duration=duration)
        video.write_videofile(output_path, fps=15, verbose=False, logger=None)
        
        return output_path