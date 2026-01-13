# PixSkin - Biblioteca de Conversão para Pixel Art

Biblioteca Python profissional para conversão automática de imagens/pastas para pixel art com remoção de fundo, redimensionamento inteligente e ajustes finais.

## Instalação

```bash
pip install -e .
```

Ou com dependências específicas:

```bash
pip install -r requirements.txt
pip install -e .
```

## Uso Rápido

### Processar uma imagem

```python
from pixskin import PixSkinConverter

converter = PixSkinConverter()
result = converter.process_image("personagem.png")
print(f"Resultado salvo em: {result}")
# Saída: personagem_final.png (no mesmo diretório)
```

### Processar uma pasta

```python
from pixskin import PixSkinConverter

converter = PixSkinConverter()
results = converter.process_folder("./sprites/")
print(f"Processadas {len(results)} imagens")
# Saída: ./sprites/pixskin_output/
#        ├── personagem1_final.png
#        ├── personagem2_final.png
#        └── ...
```

### Configuração customizada

```python
converter = PixSkinConverter(
    downscale_size=(64, 64),  # Tamanho para reduzir
    upscale_factor=3,         # Multiplicador de aumento
    alpha_threshold=15,       # Limite para limpeza de alpha
    preserve_intermediates=True  # Manter etapas intermediárias
)

result = converter.process_image("sprite.png")
```

## Pipeline

Cada imagem passa por:

1. **Remove Fundo** - Usa IA (rembg) para remover background
2. **Downscale** - Reduz para tamanho definido (padrão: 80x80)
3. **Upscale** - Aumenta mantendo pixels nítidos (NEAREST)
4. **Ajuste Final** - Limpeza de alpha e validação de qualidade

## Estrutura de Saída

### Arquivo único
```
personagem.png → personagem_final.png (no mesmo diretório)
```

### Pasta com múltiplas imagens
```
sprites/
├── sprite1.png
├── sprite2.png
└── pixskin_output/
    ├── .pixskin_temp/
    │   ├── 01_input/
    │   ├── 02_resize/
    │   └── 03_final/
    ├── sprite1_final.png
    ├── sprite2_final.png
    └── ...
```

## Logs

Todos os passos são registrados com formato estruturado:

```
[INFO] [PixSkinConverter] processing image: personagem.png
[INFO] [InputImage] background removed: personagem.png
[INFO] [ResizeModule] downscale applied (80, 80)
[INFO] [ResizeModule] upscale applied (factor=2)
[INFO] [FinalAdjust] alpha cleaned (threshold=20)
[INFO] [FinalAdjust] orphan pixels removed (5)
[INFO] [FinalAdjust] validation: OK (160x160, 23 colors)
[INFO] [PixSkinConverter] output saved: personagem_final.png
```

## API Completa

### PixSkinConverter

```python
class PixSkinConverter:
    def __init__(
        self,
        downscale_size: tuple = (80, 80),
        upscale_factor: int = 2,
        alpha_threshold: int = 20,
        preserve_intermediates: bool = True
    ) -> None
    
    def process_image(self, image_path: str) -> str
    def process_folder(self, folder_path: str) -> list[str]
```

## Requisitos

- Python 3.8+
- Pillow >= 10.0.0
- numpy >= 1.24.0
- scipy >= 1.10.0
- rembg >= 0.0.0

## Licença

MIT License
