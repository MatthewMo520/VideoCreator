#!/usr/bin/env python3
"""
AI Reel Generator - Main startup script
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"[OK] Python {sys.version.split()[0]} detected")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'opencv-python', 'pillow', 'moviepy',
        'transformers', 'torch', 'requests', 'beautifulsoup4'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  [OK] {package}")
        except ImportError:
            print(f"  [MISSING] {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade"
        ] + missing_packages)
        print("[OK] All dependencies installed!")
    else:
        print("[OK] All dependencies are installed!")

def setup_directories():
    """Create necessary directories"""
    print("Setting up directories...")
    
    directories = [
        'uploads', 'outputs', 'temp', 'models',
        'temp/audio_cache', 'static'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  [OK] {directory}")

def start_backend():
    """Start the FastAPI backend server"""
    print("Starting backend server...")
    
    os.chdir('backend')
    
    # Start uvicorn server
    cmd = [
        sys.executable, "-m", "uvicorn",
        "main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ]
    
    return subprocess.Popen(cmd)

def start_frontend():
    """Start the frontend server (simple HTTP server)"""
    print("🌐 Starting frontend server...")
    
    os.chdir('frontend')
    
    # Start simple HTTP server
    cmd = [
        sys.executable, "-m", "http.server", "3000"
    ]
    
    return subprocess.Popen(cmd)

def wait_for_server(url, timeout=30):
    """Wait for server to be ready"""
    import requests
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def open_browser():
    """Open the application in browser"""
    print("Opening application in browser...")
    webbrowser.open('http://localhost:3000')

def main():
    """Main function to start the application"""
    print("AI Reel Generator - Starting Application")
    print("=" * 50)
    
    # Check system requirements
    check_python_version()
    check_dependencies()
    setup_directories()
    
    # Change to project root
    os.chdir(Path(__file__).parent)
    
    try:
        # Start backend
        backend_process = start_backend()
        
        # Wait for backend to be ready
        print("Waiting for backend to start...")
        if not wait_for_server('http://localhost:8000'):
            print("[ERROR] Backend failed to start properly")
            backend_process.terminate()
            sys.exit(1)
        print("[OK] Backend is ready!")
        
        # Change back to project root for frontend
        os.chdir(Path(__file__).parent)
        
        # Start frontend
        frontend_process = start_frontend()
        
        # Wait for frontend to be ready
        print("Waiting for frontend to start...")
        if not wait_for_server('http://localhost:3000'):
            print("[ERROR] Frontend failed to start properly")
            backend_process.terminate()
            frontend_process.terminate()
            sys.exit(1)
        print("[OK] Frontend is ready!")
        
        # Open browser
        time.sleep(2)
        open_browser()
        
        print("\n🎉 Application is running!")
        print("📱 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\n💡 Tips:")
        print("  - Upload images of your gains for finance-style reels")
        print("  - Try different styles for different content types")
        print("  - Include trending elements for viral potential")
        print("\n⚠️  Press Ctrl+C to stop the application")
        
        # Keep the application running
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            backend_process.terminate()
            frontend_process.terminate()
            print("[OK] Application stopped successfully!")
            
    except Exception as e:
        print(f"[ERROR] Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()