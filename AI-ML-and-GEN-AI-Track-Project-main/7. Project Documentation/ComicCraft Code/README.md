# ComicCraft - AI Comic Story Creator

ComicCraft is a five-panel AI comic generator based on the supplied project specification. It uses FastAPI/Jinja2 for the web application, Gemini for the structured outline and story, Stable Diffusion through Hugging Face Diffusers for illustrations, and FPDF2 for PDF export.

## Project flow

1. User enters story prompt, character, setting, tone, and art style.
2. Gemini generates a structured five-panel outline.
3. Gemini expands the outline into narration, captions, dialogue, and image prompts.
4. Stable Diffusion generates one image per panel.
5. The panels are assembled and exported to PDF.

## Windows setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Edit `.env` with your credentials:

```env
GEMINI_API_KEY=your_key
HF_TOKEN=hf_your_token
DEMO_MODE=false
```

For a first smoke test without AI credentials, set `DEMO_MODE=true`.

## Run

```powershell
python run.py
```

Open http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

## Tests

```powershell
pytest -q
```

## Notes

Real Stable Diffusion generation is resource-intensive. CPU generation can be very slow. A CUDA-capable GPU is recommended for practical local image generation.

Never commit `.env` or expose API tokens. `.env.example` is the safe template to share.
