"""Módulo de remoção de fundo para PixSkin."""

import os
from PIL import Image
from rembg import remove
from ..utils import _ensure_png


class InputImage:
    """Remove fundo de imagem e prepara para pipeline (RGBA + PNG)."""

    def __init__(self, image_path: str, auto_process: bool = False):
        self.path = image_path
        self.raw_image = Image.open(self.path)
        self.processed_image = None
        self.prepared_image = None
        
        if auto_process:
            self.process()

    def remove_background(self) -> "InputImage":
        """Remove fundo usando IA. Atualiza estado interno."""
        self.processed_image = remove(self.raw_image)
        print(f"[INFO] [InputImage] background removed: {os.path.basename(self.path)}")
        return self

    def prepare_for_pipeline(self) -> "InputImage":
        """Converte para RGBA. Atualiza estado interno."""
        source = self.processed_image or self.raw_image
        self.prepared_image = source.convert("RGBA")
        return self

    def process(self) -> "InputImage":
        """Remove fundo + prepara para pipeline."""
        return self.remove_background().prepare_for_pipeline()

    def save_prepared(self, output_path: str) -> None:
        """Salva imagem preparada (transparência preservada em PNG)."""
        if not self.prepared_image:
            raise RuntimeError("Nenhuma imagem preparada. Execute process() primeiro.")
        
        output_path = _ensure_png(output_path)
        self.prepared_image.save(output_path, 'PNG')
        print(f"[INFO] [InputImage] output saved: {output_path}")
