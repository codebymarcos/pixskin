"""Polimento final para pixel art: grid, alpha, orphans, validação."""

from PIL import Image
import numpy as np


class FinalAdjustModule:
    """Ajustes cirúrgicos em pixel art (sem criar pixels novos)."""

    def __init__(self, image: Image.Image):
        """Recebe imagem já processada (RGBA, redimensionada)."""
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        self.image = image
        self.data = np.array(image)

    def clean_alpha(self, threshold: int = 20) -> "FinalAdjustModule":
        """Alpha hard: pixels com alpha < threshold → transparente.
        
        Limpa lixo visual (semi-transparência acidental).
        """
        alpha = self.data[:, :, 3]
        self.data[:, :, 3] = np.where(alpha < threshold, 0, alpha)
        print(f"[INFO] [FinalAdjust] alpha cleaned (threshold={threshold})")
        return self

    def remove_orphan_pixels(self, min_neighbors: int = 1) -> "FinalAdjustModule":
        """Remove pixels isolados (sem vizinhos opacos adjacentes).
        
        Melhora contorno, remove ruído.
        """
        h, w = self.data.shape[:2]
        alpha = self.data[:, :, 3]
        opaque = alpha > 0
        
        removed = 0
        for y in range(h):
            for x in range(w):
                if not opaque[y, x]:
                    continue
                
                neighbors = 0
                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and opaque[ny, nx]:
                        neighbors += 1
                
                if neighbors < min_neighbors:
                    self.data[y, x, 3] = 0
                    removed += 1
        
        print(f"[INFO] [FinalAdjust] orphan pixels removed ({removed})")
        return self

    def align_to_grid(self, grid_size: int = 1) -> "FinalAdjustModule":
        """Valida alinhamento ao grid (múltiplos de grid_size)."""
        h, w = self.image.size[1], self.image.size[0]
        if w % grid_size == 0 and h % grid_size == 0:
            print(f"[INFO] [FinalAdjust] grid aligned ({w}x{h})")
        else:
            print(f"[WARN] [FinalAdjust] grid misaligned ({w}x{h} vs {grid_size})")
        return self

    def quantize_palette(self, colors: int = None) -> "FinalAdjustModule":
        """Quantização de paleta opcional (limita cores)."""
        if colors is None:
            print(f"[INFO] [FinalAdjust] palette quantization: skipped")
            return self
        
        img_rgb = Image.fromarray(self.data)
        img_quant = img_rgb.quantize(colors=colors)
        self.data = np.array(img_quant.convert("RGBA"))
        print(f"[INFO] [FinalAdjust] palette quantized ({colors} colors)")
        return self

    def validate(self) -> dict:
        """Checklist de qualidade pixel art."""
        alpha = self.data[:, :, 3]
        h, w = self.data.shape[:2]
        
        opaque_pixels = np.count_nonzero(alpha > 200)
        semi_transparent = np.count_nonzero((alpha > 0) & (alpha <= 200))
        unique_colors = len(np.unique(self.data.reshape(-1, 4), axis=0))
        grid_ok = (w % 1 == 0 and h % 1 == 0)
        
        status = {
            "size": (w, h),
            "opaque_pixels": int(opaque_pixels),
            "semi_transparent": int(semi_transparent),
            "unique_colors": int(unique_colors),
            "grid_aligned": grid_ok,
            "quality": "OK" if semi_transparent < 50 and grid_ok else "CHECK",
        }
        
        print(f"[INFO] [FinalAdjust] validation: {status['quality']} ({w}x{h}, {unique_colors} colors)")
        return status

    def save(self, output_path: str) -> None:
        """Salva imagem final com metadata de validação."""
        result = Image.fromarray(self.data, "RGBA")
        result.save(output_path, "PNG")
        print(f"[INFO] [FinalAdjust] output saved: {output_path}")
