from __future__ import annotations

from pathlib import Path
import re
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from app.config import settings


def _safe_name(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text[:50] or "panel"


def _public_panel_path(filename: str) -> str:
    return f"{settings.panel_dir.replace(chr(92), '/')}/{filename}"


class ImageGenerator:
    def __init__(self) -> None:
        self._pipeline = None
        self._device = None

    def _select_device(self) -> str:
        if settings.device.lower() != "auto":
            return settings.device.lower()
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def _load_pipeline(self):
        if self._pipeline is not None:
            return self._pipeline
        if not settings.hf_token:
            raise RuntimeError("HF_TOKEN is missing. Add your Hugging Face token to .env.")

        import torch
        from diffusers import StableDiffusionPipeline

        device = self._select_device()
        dtype = torch.float16 if device in {"cuda", "mps"} else torch.float32
        kwargs = {"torch_dtype": dtype, "use_safetensors": True, "token": settings.hf_token}
        self._pipeline = StableDiffusionPipeline.from_pretrained(settings.diffusion_model, **kwargs)
        self._pipeline = self._pipeline.to(device)
        if device == "cuda":
            self._pipeline.enable_attention_slicing()
        self._device = device
        return self._pipeline

    def generate_demo(self, prompt: str, panel_number: int) -> str:
        filename = f"demo-panel-{panel_number}.png"
        path = settings.panel_path / filename
        image = Image.new("RGB", (settings.image_width, settings.image_height), "#dbeafe")
        draw = ImageDraw.Draw(image)
        draw.rectangle((20, 20, settings.image_width - 20, settings.image_height - 20), outline="#1e3a8a", width=5)
        draw.ellipse((170, 100, 340, 270), fill="#f59e0b", outline="#111827", width=4)
        draw.ellipse((210, 150, 230, 170), fill="#111827")
        draw.ellipse((280, 150, 300, 170), fill="#111827")
        draw.arc((220, 175, 290, 225), 0, 180, fill="#111827", width=4)
        draw.polygon([(255, 115), (225, 70), (250, 90)], fill="#f59e0b", outline="#111827")
        draw.polygon([(255, 115), (285, 70), (270, 95)], fill="#f59e0b", outline="#111827")
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except OSError:
            font = ImageFont.load_default()
        draw.text((35, 35), f"DEMO PANEL {panel_number}", fill="#111827", font=font)
        draw.text((35, 440), "Demo artwork - enable real mode for Stable Diffusion", fill="#111827", font=font)
        image.save(path, "PNG")
        return _public_panel_path(filename)

    def generate(self, prompt: str, panel_number: int) -> str:
        if settings.demo_mode:
            return self.generate_demo(prompt, panel_number)
        if settings.image_provider.lower() != "diffusers":
            raise RuntimeError(f"Unsupported IMAGE_PROVIDER: {settings.image_provider}")

        pipeline = self._load_pipeline()
        result = pipeline(
            prompt,
            num_inference_steps=settings.image_steps,
            guidance_scale=settings.image_guidance_scale,
            width=settings.image_width,
            height=settings.image_height,
        )
        image = result.images[0]
        filename = f"panel-{panel_number}-{_safe_name(prompt)}.png"
        path = settings.panel_path / filename
        image.save(path, "PNG")
        return _public_panel_path(filename)


image_generator = ImageGenerator()


def generate_image(prompt: str, panel_number: int) -> str:
    return image_generator.generate(prompt, panel_number)
