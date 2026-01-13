# Documentação Técnica - PixSkin

## Visão Geral

O **PixSkin** é um framework Python modular para processamento de imagens focado em remoção automática de fundos. O projeto foi desenvolvido seguindo princípios de arquitetura limpa, com separação clara entre camadas de entrada, processamento core e saída.

## Arquitetura

### Padrão de Design

O projeto utiliza uma arquitetura em camadas:

1. **Camada de Entrada** (`input.py`): Responsável por carregar e preparar imagens
2. **Camada Core** (`core/remove_bg.py`): Lógica de negócio para remoção de fundo
3. **Camada de Saída**: Manipulação e salvamento dos resultados

### Classes Principais

#### `input_image`

Classe de alto nível que encapsula o fluxo completo de processamento:

```python
class input_image:
    def __init__(self, image_path: str)
    def remove_background(self) -> Image
    def prepare_for_pipeline(self) -> Image
```

**Responsabilidades:**
- Carregamento de imagens do disco
- Coordenação do processo de remoção de fundo
- Preparação de imagens para pipelines downstream
- Conversão de formatos quando necessário

#### `remove_bg`

Classe utilitária especializada em operações de remoção de fundo:

```python
class remove_bg:
    @staticmethod
    def remove_background(image: Image) -> Image
    @staticmethod
    def save_image(processed_image: Image, output_path: str) -> None
```

**Responsabilidades:**
- Execução da remoção de fundo usando rembg
- Salvamento de imagens processadas
- Validação de entrada/saída

## Algoritmo de Remoção de Fundo

### Tecnologia Utilizada

- **Modelo**: U2Net (U-Net para segmentação de objetos)
- **Framework**: ONNX Runtime para inferência
- **Biblioteca**: rembg como interface de alto nível

### Processo

1. **Pré-processamento**: Conversão da imagem para formato adequado
2. **Inferência**: Aplicação do modelo de IA para segmentação
3. **Pós-processamento**: Aplicação de máscara e criação de transparência
4. **Saída**: Imagem com fundo removido em formato RGBA

### Limitações

- Requer imagens com contraste suficiente entre objeto e fundo
- Melhor performance com objetos bem definidos
- Pode ter dificuldades com cabelos finos, transparências ou objetos complexos

## Configuração e Dependências

### Ambiente de Desenvolvimento

```toml
# pyproject.toml
[project]
name = "pixskin"
version = "0.1.0"
requires-python = ">=3.9"
```

### Dependências Principais

- **rembg[cpu]**: Core da funcionalidade de remoção de fundo
- **Pillow**: Manipulação de imagens
- **pytest**: Testes automatizados

### Instalação de Dependências

```bash
# Ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Dependências básicas
pip install -r requirements.txt

# Suporte IA (obrigatório)
pip install "rembg[cpu]"
```

## Testes

### Estrutura de Testes

```
tests/
├── test_main.py      # Testes da função main
└── img/             # Imagens de teste
    ├── personagem1.png
    ├── personagem2.jpg
    └── personagem3.jpg
```

### Execução de Testes

```bash
# Todos os testes
python -m pytest tests/ -v

# Com cobertura
python -m pytest tests/ --cov=src --cov-report=html
```

### Testes de Integração

Para testar a funcionalidade completa:

```python
from src.input import input_image

def test_full_pipeline():
    processor = input_image("tests/img/personagem1.png")
    result = processor.remove_background()
    final = processor.prepare_for_pipeline()

    assert final.mode == "RGBA"
    assert result is not None
```

## Performance

### Métricas de Desempenho

- **Tempo médio de processamento**: ~2-5 segundos por imagem (depende do hardware)
- **Uso de memória**: ~200-500MB durante processamento
- **Download inicial**: Modelo U2Net (~176MB) baixado automaticamente

### Otimizações

- Processamento em lote não implementado
- Cache de modelos não configurado
- Paralelização limitada ao que o ONNX Runtime oferece

## Tratamento de Erros

### Exceções Comuns

- `FileNotFoundError`: Caminho de imagem inválido
- `PIL.UnidentifiedImageError`: Formato de imagem não suportado
- `ModuleNotFoundError`: Dependências não instaladas

### Validações

- Verificação de existência de arquivo na inicialização
- Validação de formato de imagem suportado
- Checagem de imagem processada antes do salvamento

## Extensibilidade

### Adição de Novos Processamentos

Para adicionar novos tipos de processamento:

1. Criar nova classe em `src/core/`
2. Seguir padrão de métodos estáticos
3. Integrar na classe `input_image` se necessário

### Suporte a Novos Modelos

Para usar diferentes modelos de IA:

1. Modificar import em `remove_bg.py`
2. Atualizar método `remove_background`
3. Testar compatibilidade com interface existente

## Boas Práticas

### Desenvolvimento

- Usar type hints em todas as funções
- Manter docstrings atualizadas
- Seguir convenções de nomenclatura PEP 8

### Produção

- Sempre usar ambiente virtual
- Instalar dependências em ordem específica
- Validar imagens antes do processamento

## Troubleshooting

### Problemas Comuns

**Erro: "No onnxruntime backend found"**
- Solução: `pip install "rembg[cpu]"`

**Erro: "ModuleNotFoundError: No module named 'rembg'"**
- Solução: Ativar ambiente virtual e reinstalar dependências

**Imagens com fundo não removido corretamente**
- Verificar contraste entre objeto e fundo
- Testar com diferentes tipos de imagem

### Logs e Debug

O projeto utiliza prints simples para feedback. Para debug avançado:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Referências

- [rembg Documentation](https://github.com/danielgatis/rembg)
- [U2Net Paper](https://arxiv.org/abs/2005.09007)
- [Pillow Documentation](https://pillow.readthedocs.io/)