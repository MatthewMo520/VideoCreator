import random
from typing import List, Dict, Optional
import re

class TextOverlay:
    def __init__(self):
        self.trending_fonts = [
            'Arial-Bold', 'Helvetica-Bold', 'Impact', 'Anton-Regular',
            'Roboto-Bold', 'Montserrat-Bold', 'Oswald-Bold'
        ]
        
        self.style_configs = {
            "trendy": {
                "colors": ["white", "yellow", "#FF6B6B", "#4ECDC4", "#45B7D1"],
                "stroke_colors": ["black", "#333333"],
                "fontsize_range": (50, 80),
                "positions": ["center", ("center", "top"), ("center", "bottom")],
                "effects": ["bounce", "fade", "slide"]
            },
            "business": {
                "colors": ["white", "#2C3E50", "#34495E"],
                "stroke_colors": ["black", "white"],
                "fontsize_range": (40, 60),
                "positions": ["center", ("center", "bottom")],
                "effects": ["fade", "slide"]
            },
            "lifestyle": {
                "colors": ["white", "#F39C12", "#E74C3C"],
                "stroke_colors": ["black", "#2C3E50"],
                "fontsize_range": (45, 70),
                "positions": ["center", ("left", "bottom"), ("right", "top")],
                "effects": ["fade", "typewriter"]
            },
            "tech": {
                "colors": ["#00FF00", "#0080FF", "#FF0080", "white"],
                "stroke_colors": ["black", "#001122"],
                "fontsize_range": (50, 75),
                "positions": ["center", ("center", "top")],
                "effects": ["glitch", "fade"]
            },
            "finance": {
                "colors": ["#00FF00", "#FF0000", "white", "#FFD700"],
                "stroke_colors": ["black", "#003300"],
                "fontsize_range": (55, 85),
                "positions": ["center", ("center", "bottom")],
                "effects": ["counter", "fade"]
            },
            "fitness": {
                "colors": ["#FF4444", "#00AA00", "white", "#FFAA00"],
                "stroke_colors": ["black", "#330000"],
                "fontsize_range": (60, 90),
                "positions": ["center", ("center", "top")],
                "effects": ["bounce", "pulse"]
            }
        }
    
    def generate_overlay_texts(
        self, 
        prompt: str, 
        style: str, 
        trending_data: Optional[Dict] = None
    ) -> List[Dict]:
        """Generate text overlays based on prompt and style"""
        
        overlay_texts = []
        style_config = self.style_configs.get(style, self.style_configs["trendy"])
        
        # Extract key phrases from prompt
        key_phrases = self._extract_key_phrases(prompt)
        
        # Add trending hashtags if available
        if trending_data and trending_data.get('hashtags'):
            trending_hashtags = trending_data['hashtags'][:3]  # Top 3 hashtags
        else:
            trending_hashtags = self._generate_generic_hashtags(style)
        
        # Generate main title text
        main_text = self._generate_main_text(prompt, style)
        overlay_texts.append({
            "text": main_text,
            "fontsize": random.randint(*style_config["fontsize_range"]),
            "color": random.choice(style_config["colors"]),
            "stroke_color": random.choice(style_config["stroke_colors"]),
            "stroke_width": 3,
            "font": random.choice(self.trending_fonts),
            "position": "center",
            "start": 0.5,
            "duration": 3
        })
        
        # Add key phrases as smaller overlays
        for i, phrase in enumerate(key_phrases[:3]):
            overlay_texts.append({
                "text": phrase.upper(),
                "fontsize": random.randint(30, 50),
                "color": random.choice(style_config["colors"]),
                "stroke_color": random.choice(style_config["stroke_colors"]),
                "stroke_width": 2,
                "font": random.choice(self.trending_fonts),
                "position": random.choice(style_config["positions"]),
                "start": 2 + i * 2,
                "duration": 2.5
            })
        
        # Add hashtags overlay
        hashtag_text = " ".join([f"#{tag}" for tag in trending_hashtags])
        overlay_texts.append({
            "text": hashtag_text,
            "fontsize": 35,
            "color": style_config["colors"][0],
            "stroke_color": style_config["stroke_colors"][0],
            "stroke_width": 1,
            "font": self.trending_fonts[0],
            "position": ("center", "bottom"),
            "start": -3,  # Last 3 seconds
            "duration": 3
        })
        
        # Add call-to-action based on style
        cta_text = self._generate_cta(style)
        if cta_text:
            overlay_texts.append({
                "text": cta_text,
                "fontsize": 40,
                "color": "#FFFF00",  # Bright yellow for attention
                "stroke_color": "black",
                "stroke_width": 2,
                "font": "Arial-Bold",
                "position": ("center", "top"),
                "start": -4,
                "duration": 2
            })
        
        return overlay_texts
    
    def _extract_key_phrases(self, prompt: str) -> List[str]:
        """Extract key phrases from the prompt"""
        
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', prompt.lower())
        
        # Remove common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Take top keywords and create phrases
        phrases = []
        if len(keywords) >= 2:
            phrases.append(f"{keywords[0]} {keywords[1]}")
        if len(keywords) >= 4:
            phrases.append(f"{keywords[2]} {keywords[3]}")
        if len(keywords) >= 1:
            phrases.append(keywords[0])
        
        return phrases[:3]
    
    def _generate_main_text(self, prompt: str, style: str) -> str:
        """Generate main overlay text based on prompt and style"""
        
        style_templates = {
            "trendy": [
                "✨ {key} ✨",
                "🔥 {key} 🔥",
                "💯 {key}",
                "{key} HITS DIFFERENT",
                "THIS {key} THOUGH"
            ],
            "business": [
                "{key} Strategy",
                "Professional {key}",
                "{key} Success",
                "Master {key}",
                "{key} Excellence"
            ],
            "lifestyle": [
                "Living with {key}",
                "My {key} Journey",
                "{key} Life",
                "Everyday {key}",
                "{key} Vibes"
            ],
            "tech": [
                "{key} 2.0",
                "Next-Gen {key}",
                "{key} Revolution",
                "Smart {key}",
                "{key} Innovation"
            ],
            "finance": [
                "{key} GAINS 📈",
                "{key} TO THE MOON 🚀",
                "💰 {key} PROFIT",
                "{key} INVESTMENT",
                "📊 {key} RETURNS"
            ],
            "fitness": [
                "{key} POWER 💪",
                "STRONG {key}",
                "{key} GAINS",
                "FIT {key}",
                "{key} ENERGY ⚡"
            ]
        }
        
        # Extract first key word from prompt
        words = prompt.split()
        key_word = words[0] if words else "CONTENT"
        
        templates = style_templates.get(style, style_templates["trendy"])
        template = random.choice(templates)
        
        return template.format(key=key_word.upper())
    
    def _generate_generic_hashtags(self, style: str) -> List[str]:
        """Generate generic hashtags based on style"""
        
        hashtag_sets = {
            "trendy": ["trending", "viral", "fyp", "explore", "mood"],
            "business": ["business", "entrepreneur", "success", "professional", "growth"],
            "lifestyle": ["lifestyle", "daily", "life", "vibes", "authentic"],
            "tech": ["tech", "innovation", "future", "digital", "ai"],
            "finance": ["finance", "investing", "money", "stocks", "wealth"],
            "fitness": ["fitness", "workout", "health", "strong", "motivation"]
        }
        
        return hashtag_sets.get(style, hashtag_sets["trendy"])
    
    def _generate_cta(self, style: str) -> Optional[str]:
        """Generate call-to-action text based on style"""
        
        cta_options = {
            "trendy": ["FOLLOW FOR MORE", "LIKE IF YOU AGREE", "SAVE THIS POST"],
            "business": ["LEARN MORE", "GET STARTED", "CONTACT US"],
            "lifestyle": ["FOLLOW MY JOURNEY", "SHARE YOUR STORY", "TAG A FRIEND"],
            "tech": ["TRY IT NOW", "LEARN MORE", "STAY UPDATED"],
            "finance": ["START INVESTING", "LEARN TO TRADE", "GET RICH"],
            "fitness": ["START TODAY", "GET FIT", "TRANSFORM NOW"]
        }
        
        options = cta_options.get(style, cta_options["trendy"])
        return random.choice(options) if random.random() > 0.3 else None  # 70% chance of CTA