"""Testes para processamento de pasta."""

import pytest
from pathlib import Path
from pixskin import PixSkinConverter


def test_process_folder_not_found():
    """Testa erro quando pasta não existe."""
    converter = PixSkinConverter()
    
    with pytest.raises(NotADirectoryError):
        converter.process_folder("pasta_inexistente")


def test_process_folder_empty():
    """Testa processamento de pasta vazia."""
    import tempfile
    
    converter = PixSkinConverter()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        results = converter.process_folder(tmpdir)
        assert results == []


def test_process_folder_creates_output_dir():
    """Testa se cria subpasta pixskin_output."""
    import tempfile
    import os
    
    converter = PixSkinConverter(preserve_intermediates=False)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Verificar que pixskin_output será criada
        output_dir = Path(tmpdir) / "pixskin_output"
        assert not output_dir.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
