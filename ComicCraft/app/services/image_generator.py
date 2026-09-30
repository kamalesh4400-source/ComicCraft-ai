from pathlib import Path
from threading import Lock
from PIL import Image, ImageDraw
from app.config import settings
from app.utils.files import safe_filename

_pipeline = None
_pipeline_lock = Lock()

def _placeholder_image(prompt: str, output_path: Path) -> None:
    image = Image.new("RGB", (settings.image_width, settings.image_height), "#f5ead7")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, settings.image_width - 16, settings.image_height - 16), outline="#222222", width=6)
    draw.text((32, 32), "ComicCraft\nDemo Panel", fill="#111111", spacing=8)
    draw.text((32, settings.image_height - 120), prompt[:180], fill="#333333")
    image.save(output_path)

def _load_pipeline():
    global _pipeline
    if _pipeline is not None:
        return _pipeline
    with _pipeline_lock:
        if _pipeline is not None:
            return _pipeline
        try:
            import torch
            from diffusers import StableDiffusionPipeline
        except ImportError as exc:
            raise RuntimeError("Install image dependencies with: pip install -r requirements-image.txt") from exc

        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        kwargs = {"torch_dtype": dtype}
        if settings.hf_api_key:
            kwargs["token"] = settings.hf_api_key

        _pipeline = StableDiffusionPipeline.from_pretrained(settings.diffusion_model_id, **kwargs)
        _pipeline = _pipeline.to("cuda" if torch.cuda.is_available() else "cpu")
        if torch.cuda.is_available():
            try:
                _pipeline.enable_attention_slicing()
            except Exception:
                pass
    return _pipeline

def generate_image(prompt: str, panel_number: int) -> str:
    filename = safe_filename(f"panel_{panel_number}")
    output_path = settings.panels_dir / filename
    provider = settings.image_provider.lower().strip()

    if settings.mock_ai or provider == "placeholder":
        _placeholder_image(prompt, output_path)
    elif provider == "diffusers":
        pipeline = _load_pipeline()
        result = pipeline(
            prompt=prompt,
            num_inference_steps=settings.image_steps,
            guidance_scale=settings.image_guidance_scale,
            height=settings.image_height,
            width=settings.image_width,
        )
        result.images[0].save(output_path)
    else:
        raise RuntimeError(f"Unsupported IMAGE_PROVIDER={settings.image_provider!r}. Use diffusers or placeholder.")

    return f"/static/panels/{filename}"
