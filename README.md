# PixSkin

Conversor automático de imagens para pixel art com remoção de fundo IA.

## Instalação

```bash
pip install -e .
```

## Uso Rápido

**Imagem única:**
```python
from pixskin import PixSkinConverter

converter = PixSkinConverter()
converter.process_image("foto.png")  # Salva foto_final.png
```

**Pasta (lote):**
```python
converter.process_folder("./imagens/")  # Salva em imagens/pixskin_output/
```

**Customizado:**
```python
converter = PixSkinConverter(
    downscale_size=(64, 64),
    upscale_factor=3,
    alpha_threshold=15,
    preserve_intermediates=True
)
```

## Docs

- [Quickstart](docs/quickstart.md)
- [Exemplos](docs/examples.md)
- [API](docs/api.md)
- [Troubleshooting](docs/troubleshooting.md)

## Licença

MIT
