import numpy as np
import moviepy.editor as mp

print("Testing basic MoviePy...")

# Create a simple 5-second video
def make_frame(t):
    return np.random.randint(0, 255, (1920, 1080, 3), dtype=np.uint8)

try:
    video = mp.VideoClip(make_frame, duration=5)
    video.write_videofile("test_output.mp4", fps=15, verbose=False, logger=None)
    print("SUCCESS: Basic video created!")
except Exception as e:
    print(f"ERROR: {e}")