"""Classe principal PixSkinConverter - orquestrador do pipeline."""

import os
from pathlib import Path
from PIL import Image

from .modules import InputImage, ResizeModule, FinalAdjustModule
from .utils import _setup_folders, _get_image_files, _output_name


class PixSkinConverter:
    """Conversor de imagens/pastas para pixel art com pipeline automatizado."""

    def __init__(self, downscale_size: tuple = (80, 80), upscale_factor: int = 2,
                 alpha_threshold: int = 20, preserve_intermediates: bool = True):
        """
        Inicializa conversor com configurações.
        
        Args:
            downscale_size: Dimensões para reduzir (width, height)
            upscale_factor: Multiplicador de aumento
            alpha_threshold: Limite para limpeza de alpha (0-255)
            preserve_intermediates: Manter 01_input e 02_resize
        """
        self.downscale_size = downscale_size
        self.upscale_factor = upscale_factor
        self.alpha_threshold = alpha_threshold
        self.preserve_intermediates = preserve_intermediates

    def _process_single(self, image_path: str, output_dir: str = None) -> str:
        """Processa uma imagem única. Retorna caminho de saída."""
        image_path = Path(image_path).resolve()
        
        if not image_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {image_path}")
        
        if image_path.suffix.lower() not in ['.png', '.jpg', '.jpeg']:
            raise ValueError(f"Formato não suportado: {image_path.suffix}")
        
        print(f"[INFO] [PixSkinConverter] processing image: {image_path.name}")
        
        # Determinar diretório de saída
        if output_dir is None:
            output_dir = image_path.parent
        else:
            output_dir = Path(output_dir)
        
        # Criar estrutura de pastas se houver intermediários
        if self.preserve_intermediates:
            folders = _setup_folders(output_dir / ".pixskin_temp")
        
        # Etapa 1: Remover fundo
        proc = InputImage(str(image_path), auto_process=True)
        img = proc.prepared_image
        
        if self.preserve_intermediates:
            path = os.path.join(folders["input"], _output_name(str(image_path), "_background_removed"))
            proc.save_prepared(path)
        
        # Etapa 2: Downscale
        resize = ResizeModule(img).downscale(self.downscale_size)
        
        if self.preserve_intermediates:
            path = os.path.join(folders["resize"], _output_name(str(image_path), "_downscaled"))
            resize.save(path)
        
        # Etapa 3: Upscale
        resize.upscale_for_export(self.upscale_factor)
        
        # Etapa 4: Salvar resultado intermediário
        path_final = os.path.join(output_dir, _output_name(str(image_path), "_pixelart"))
        resize.save(path_final)
        
        # Etapa 5: Ajuste final
        final_img = Image.open(path_final)
        adjuster = FinalAdjustModule(final_img)
        adjuster.clean_alpha(self.alpha_threshold).remove_orphan_pixels().validate()
        
        path_adjusted = os.path.join(output_dir, _output_name(str(image_path), "_final"))
        adjuster.save(path_adjusted)
        
        print(f"[INFO] [PixSkinConverter] output saved: {Path(path_adjusted).name}")
        
        return path_adjusted

    def process_image(self, image_path: str) -> str:
        """
        Processa uma imagem única.
        
        Args:
            image_path: Caminho da imagem PNG/JPG
            
        Returns:
            Caminho do arquivo final
        """
        return self._process_single(image_path)

    def process_folder(self, folder_path: str) -> list:
        """
        Processa todas as imagens em uma pasta.
        
        Args:
            folder_path: Caminho da pasta com imagens
            
        Returns:
            Lista com caminhos dos arquivos processados
        """
        folder_path = Path(folder_path).resolve()
        
        if not folder_path.is_dir():
            raise NotADirectoryError(f"Pasta não encontrada: {folder_path}")
        
        images = _get_image_files(str(folder_path))
        
        if not images:
            print(f"[WARN] [PixSkinConverter] no images found in {folder_path}")
            return []
        
        print(f"[INFO] [PixSkinConverter] processing {len(images)} images from {folder_path.name}")
        
        # Criar subpasta de output
        output_dir = folder_path / "pixskin_output"
        output_dir.mkdir(exist_ok=True)
        
        results = []
        for img_path in images:
            try:
                result = self._process_single(str(img_path), str(output_dir))
                results.append(result)
            except Exception as e:
                print(f"[ERROR] [PixSkinConverter] failed to process {img_path.name}: {str(e)}")
                continue
        
        print(f"[INFO] [PixSkinConverter] batch processing completed ({len(results)}/{len(images)})")
        
        return results
