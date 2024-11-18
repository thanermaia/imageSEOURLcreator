from PIL import Image, ImageDraw, ImageFont
import os

# Configurações
font_title_path = "arial.ttf"  # Altere para uma fonte válida no sistema
title_color = "#351C59"
background_color = "#EE551F"
image_size = (1200, 628)
title_font_size = 60

# Diretório de saída
output_dir = os.path.dirname(os.path.abspath(__file__))  # Mesmo local do script
print(f"Diretório configurado para salvar a imagem: {output_dir}")

# Função para criar imagem
def create_image(title, filename):
    try:
        # Criação da imagem
        base_image = Image.new("RGB", image_size, background_color)
        draw = ImageDraw.Draw(base_image)

        # Carregar fonte
        try:
            title_font = ImageFont.truetype(font_title_path, title_font_size)
        except Exception as e:
            print(f"Erro ao carregar a fonte. Usando padrão: {e}")
            title_font = ImageFont.load_default()

        # Adicionar texto
        title_width, title_height = draw.textsize(title, font=title_font)
        title_position = ((image_size[0] - title_width) // 2, (image_size[1] - title_height) // 2)
        draw.text(title_position, title, fill=title_color, font=title_font)

        # Salvar imagem
        output_path = os.path.join(output_dir, filename)
        base_image.save(output_path, "PNG")
        print(f"Imagem gerada e salva em: {output_path}")
    except Exception as e:
        print(f"Erro durante a criação da imagem: {e}")

# Teste de geração de imagem
create_image("Teste de Imagem", "teste_imagem.png")
