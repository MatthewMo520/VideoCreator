import requests
from bs4 import BeautifulSoup
import json
import random
from typing import Dict, List, Optional
import time
from datetime import datetime, timedelta
import re

class TrendAnalyzer:
    def __init__(self):
        self.cache = {}
        self.cache_duration = 3600  # 1 hour cache
        
        # Fallback trending data when scraping fails
        self.fallback_trends = {
            "hashtags": ["viral", "trending", "fyp", "explore", "mood", "aesthetic", "motivation"],
            "sounds": ["trending_beat_1", "viral_audio_2", "popular_sound_3"],
            "effects": {
                "flash_transitions": True,
                "zoom_effects": True,
                "text_animations": True,
                "color_filters": ["vintage", "vibrant", "dark_mode"]
            },
            "topics": ["self_improvement", "lifestyle", "business_tips", "motivation", "success"],
            "video_styles": {
                "quick_cuts": True,
                "vertical_format": True,
                "hook_first_3_seconds": True,
                "strong_cta": True
            }
        }
    
    async def get_trending_data(self) -> Dict:
        """Get current trending data from multiple sources"""
        
        cache_key = "trending_data"
        current_time = time.time()
        
        # Check cache first
        if (cache_key in self.cache and 
            current_time - self.cache[cache_key]['timestamp'] < self.cache_duration):
            return self.cache[cache_key]['data']
        
        try:
            # Combine data from multiple sources
            trending_data = {
                "hashtags": await self._get_trending_hashtags(),
                "sounds": await self._get_trending_sounds(),
                "effects": await self._get_trending_effects(),
                "topics": await self._get_trending_topics(),
                "video_styles": await self._get_video_style_trends(),
                "timestamp": current_time
            }
            
            # Cache the result
            self.cache[cache_key] = {
                "data": trending_data,
                "timestamp": current_time
            }
            
            return trending_data
            
        except Exception as e:
            print(f"Error fetching trending data: {e}")
            # Return fallback data with some randomization
            return self._get_randomized_fallback()
    
    async def _get_trending_hashtags(self) -> List[str]:
        """Scrape trending hashtags from various sources"""
        
        hashtags = []
        
        try:
            # Try to get some trending topics (simplified)
            # In a real implementation, you'd use proper social media APIs
            
            # Simulate trending hashtags with some real ones that are often popular
            base_hashtags = [
                "viral", "trending", "fyp", "foryou", "explore", "reels", "tiktok",
                "motivation", "success", "mindset", "hustle", "entrepreneur",
                "lifestyle", "aesthetic", "mood", "vibes", "energy",
                "fitness", "health", "workout", "gains", "strong",
                "money", "wealth", "investing", "crypto", "stocks",
                "tech", "ai", "innovation", "future", "digital",
                "fashion", "style", "outfit", "ootd", "beauty",
                "food", "recipe", "cooking", "delicious", "yummy",
                "travel", "adventure", "wanderlust", "vacation", "explore"
            ]
            
            # Add some time-based trending hashtags
            current_month = datetime.now().strftime("%B").lower()
            current_year = datetime.now().year
            
            seasonal_hashtags = {
                "january": ["newyear", "resolution", "goals", "fresh_start"],
                "february": ["love", "valentine", "heart", "romance"],
                "march": ["spring", "fresh", "growth", "renewal"],
                "april": ["easter", "spring", "bloom", "new_life"],
                "may": ["spring", "flowers", "mothers_day", "bloom"],
                "june": ["summer", "sunshine", "vacation", "fathers_day"],
                "july": ["summer", "freedom", "independence", "vacation"],
                "august": ["summer", "vacation", "back_to_school", "memories"],
                "september": ["fall", "autumn", "school", "harvest"],
                "october": ["halloween", "spooky", "autumn", "scary"],
                "november": ["thanksgiving", "grateful", "thankful", "family"],
                "december": ["christmas", "holiday", "winter", "celebration"]
            }
            
            if current_month in seasonal_hashtags:
                base_hashtags.extend(seasonal_hashtags[current_month])
            
            # Randomly select trending hashtags
            hashtags = random.sample(base_hashtags, min(15, len(base_hashtags)))
            
        except Exception as e:
            print(f"Error getting trending hashtags: {e}")
            hashtags = self.fallback_trends["hashtags"]
        
        return hashtags
    
    async def _get_trending_sounds(self) -> List[str]:
        """Get trending audio/sound information"""
        
        try:
            # In a real implementation, you'd integrate with music APIs
            # For now, return some generic trending sound categories
            
            sound_categories = [
                "upbeat_electronic",
                "hip_hop_beat",
                "acoustic_chill",
                "motivational_music",
                "trending_tiktok_sound",
                "viral_audio_clip",
                "background_music_trending",
                "energetic_workout_music",
                "calm_aesthetic_sound",
                "business_presentation_music"
            ]
            
            return random.sample(sound_categories, 5)
            
        except Exception as e:
            print(f"Error getting trending sounds: {e}")
            return self.fallback_trends["sounds"]
    
    async def _get_trending_effects(self) -> Dict:
        """Get trending video effects and filters"""
        
        try:
            effects = {
                "flash_transitions": random.choice([True, False]),
                "zoom_effects": True,  # Always popular
                "text_animations": True,  # Always popular
                "color_filters": [],
                "transitions": [],
                "overlays": []
            }
            
            # Popular color filters
            color_filters = [
                "vintage", "vibrant", "dark_mode", "neon", "sepia", 
                "black_white", "high_contrast", "warm_tone", "cool_tone"
            ]
            effects["color_filters"] = random.sample(color_filters, 3)
            
            # Popular transitions
            transitions = [
                "quick_cut", "fade", "zoom_in", "zoom_out", "slide", 
                "spin", "flash", "crossfade", "wipe"
            ]
            effects["transitions"] = random.sample(transitions, 4)
            
            # Popular overlays
            overlays = [
                "trending_text", "emoji_burst", "particle_effects", 
                "light_leaks", "film_grain", "glitch_effect"
            ]
            effects["overlays"] = random.sample(overlays, 3)
            
            return effects
            
        except Exception as e:
            print(f"Error getting trending effects: {e}")
            return self.fallback_trends["effects"]
    
    async def _get_trending_topics(self) -> List[str]:
        """Get trending content topics"""
        
        try:
            # Categories of trending topics
            topics = [
                "self_improvement", "motivation", "success_tips", "mindset",
                "lifestyle_hacks", "productivity", "morning_routine", "habits",
                "business_tips", "entrepreneur_life", "side_hustle", "passive_income",
                "fitness_transformation", "workout_motivation", "healthy_living",
                "fashion_trends", "style_tips", "outfit_ideas", "beauty_hacks",
                "travel_tips", "adventure", "bucket_list", "wanderlust",
                "food_hacks", "recipe_tips", "cooking_secrets", "meal_prep",
                "tech_tips", "life_hacks", "organization", "decluttering",
                "relationship_advice", "dating_tips", "friendship_goals",
                "study_tips", "career_advice", "interview_tips", "skill_building"
            ]
            
            return random.sample(topics, 10)
            
        except Exception as e:
            print(f"Error getting trending topics: {e}")
            return self.fallback_trends["topics"]
    
    async def _get_video_style_trends(self) -> Dict:
        """Get trending video style preferences"""
        
        try:
            styles = {
                "quick_cuts": True,  # Always trending
                "vertical_format": True,  # Essential for reels
                "hook_first_3_seconds": True,  # Critical for engagement
                "strong_cta": random.choice([True, False]),
                "text_overlay_heavy": random.choice([True, False]),
                "emoji_usage": True,
                "trending_audio": True,
                "face_focus": random.choice([True, False]),
                "before_after": random.choice([True, False]),
                "tutorial_style": random.choice([True, False]),
                "storytelling": True,
                "authentic_casual": random.choice([True, False]),
                "high_energy": random.choice([True, False])
            }
            
            return styles
            
        except Exception as e:
            print(f"Error getting video style trends: {e}")
            return self.fallback_trends["video_styles"]
    
    def _get_randomized_fallback(self) -> Dict:
        """Get fallback trending data with some randomization"""
        
        fallback = self.fallback_trends.copy()
        
        # Randomize the order and selection
        fallback["hashtags"] = random.sample(fallback["hashtags"], 5)
        fallback["sounds"] = random.sample(fallback["sounds"], 3)
        fallback["topics"] = random.sample(fallback["topics"], 7)
        
        # Add timestamp
        fallback["timestamp"] = time.time()
        
        return fallback
    
    async def get_style_specific_trends(self, style: str) -> Dict:
        """Get trending data specific to a content style"""
        
        base_trends = await self.get_trending_data()
        
        # Customize trends based on style
        style_specific = {
            "finance": {
                "hashtags": ["stocks", "investing", "money", "wealth", "trading", "crypto"],
                "topics": ["stock_tips", "investment_strategy", "financial_freedom", "passive_income"],
                "effects": {"green_red_colors": True, "chart_overlays": True}
            },
            "fitness": {
                "hashtags": ["workout", "fitness", "gains", "strong", "health", "gym"],
                "topics": ["workout_routine", "fitness_motivation", "transformation", "healthy_living"],
                "effects": {"energetic_transitions": True, "before_after": True}
            },
            "business": {
                "hashtags": ["entrepreneur", "business", "success", "hustle", "mindset"],
                "topics": ["business_tips", "entrepreneur_life", "success_mindset", "leadership"],
                "effects": {"professional_style": True, "clean_transitions": True}
            },
            "tech": {
                "hashtags": ["tech", "ai", "innovation", "digital", "future", "coding"],
                "topics": ["tech_tips", "ai_news", "coding_tips", "innovation", "future_tech"],
                "effects": {"digital_effects": True, "neon_colors": True}
            }
        }
        
        if style in style_specific:
            # Merge style-specific trends with base trends
            customized = base_trends.copy()
            style_data = style_specific[style]
            
            # Prioritize style-specific hashtags
            customized["hashtags"] = style_data["hashtags"] + base_trends["hashtags"][:5]
            customized["topics"] = style_data["topics"] + base_trends["topics"][:5]
            
            # Merge effects
            if "effects" in style_data:
                customized["effects"].update(style_data["effects"])
            
            return customized
        
        return base_trends