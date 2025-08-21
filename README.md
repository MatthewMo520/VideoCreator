# 🎬 AI Reel Generator

Create viral reels instantly with AI-powered content generation! This tool analyzes trending content and generates engaging short-form videos automatically.

## ✨ Features

- **🤖 AI Video Generation**: Convert text prompts into engaging video content
- **📸 Image Integration**: Upload your own images (like stock gains) to include in reels
- **🎵 Smart Audio**: Automatic background music generation based on content style
- **📊 Trend Analysis**: Real-time trending hashtags and content patterns
- **🎨 Multiple Styles**: Finance, Business, Lifestyle, Tech, Fitness, and Trendy
- **📱 Mobile-Ready**: Optimized for 9:16 aspect ratio (Instagram Reels/TikTok)
- **🔥 Viral Elements**: Automatic trending text overlays and effects

## 🚀 Quick Start

### Option 1: One-Click Start (Recommended)
```bash
python run.py
```

The application will automatically:
- Check and install dependencies
- Set up required directories
- Start both backend and frontend servers
- Open your browser to the application

### Option 2: Manual Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Start Backend**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. **Start Frontend** (in new terminal)
```bash
cd frontend
python -m http.server 3000
```

4. **Open Application**
Navigate to: http://localhost:3000

## 💡 Usage Examples

### Finance Reels
Perfect for stock traders and investors:
- **Prompt**: "My top 3 stocks that gained 500% this year"
- **Style**: Finance
- **Upload**: Screenshot of your portfolio gains
- **Result**: Professional reel with stock tickers and gain highlights

### Business Content
For entrepreneurs and professionals:
- **Prompt**: "5 habits that made me successful"
- **Style**: Business
- **Result**: Clean, professional reel with motivational text overlays

### Lifestyle Content
For personal brand building:
- **Prompt**: "My morning routine for productivity"
- **Style**: Lifestyle
- **Result**: Casual, authentic-feeling reel with lifestyle aesthetics

## 🎯 Content Styles

| Style | Best For | Characteristics |
|-------|----------|----------------|
| 🔥 **Trendy** | Viral content, general audience | Bright colors, energetic transitions, trending audio |
| 💼 **Business** | Professional content, B2B | Clean design, corporate aesthetics, professional audio |
| ✨ **Lifestyle** | Personal brand, lifestyle tips | Warm tones, casual feel, authentic vibes |
| 🚀 **Tech** | Technology, innovation | Futuristic design, digital effects, tech aesthetics |
| 📈 **Finance** | Trading, investing, money tips | Green/red colors, chart overlays, professional tone |
| 💪 **Fitness** | Workouts, health, motivation | High energy, bold colors, motivational text |

## 🛠️ System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended for AI features)
- **Storage**: 2GB free space for models and cache
- **GPU**: Optional (CUDA-compatible GPU speeds up AI generation)

## 📁 Project Structure

```
VideoCreator/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API server
│   ├── video_generator.py  # Core video generation
│   ├── ai_models.py        # AI text-to-video models
│   ├── trend_analyzer.py   # Trending content analysis
│   ├── text_overlay.py     # Text generation and styling
│   └── audio_processor.py  # Audio generation and processing
├── frontend/               # Web interface
│   └── index.html         # Main application UI
├── uploads/               # Uploaded images/audio
├── outputs/              # Generated videos
├── temp/                 # Temporary files
├── models/               # Cached AI models
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── run.py               # One-click startup script
```

## ⚙️ Configuration

Copy `.env.example` to `.env` and configure:

```env
# Optional API keys for premium features
ELEVENLABS_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# App settings
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Enable GPU acceleration (if available)
USE_GPU=True
```

## 🔧 Advanced Features

### Custom Audio
- Upload your own audio files
- Automatic audio generation based on content style
- Beat detection for transition timing

### AI Enhancement
- Text-to-video generation using Stable Diffusion
- Automatic image-to-video conversion
- Smart text overlay positioning

### Trend Integration
- Real-time hashtag analysis
- Popular audio detection
- Viral content pattern recognition

## 🎯 Use Cases

### Content Creators
- Generate multiple variations quickly
- Test different styles and approaches
- Maintain consistent posting schedule

### Businesses
- Create product showcase reels
- Share company updates
- Build brand awareness

### Personal Brands
- Share achievements and milestones
- Create educational content
- Build following with trending content

## 🔍 Troubleshooting

### Common Issues

**"Module not found" errors**
```bash
pip install -r requirements.txt --upgrade
```

**Video generation fails**
```bash
# Check if FFmpeg is installed
ffmpeg -version

# Install FFmpeg if missing (Windows)
# Download from https://ffmpeg.org/download.html
```

**GPU not detected**
```bash
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Server won't start**
- Check if ports 8000 and 3000 are available
- Try different ports in the configuration

## 🚨 Performance Tips

1. **Use GPU**: Enable GPU acceleration for faster AI generation
2. **Smaller Images**: Resize large images before uploading
3. **Shorter Videos**: Start with 15-second reels for faster processing
4. **Cache Models**: AI models are cached after first use

## 🔐 Privacy & Security

- All processing happens locally on your machine
- No data is sent to external servers (except for trending analysis)
- Generated videos are stored only on your device
- Optional API integrations require your own keys

## 📈 Roadmap

- [ ] Advanced AI video models (Runway ML, Pika Labs integration)
- [ ] Real-time social media trend scraping
- [ ] Automated posting to platforms
- [ ] Voice cloning and custom narration
- [ ] Batch generation for multiple ideas
- [ ] Analytics and performance tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - Feel free to use this for personal and commercial projects!

## 🙏 Acknowledgments

- Stable Diffusion for AI image generation
- MoviePy for video processing
- FastAPI for the backend framework
- All the open-source libraries that make this possible

---

**Happy Reel Creating! 🎬✨**

For support or questions, please open an issue in the repository.