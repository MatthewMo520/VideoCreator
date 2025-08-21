from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from dotenv import load_dotenv
from typing import List, Optional
import json

from ai_content_generator import AIContentGenerator
from trend_analyzer import TrendAnalyzer

load_dotenv()

app = FastAPI(title="AI Reel Generator", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (ensure directories exist)
os.makedirs("../static", exist_ok=True)
os.makedirs("../outputs", exist_ok=True)
app.mount("/static", StaticFiles(directory="../static"), name="static")
app.mount("/outputs", StaticFiles(directory="../outputs"), name="outputs")

# Initialize components
video_generator = AIContentGenerator()
trend_analyzer = TrendAnalyzer()

@app.get("/")
async def root():
    return {"message": "AI Reel Generator API", "version": "1.0.0"}

@app.post("/generate-reel")
async def generate_reel(
    prompt: str = Form(...),
    style: str = Form(default="trendy"),
    duration: int = Form(default=15),
    images: List[UploadFile] = File(default=[]),
    audio: Optional[UploadFile] = File(default=None),
    include_trending: bool = Form(default=True)
):
    """Generate a reel based on prompt and optional media"""
    try:
        # Save uploaded files
        os.makedirs("../uploads", exist_ok=True)
        image_paths = []
        for img in images:
            if img.filename:
                img_path = f"../uploads/{img.filename}"
                with open(img_path, "wb") as f:
                    f.write(await img.read())
                image_paths.append(img_path)
        
        audio_path = None
        if audio and audio.filename:
            audio_path = f"../uploads/{audio.filename}"
            with open(audio_path, "wb") as f:
                f.write(await audio.read())
        
        # Get trending data if requested
        trending_data = None
        if include_trending:
            trending_data = await trend_analyzer.get_trending_data()
        
        # Generate the reel
        output_path = await video_generator.generate_reel(
            prompt=prompt,
            style=style,
            duration=duration,
            image_paths=image_paths,
            audio_path=audio_path,
            trending_data=trending_data
        )
        
        return {
            "success": True,
            "video_path": output_path,
            "download_url": f"/outputs/{os.path.basename(output_path)}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trends")
async def get_trends():
    """Get current trending data"""
    try:
        trends = await trend_analyzer.get_trending_data()
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/styles")
async def get_styles():
    """Get available video styles"""
    return {
        "styles": [
            {"id": "trendy", "name": "Trendy", "description": "Popular social media style"},
            {"id": "business", "name": "Business", "description": "Professional and clean"},
            {"id": "lifestyle", "name": "Lifestyle", "description": "Casual and personal"},
            {"id": "tech", "name": "Tech", "description": "Modern and sleek"},
            {"id": "finance", "name": "Finance", "description": "Stock market focused"},
            {"id": "fitness", "name": "Fitness", "description": "Health and wellness"},
        ]
    }

@app.delete("/cleanup")
async def cleanup_files():
    """Clean up temporary files"""
    try:
        # Clean uploads and temp directories
        for folder in ["../uploads", "../temp"]:
            if os.path.exists(folder):
                for file in os.listdir(folder):
                    file_path = os.path.join(folder, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
        return {"success": True, "message": "Cleanup completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8001)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )