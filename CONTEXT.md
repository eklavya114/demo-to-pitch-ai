# Autonomous SDR Visual Intel: System Architecture & Context

## Project Overview
This project is a Python Streamlit application built to extract visual intelligence from YouTube videos. It serves as an Autonomous Sales Development Representative (SDR) tool by processing short video snippets to understand visual context using a Large Language Model.

## Core Directives & Constraints
1. **Framework**: Python 3.x, Streamlit for Frontend/UI.
2. **AI Model Integration**: Must STRICTLY use the `huggingface_hub` Inference API for the `google/gemma-4-31B-it` model.
3. **Firm Constraint**: Do NOT use the `transformers` library to download or run model weights locally. All inferences must be performed remotely via the API to conserve local compute.
4. **File System Handling**: Ensure robust temporary file management. All media artifacts MUST be stored and manipulated within a locally synthesized `./temp` directory, which should be cleaned up post-processing.

## Architecture Modules

### 1. Media Acquisition (yt-dlp)
- **Core Library**: `yt-dlp` (via Python wrapper or Subprocess Shell command)
- **Logic**: Fetch the media stream from a provided YouTube URL.
- **Ruleset**: Download *only* the first 3 minutes of the stream to optimize pipeline execution speed.
- **Output**: A local temporary video file saved in `./temp/`.

### 2. Video Processing (ffmpeg)
- **Core Engine**: `ffmpeg`
- **Logic**: Process the locally downloaded video file to extract representative visual frames.
- **Ruleset**: Extract exactly 1 frame every 5 seconds (using `fps=1/5` filter).
- **Output**: A sequence of image files stored in an isolated subdirectory, e.g., `./temp/frames/`.

### 3. AI Intelligence Hub (Hugging Face API)
- **Core Library**: `huggingface_hub` (`InferenceClient`)
- **Logic**: Interface to communicate with `google/gemma-4-31B-it`. Construct conversational prompts combining SDR analytical directives with descriptions or converted representations of the visual frames.
- **API Flow**: Provide User Prompts via the Serverless Inference API endpoints securely, returning structured intelligence on the visual context.

### 4. Interactive Frontend (Streamlit)
- **Core Library**: `streamlit`
- **Logic**: Provide a minimal, clean, responsive UI:
  1. Input field for the YouTube URL.
  2. Single call-to-action (CTA) button to trigger the pipeline.
  3. Interactive progress states: Downloading -> Extracting Frames -> AI Synthesizing Insights.
  4. Final View: Display the extracted frames alongside the AI-generated intelligence report.
