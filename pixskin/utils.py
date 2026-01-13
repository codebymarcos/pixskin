"""Utilitários compartilhados para pixskin."""

from pathlib import Path


def _ensure_png(path: str) -> str:
    """Garante extensão PNG e retorna caminho normalizado."""
    if not path.lower().endswith('.png'):
        path = path.rsplit('.', 1)[0] + '.png'
    return path


def _setup_folders(base: str) -> dict:
    """Cria e retorna estrutura de pastas."""
    base = Path(base)
    folders = {
        "input": base / "01_input",
        "resize": base / "02_resize",
        "final": base / "03_final",
    }
    for path in folders.values():
        path.mkdir(parents=True, exist_ok=True)
    return {k: str(v) for k, v in folders.items()}


def _get_image_files(path: str) -> list:
    """Retorna lista de arquivos PNG em um diretório."""
    p = Path(path)
    if not p.is_dir():
        return []
    return sorted(p.glob("*.png")) + sorted(p.glob("*.jpg")) + sorted(p.glob("*.jpeg"))


def _output_name(image_path: str, suffix: str) -> str:
    """Nome arquivo: basename + suffix + .png"""
    base = Path(image_path).stem
    return f"{base}{suffix}.png"
