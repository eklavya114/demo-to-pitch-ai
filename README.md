# Autonomous SDR Visual Intel

An AI-powered tool that acts as an Autonomous Sales Development Representative. It accepts a YouTube software demo URL, extracts keyframes using `yt-dlp` and `ffmpeg`, and uses the Google Gemini API to analyze the UI for friction points and automatically draft highly personalized cold outreach emails.

## Tech Stack
* **Frontend:** Streamlit
* **Video Pipeline:** yt-dlp, ffmpeg, subprocess
* **AI Model:** Gemini Pro/Flash (via Google Generative AI API)

## Local Setup
1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file and add your token: `GEMINI_API_KEY=your_api_key`
5. Run the app: `streamlit run app.py`
