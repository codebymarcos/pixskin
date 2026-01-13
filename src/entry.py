import os
from PIL import Image
import logging
import sys
import glob

class input_image:
    """ Preparar imagem de entrada para o pipeline PixelSkin """

    def __init__(self, image_path: str):
        self.path = image_path
        self.filename = os.path.basename(image_path) if image_path else None
        self.image = None

        # Verifica se o caminho da imagem é válido
        if not image_path or not os.path.isfile(image_path):
            raise ValueError(f"Caminho de imagem inválido: {image_path}")
        else:
            print(f"Caminho de imagem definido: {self.path}")
        
    def load_and_normalize(self):
        try:
            img = Image.open(self.path)
            print(f"Imagem [{self.filename}] no formato [{img.format}].")

            if img.format not in ["PNG", "JPEG", "JPG"]:
                print(f"Formato [{img.format}] não suportado. Convertendo para PNG.")
                img = img.convert("RGBA")
            else:
                img = img.convert("RGBA")
                print(f"Imagem [{self.filename}] carregada e normalizada para RGBA.")
            self.image = img
            return img
        except Exception as e:
            logging.error(f"Erro ao carregar a imagem: {e}")
            return None

    def save_normalized(self, output_path=None):
        if self.image is not None:
            if not output_path:
                output_path = f"normalized_{self.filename}.png"
            self.image.save(output_path)
            print(f"Imagem normalizada salva em: {output_path}")
        else:
            print("Nenhuma imagem para salvar.")

if __name__ == "__main__":
    # Se o argumento não for passado, procura automaticamente a primeira imagem na pasta src
    if len(sys.argv) == 2:
        image_path = sys.argv[1]
    else:
        # Procura por arquivos de imagem comuns na pasta src
        imagens = glob.glob("src/*.jpg") + glob.glob("src/*.jpeg") + glob.glob("src/*.png")
        if imagens:
            image_path = imagens[0]
            print(f"Nenhum argumento fornecido. Usando automaticamente: {image_path}")
        else:
            print("Uso: python entry.py <caminho_da_imagem>\nOu coloque uma imagem (.jpg, .jpeg, .png) na pasta src.")
            sys.exit(1)

    input_img = input_image(image_path)
    normalized_img = input_img.load_and_normalize()
    input_img.save_normalized()
    print("Processamento concluído.")