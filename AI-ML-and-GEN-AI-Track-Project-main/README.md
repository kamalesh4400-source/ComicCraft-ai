# AI-ML-and-GEN-AI-Track-Project-main

## ComicCraft – AI Comic Story Creator using Gemini Models

### Team Details
- **Team ID:** SWTID-2026-1254
- **Team Leader:** Kamalesh S
- **Team Members:**
  - Tamilselvan P
  - Tamilselvam K
  - Mugunthan S
  - Suriya L

### Project Summary
ComicCraft is a web-based AI application that generates personalized comic stories and illustrations from user-provided creative prompts. It uses FastAPI for the backend, Google Gemini models for story generation, Stable Diffusion for comic-style image generation, and PDF export for the final comic.

### Submission Structure
1. Brainstorming & Ideation
2. Requirement Analysis
3. Project Design Phase
4. Project Planning Phase
5. Project Development Phase
6. Project Testing
7. Project Documentation
8. Project Demonstration

### Technology Stack
- Python / FastAPI / Uvicorn
- Google Gemini models
- Hugging Face Diffusers / Stable Diffusion
- HTML, CSS, Jinja2
- FPDF

### Run the Application
```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
pip install -r "7. Project Documentation/ComicCraft Code/requirements.txt"
uvicorn app.main:app --reload
```

Configure the required `GEMINI_API_KEY` and `HF_API_KEY` environment variables before running.
