# ComicCraft — AI Comic Story Creator

A complete FastAPI application that turns a story idea into a five-panel comic:
1. Gemini generates a structured panel outline.
2. Gemini expands it into captions, narration, and dialogue.
3. Hugging Face Diffusers generates panel illustrations when enabled.
4. A layout builder combines the panel data.
5. fpdf2 exports the comic as a multi-page PDF.

## Structure

```text
ComicCraft/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── services/
│   │   ├── comic_service.py
│   │   ├── gemini_flash.py
│   │   ├── gemini_pro.py
│   │   ├── image_generator.py
│   │   ├── layout_builder.py
│   │   └── exporters.py
│   └── utils/files.py
├── templates/
├── static/css/
├── tests/
├── .env.example
├── requirements.txt
├── requirements-image.txt
└── run.py
```

## Windows / VS Code

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For local Stable Diffusion:

```powershell
pip install -r requirements-image.txt
```

Copy `.env.example` to `.env`:

```powershell
copy .env.example .env
```

For a complete pipeline without external AI calls first:

```env
MOCK_AI=true
IMAGE_PROVIDER=placeholder
```

Then run:

```powershell
python run.py
```

Open http://127.0.0.1:8000 and API docs at http://127.0.0.1:8000/docs.

Run tests:

```powershell
pytest -q
```

## Real Gemini configuration

```env
GEMINI_API_KEY=your_key_here
MOCK_AI=false
GEMINI_OUTLINE_MODEL=gemini-2.5-flash
GEMINI_STORY_MODEL=gemini-2.5-pro
```

The project keeps the source document's `gemini_flash.py` and `gemini_pro.py` architecture, but uses Google's current `google-genai` SDK and configurable model names instead of hard-coding the older `google-generativeai` package.

## Real image generation

```env
IMAGE_PROVIDER=diffusers
DIFFUSION_MODEL_ID=stable-diffusion-v1-5/stable-diffusion-v1-5
```

Local Diffusers generation downloads model weights on first use and is much faster with a compatible GPU. For a laptop without suitable GPU memory, use `IMAGE_PROVIDER=placeholder` while developing.

## API

`POST /generate-comic/json`

```json
{
  "story_prompt": "A brave fox exploring an enchanted forest.",
  "character_name": "Lumi",
  "setting": "forest",
  "tone": "dramatic",
  "art_style": "comic book"
}
```

`POST /test-image`

```json
{"prompt":"A heroic fox in an enchanted forest, comic book illustration"}
```

`GET /health`

The browser workflow is `GET /` → `POST /generate` → comic preview → PDF download.

## Production hardening

Before public deployment, add authentication, rate limiting, background jobs for long image generation, persistent storage/database, moderation, logging, HTTPS, and secret management.
