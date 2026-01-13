"""Redimensionamento pixel art com autocrop e transparência."""

from PIL import Image
from ..utils import _ensure_png


class ResizeModule:
    """Downscale/upscale com NEAREST (pixel art) e autocrop."""

    def __init__(self, image: Image.Image):
        self.image = image

    def _crop_transparent(self) -> "ResizeModule":
        """Autocrop: remove áreas transparentes/vazias."""
        if self.image.mode == "RGBA":
            bbox = self.image.getbbox()
            if bbox:
                self.image = self.image.crop(bbox)
        return self

    def downscale(self, target_size: tuple) -> "ResizeModule":
        """Reduz mantendo pixels nítidos (NEAREST)."""
        self.image = self.image.resize(target_size, resample=Image.NEAREST)
        print(f"[INFO] [ResizeModule] downscale applied {target_size}")
        return self

    def upscale_for_export(self, factor: int) -> "ResizeModule":
        """Aumenta por fator mantendo pixels nítidos."""
        new_size = (self.image.width * factor, self.image.height * factor)
        self.image = self.image.resize(new_size, resample=Image.NEAREST)
        print(f"[INFO] [ResizeModule] upscale applied (factor={factor})")
        return self

    def save(self, output_path: str) -> None:
        """Autocrop + PNG com transparência."""
        self._crop_transparent()
        output_path = _ensure_png(output_path)
        self.image.save(output_path, 'PNG')
        print(f"[INFO] [ResizeModule] output saved: {output_path}")
