import os
import subprocess
import shutil
import sys

FFMPEG_EXE = "ffmpeg"

TEMP_DIR = "./temp"
FRAMES_DIR = os.path.join(TEMP_DIR, "frames")
VIDEO_PATH = os.path.join(TEMP_DIR, "vid.mp4")

def ensure_dirs():
    """Ensure that the required temporary directories exist."""
    os.makedirs(FRAMES_DIR, exist_ok=True)

def clean_temp_dir():
    """Delete the ./temp directory and all its contents."""
    print("Cleaning up temporary directory...")
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
    print("Cleanup complete.")

def download_video(url: str):
    """
    Downloads only the first 3 minutes of the YouTube video using yt-dlp.
    Saves the video to ./temp/vid.mp4
    """
    print(f"Downloading first 3 minutes of {url}...")
    ensure_dirs()
    
    command = [
        sys.executable, "-m", "yt_dlp",
        "--download-sections", "*00:00:00-00:03:00",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--force-overwrites",
        "-o", VIDEO_PATH,
        url
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp error: {result.stderr}")
        
    if not os.path.exists(VIDEO_PATH):
        raise FileNotFoundError(f"Video file was not found at {VIDEO_PATH} after download.")
        
    print("Download complete.")
    return VIDEO_PATH

def extract_frames():
    """
    Extracts 1 frame every 5 seconds from the downloaded video using ffmpeg.
    Saves the frames to ./temp/frames/
    """
    print("Extracting frames (1 frame every 5 seconds)...")
    ensure_dirs()
    
    if not os.path.exists(VIDEO_PATH):
        raise FileNotFoundError(f"Source video not found at {VIDEO_PATH}")
        
    output_pattern = os.path.join(FRAMES_DIR, "frame_%04d.jpg")
    
    command = [
        FFMPEG_EXE,
        "-i", VIDEO_PATH,
        "-vf", "fps=1/5",
        "-y",  # Overwrite output files without asking
        output_pattern
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {result.stderr}")
        
    extracted_files = [f for f in os.listdir(FRAMES_DIR) if f.endswith(".jpg")]
    if not extracted_files:
        raise RuntimeError("No frames were extracted. Please check the video length.")
        
    print(f"Extracted {len(extracted_files)} frames.")
    
    # Return full paths to the sorted frames
    return sorted([os.path.join(FRAMES_DIR, f) for f in extracted_files])

def process_youtube_video(url: str):
    """
    Orchestrates the download and frame extraction process.
    Returns a list of image paths.
    """
    # Defensive cleanup to ensure fresh state if previous run failed
    clean_temp_dir() 
    ensure_dirs()
    
    try:
        download_video(url)
        frames = extract_frames()
        return frames
    except Exception as e:
        print(f"Failed to process video: {e}")
        # Not calling clean_temp_dir() here to allow debugging, but can be added if strict
        raise
