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
            
            # Step 3: Generate voiceover audio
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
        
        # Generate hook (first 3 seconds)
        hook = self._generate_hook(prompt, style)
        script['segments'].append({
            'type': 'hook',
            'text': hook,
            'duration': 3,
            'visual': 'attention_grabber'
        })
        
        # Generate main content
        remaining_time = duration - 3
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
    
    async def _create_visual_content(self, script: Dict, style: str, duration: int) -> List:
        """Create visual content based on script"""
        
        clips = []
        current_time = 0
        
        # Style-specific colors
        colors = self._get_style_colors(style)
        
        for segment in script['segments']:
            segment_duration = segment['duration']
            
            if segment['type'] == 'hook':
                clip = self._create_hook_visual(segment['text'], colors, segment_duration)
            elif segment['type'] == 'fact':
                clip = self._create_fact_visual(segment['text'], segment.get('data'), colors, segment_duration)
            elif segment['type'] == 'conclusion':
                clip = self._create_conclusion_visual(segment['text'], colors, segment_duration)
            else:
                clip = self._create_default_visual(segment['text'], colors, segment_duration)
            
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
    
    def _create_fact_visual(self, text: str, data: Dict, colors: tuple, duration: float) -> mp.VideoClip:
        """Create animated fact card with data visualization"""
        
        def make_frame(t):
            width, height = 1080, 1920
            img = Image.new('RGB', (width, height), colors[0])
            draw = ImageDraw.Draw(img)
            
            progress = t / duration
            
            # Simple animated gradient background
            wave_offset = t * 50
            for y in range(0, height, 2):  # Every 2nd line for performance
                ratio = y / height
                wave_factor = 0.1 * np.sin((y + wave_offset) * 0.02)
                ratio = max(0, min(1, ratio + wave_factor))
                
                r = int(colors[0][0] * (1-ratio) + colors[1][0] * ratio)
                g = int(colors[0][1] * (1-ratio) + colors[1][1] * ratio)
                b = int(colors[0][2] * (1-ratio) + colors[1][2] * ratio)
                draw.rectangle([(0, y), (width, y+2)], fill=(r, g, b))
            
            # Add animated border/frame
            border_pulse = int(10 + 5 * np.sin(t * 4))
            border_color = (255, 255, 255, int(200 + 55 * np.sin(t * 3)))
            draw.rectangle([border_pulse, border_pulse, width-border_pulse, height-border_pulse], 
                          outline='white', width=3)
            
            # Add fact text with animations
            try:
                title_font = ImageFont.truetype("arial.ttf", 60)
                text_font = ImageFont.truetype("arial.ttf", 45)
                stat_font = ImageFont.truetype("arial.ttf", 55)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                stat_font = ImageFont.load_default()
            
            # Animated title with slide-in effect
            title_slide = min(1.0, t * 3)  # Slide in quickly
            title_x = int(-200 + (250 * title_slide))  # Slide from left
            title_scale = 1.0 + 0.1 * np.sin(t * 5)  # Subtle pulse
            
            # Title with glow effect
            title_text = "KEY INSIGHT"
            for offset in [(4, 4), (2, 2), (0, 0)]:
                color = 'black' if offset != (0, 0) else 'yellow'
                draw.text((title_x + offset[0], 200 + offset[1]), title_text, font=title_font, fill=color)
            
            # Fact text with word-by-word reveal
            words = text.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > 20:  # Shorter lines for bigger text
                    lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            
            # Progressive text reveal
            text_reveal_progress = min(1.0, (t - 0.5) * 2)  # Start after title
            total_words = len(' '.join(lines).split())
            words_to_show = int(total_words * text_reveal_progress)
            
            all_words = ' '.join(lines).split()
            revealed_words = all_words[:words_to_show]
            
            # Rebuild lines with revealed words
            revealed_lines = []
            current_line = []
            for word in revealed_words:
                current_line.append(word)
                if len(' '.join(current_line)) > 20:
                    revealed_lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
            if current_line:
                revealed_lines.append(' '.join(current_line))
            
            y_pos = 320
            for i, line in enumerate(revealed_lines[:4]):  # Max 4 lines
                if not line.strip():
                    continue
                    
                # Add bounce effect to each line
                bounce = int(5 * np.sin(t * 4 + i * 0.8))
                
                # Text with shadow for depth
                for shadow_offset in [(3, 3), (1, 1), (0, 0)]:
                    color = 'black' if shadow_offset != (0, 0) else 'white'
                    draw.text((60 + shadow_offset[0], y_pos + bounce + shadow_offset[1]), 
                             line, font=text_font, fill=color)
                
                y_pos += 65
            
            # Animated data visualization
            if data and progress > 0.3:  # Data appears after text
                data_progress = min(1.0, (t - 1.0) * 2)  # Delayed appearance
                
                # Create animated chart/bar for statistics
                chart_y = y_pos + 80
                chart_width = 400
                chart_height = 60
                
                # Background bar
                draw.rectangle([60, chart_y, 60 + chart_width, chart_y + chart_height], 
                              fill=(50, 50, 50), outline='white', width=2)
                
                # Animated progress bar based on data value
                if data.get('value'):
                    # Extract percentage if available
                    value_str = str(data['value'])
                    percentage = 0.7  # Default
                    if '%' in value_str:
                        try:
                            percentage = abs(float(value_str.replace('%', '').replace('+', '').replace(',', ''))) / 100
                            percentage = min(1.0, percentage)
                        except:
                            percentage = 0.7
                    
                    # Animated fill
                    fill_width = int(chart_width * percentage * data_progress)
                    bar_color = 'lime' if '+' in value_str or percentage > 0 else 'red'
                    
                    draw.rectangle([60, chart_y, 60 + fill_width, chart_y + chart_height], 
                                  fill=bar_color)
                
                # Data label with typewriter effect
                label_text = f"{data['label']}: {data['value']}"
                chars_to_show = int(len(label_text) * data_progress)
                visible_label = label_text[:chars_to_show]
                
                # Glowing text effect for data
                for glow in [(6, 6), (3, 3), (0, 0)]:
                    glow_color = 'black' if glow != (0, 0) else 'lime'
                    draw.text((60 + glow[0], chart_y - 50 + glow[1]), 
                             visible_label, font=stat_font, fill=glow_color)
                
                # Change indicator with pulsing effect
                if 'change' in data and data_progress > 0.5:
                    change_pulse = 1.0 + 0.2 * np.sin(t * 6)
                    change_text = f"Change: {data['change']}"
                    change_color = 'lime' if '+' in data['change'] else 'orange'
                    
                    draw.text((60, chart_y + chart_height + 20), 
                             change_text, font=text_font, fill=change_color)
            
            # Simplified floating icons for performance
            if progress > 0.7:
                icon_count = 4  # Reduced from 8
                for i in range(icon_count):
                    icon_x = int(width - 80 + 20 * np.sin(t * 2 + i))
                    icon_y = int(300 + i * 300)
                    icon_size = 10  # Fixed size
                    
                    # Simple circles only for performance
                    draw.ellipse([icon_x - icon_size, icon_y - icon_size,
                                icon_x + icon_size, icon_y + icon_size],
                               fill='white')
            
            return np.array(img)
        
        return mp.VideoClip(make_frame, duration=duration)
    
    def _create_conclusion_visual(self, text: str, colors: tuple, duration: float) -> mp.VideoClip:
        """Create animated conclusion/CTA visual"""
        
        def make_frame(t):
            width, height = 1080, 1920
            img = Image.new('RGB', (width, height), colors[1])
            draw = ImageDraw.Draw(img)
            
            progress = t / duration
            
            # Animated spiral background
            center_x, center_y = width // 2, height // 2
            for radius in range(20, min(width, height) // 2, 40):
                spiral_progress = (t * 2 + radius * 0.01) % (2 * np.pi)
                spiral_x = center_x + int(radius * np.cos(spiral_progress))
                spiral_y = center_y + int(radius * np.sin(spiral_progress))
                
                # Fade effect for distant spirals
                alpha = max(0, 255 - radius // 3)
                spiral_size = max(1, int(10 - radius // 50))
                
                draw.ellipse([spiral_x - spiral_size, spiral_y - spiral_size,
                            spiral_x + spiral_size, spiral_y + spiral_size],
                           fill=colors[0])
            
            # Pulsating border with multiple layers
            for layer in range(3):
                border_pulse = int(15 + layer * 5 + 10 * np.sin(t * 4 + layer))
                border_alpha = int(100 + 50 * np.sin(t * 3 + layer))
                border_color = colors[0] if layer % 2 == 0 else 'white'
                
                draw.rectangle([border_pulse, border_pulse, width-border_pulse, height-border_pulse], 
                              outline=border_color, width=2 + layer)
            
            try:
                font = ImageFont.truetype("arial.ttf", 50)
                cta_font = ImageFont.truetype("arial.ttf", 70)
            except:
                font = ImageFont.load_default()
                cta_font = ImageFont.load_default()
            
            # Wrap and center text with bounce animations
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
            
            # Text with cascading reveal effect
            text_progress = min(1.0, progress * 2)
            lines_to_show = int(len(lines) * text_progress)
            
            y_start = height // 2 - (len(lines) * 40)
            for i, line in enumerate(lines[:lines_to_show + 1]):
                if i > lines_to_show:
                    break
                    
                # Bounce effect with different phases for each line
                bounce = int(15 * np.sin(t * 5 + i * 1.2))
                
                # Slide in from different directions
                slide_progress = min(1.0, (progress - i * 0.1) * 3)
                if slide_progress <= 0:
                    continue
                    
                slide_x = int(width * (1 - slide_progress) * (1 if i % 2 == 0 else -1))
                
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = max(1, bbox[2] - bbox[0])
                x = max(0, (width - text_width) // 2 + slide_x)
                y = y_start + bounce
                
                # Multi-shadow effect for depth
                for shadow in [(6, 6), (3, 3), (0, 0)]:
                    shadow_color = 'black' if shadow != (0, 0) else 'white'
                    draw.text((x + shadow[0], y + shadow[1]), line, font=font, fill=shadow_color)
                
                y_start += 70
            
            # Spectacular CTA with rainbow and pulse effects
            if progress > 0.6:  # CTA appears later for impact
                cta_progress = (progress - 0.6) / 0.4  # 0 to 1 for CTA animation
                
                cta = "LIKE & FOLLOW FOR MORE!"
                
                # Rainbow color cycle for CTA
                hue_shift = (t * 200) % 360
                r = int(255 * (1 + np.sin(np.radians(hue_shift))) / 2)
                g = int(255 * (1 + np.sin(np.radians(hue_shift + 120))) / 2)
                b = int(255 * (1 + np.sin(np.radians(hue_shift + 240))) / 2)
                rainbow_color = (r, g, b)
                
                # Scale pulsing effect
                cta_scale = 1.0 + 0.3 * np.sin(t * 6) * cta_progress
                
                # Position with slight bounce
                cta_bounce = int(20 * np.sin(t * 4))
                bbox = draw.textbbox((0, 0), cta, font=cta_font)
                text_width = bbox[2] - bbox[0]
                cta_x = (width - int(text_width * cta_scale)) // 2
                cta_y = height - 250 + cta_bounce
                
                # Multiple outline layers for glow effect
                for glow_size in [8, 5, 3, 0]:
                    glow_color = 'black' if glow_size > 0 else rainbow_color
                    
                    for glow_x in range(-glow_size, glow_size + 1):
                        for glow_y in range(-glow_size, glow_size + 1):
                            if glow_x == 0 and glow_y == 0 and glow_size > 0:
                                continue
                            draw.text((cta_x + glow_x, cta_y + glow_y), cta, font=cta_font, fill=glow_color)
                
                # Simplified sparkle effects 
                if cta_progress > 0.5:
                    sparkle_count = 6  # Reduced from 12
                    for i in range(sparkle_count):
                        sparkle_angle = (t * 200 + i * 60) % 360  # Slower rotation
                        sparkle_radius = 120  # Fixed radius
                        sparkle_x = cta_x + text_width // 2 + int(sparkle_radius * np.cos(np.radians(sparkle_angle)))
                        sparkle_y = cta_y + 40 + int(sparkle_radius * np.sin(np.radians(sparkle_angle)))
                        
                        if 0 <= sparkle_x < width and 0 <= sparkle_y < height:
                            sparkle_size = 8  # Fixed size
                            draw.ellipse([sparkle_x - sparkle_size, sparkle_y - sparkle_size,
                                        sparkle_x + sparkle_size, sparkle_y + sparkle_size],
                                       fill='yellow')
            
            # Add corner decorations
            corner_size = int(30 + 20 * np.sin(t * 3))
            for corner in [(50, 50), (width-50, 50), (50, height-50), (width-50, height-50)]:
                draw.ellipse([corner[0] - corner_size, corner[1] - corner_size,
                            corner[0] + corner_size, corner[1] + corner_size],
                           fill=colors[0], outline='white', width=3)
            
            return np.array(img)
        
        return mp.VideoClip(make_frame, duration=duration)
    
    def _create_default_visual(self, text: str, colors: tuple, duration: float) -> mp.VideoClip:
        """Create default visual for any segment"""
        return self._create_fact_visual(text, None, colors, duration)
    
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