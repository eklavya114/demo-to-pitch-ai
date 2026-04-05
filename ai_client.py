import os
import google.generativeai as genai
from PIL import Image

# Load environment variable via standard file reading if dotenv is missing
def load_env():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('GEMINI_API_KEY='):
                        os.environ['GEMINI_API_KEY'] = line.split('=', 1)[1]

def generate_pitch(frame_paths):
    """
    Constructs a multimodal payload with the extracted frames and fetches
    a localized cold outreach email from the Gemini API.
    """
    load_env()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables or .env file.")
        
    genai.configure(api_key=api_key)
    
    # We use Flash since it's the fastest and free tier is generous (15 RPM)
    # Gemini Pro is also free tier (2 RPM) but Flash is better for this use case
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    prompt = "Watch these frames from a software demo. Identify any UI/UX friction, loading lag, or error messages. Draft a short, highly personalized cold outreach email mentioning the specific timestamp and visual issue."
    
    content = [prompt]
    
    # Load each frame as a PIL Image which Google's SDK accepts natively
    images = []
    for path in frame_paths:
        img = Image.open(path)
        img.load()  # Make sure the image is fully loaded before closing
        content.append(img)
        images.append(img)
        
    print(f"Calling Gemini API with {len(frame_paths)} frames...")
    response = model.generate_content(content)
    
    # Close images
    for img in images:
        img.close()
        
    return response.text
