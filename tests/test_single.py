"""Testes para processamento de arquivo único."""

import pytest
from pathlib import Path
from pixskin import PixSkinConverter


def test_process_image_not_found():
    """Testa erro quando arquivo não existe."""
    converter = PixSkinConverter()
    
    with pytest.raises(FileNotFoundError):
        converter.process_image("arquivo_inexistente.png")


def test_process_image_invalid_format():
    """Testa erro com formato inválido."""
    converter = PixSkinConverter()
    
    # Criar arquivo temporário com extensão inválida
    test_file = Path("test_image.bmp")
    test_file.touch()
    
    try:
        with pytest.raises(ValueError):
            converter.process_image(str(test_file))
    finally:
        test_file.unlink()


def test_converter_initialization():
    """Testa inicialização do conversor."""
    converter = PixSkinConverter(
        downscale_size=(64, 64),
        upscale_factor=3,
        alpha_threshold=15
    )
    
    assert converter.downscale_size == (64, 64)
    assert converter.upscale_factor == 3
    assert converter.alpha_threshold == 15
    assert converter.preserve_intermediates is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
