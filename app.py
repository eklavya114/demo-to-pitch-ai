import streamlit as st
import traceback

from processor import download_video, extract_frames, clean_temp_dir
from ai_client import generate_pitch

st.set_page_config(
    page_title="Autonomous SDR Visual Intel",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
/* Hide Streamlit branding and top padding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {
    padding-top: 2rem !important;
    max-width: 900px !important;
}

/* Professional Dark SaaS Background */
.stApp {
    background-color: #0A0A0A !important;
    background-image: radial-gradient(circle at 50% 0%, #1A1A1A 0%, #0A0A0A 70%) !important;
    color: #EDEDED !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Sleek Input Field */
.stTextInput > div > div > input {
    background-color: #121212 !important;
    color: #FFFFFF !important;
    border: 1px solid #333333 !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    transition: border-color 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #0070F3 !important; /* Professional Blue */
    box-shadow: 0 0 0 1px #0070F3 !important;
}

/* High-End CTA Button */
.stButton > button {
    background-color: #EDEDED !important;
    color: #0A0A0A !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background-color: #FFFFFF !important;
    transform: scale(0.99) !important;
}

/* Fix Status Widget & Expander White Background Issue */
[data-testid="stStatusWidget"] > div,
[data-testid="stExpander"] > div,
[data-baseweb="accordion"] > div,
[data-baseweb="accordion"] div {
    background-color: #121212 !important;
    color: #EDEDED !important;
    border-color: #333333 !important;
}

[data-testid="stStatusWidget"] label,
[data-testid="stStatusWidget"] p,
[data-testid="stStatusWidget"] span {
    color: #EDEDED !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Autonomous SDR Visual Intel")
st.markdown("""
Welcome to the internal SDR intel tool. Please drop a YouTube logic or software demo link here. 
We will clip the first 3 minutes, extract strategic keyframes, and generate a highly personalized outreach email based on visual UI friction.
""")

url_input = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Generate Pitch", type="primary"):
    if not url_input.strip():
        st.error("Please provide a valid YouTube URL.")
    else:
        pitch_content = ""
        frames_list = []
        
        try:
            with st.status("🧠 Processing Pipeline Engine", expanded=True) as status:
                st.write("📥 Downloading Video (capturing first 3 mins)...")
                download_video(url_input)
                
                st.write("🎞️ Extracting intelligence frames (1 per 5 secs)...")
                frames_list = extract_frames()
                
                st.write(f"🚀 Analyzing {len(frames_list)} frames with Google Gemini 1.5 Flash...")
                pitch_content = generate_pitch(frames_list)
                
                status.update(label="Task Complete!", state="complete", expanded=False)

            st.success("Analysis successful! Review the draft below.")
            
            import re
            formatted_pitch = pitch_content
            formatted_pitch = re.sub(r'###\s+(.*)', r'<h4 style="color:#FFFFFF; margin-top:16px; margin-bottom:8px;">\1</h4>', formatted_pitch)
            formatted_pitch = re.sub(r'\*\*(.*?)\*\*', r'<b style="color:#FFFFFF;">\1</b>', formatted_pitch)
            formatted_pitch = formatted_pitch.replace('* **', '• **')
            formatted_pitch = formatted_pitch.replace('\n', '<br>')
            st.markdown(f'''
<div style="background-color: #111111; border: 1px solid #222222; border-radius: 12px; padding: 24px; box-shadow: 0 4px 24px rgba(0,0,0,0.5); margin-top: 24px; margin-bottom: 24px;">
  <h3 style="color: #888888; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">Generated Pitch</h3>
  <div style="color: #EDEDED; line-height: 1.6; font-size: 16px;">
     {formatted_pitch}
  </div>
</div>
''', unsafe_allow_html=True)
            
            with st.expander("View AI Processed Frames"):
                cols = st.columns(3)
                for index, f_path in enumerate(frames_list):
                    cols[index % 3].image(f_path, use_container_width=True, caption=f"Frame {index+1}")
                    
        except Exception as e:
            st.error("An error occurred during processing.")
            with st.expander("View specific error details"):
                st.code(traceback.format_exc())
        finally:
            clean_temp_dir()
