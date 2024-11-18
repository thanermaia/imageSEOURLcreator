from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import re

# Configurações de estilos
font_title_path = "TCM_____.ttf"  # Fonte para o título
font_description_path = "TCM_____.ttf"  # Fonte para a descrição
title_color = "#351C59"
background_color = "#EE551F"
overlay_color = (238, 85, 31, 204)  # Cor com transparência 80%
output_dir = "generated_images"

# Tamanhos e fontes
image_size = (1200, 628)
title_font_size = 60
description_font_size = 30

# Carregar o CSV
csv_path = "seopress-metadata-export-11-12-2024.csv"
data = pd.read_csv(csv_path)

# Criar o diretório de saída
os.makedirs(output_dir, exist_ok=True)

# Função para criar nomes de arquivos válidos
def clean_filename(title):
    return re.sub(r'[^A-Za-z0-9]+', '_', title)[:50] + ".png"

# Função para criar imagens
def create_image(title, description, filename):
    # Criar imagem base
    base_image = Image.new("RGB", image_size, background_color)
    overlay = Image.new("RGBA", image_size, overlay_color)
    base_image.paste(overlay, (0, 0), overlay)

    draw = ImageDraw.Draw(base_image)
    
    try:
        title_font = ImageFont.truetype(font_title_path, title_font_size)
        description_font = ImageFont.truetype(font_description_path, description_font_size)
    except Exception as e:
        print(f"Erro ao carregar fonte: {e}. Usando fonte padrão.")
        title_font = ImageFont.load_default()
        description_font = ImageFont.load_default()

    # Centralizar o título
    bbox_title = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox_title[2] - bbox_title[0]
    title_height = bbox_title[3] - bbox_title[1]
    title_position = ((image_size[0] - title_width) // 2, (image_size[1] - title_height) // 3)
    draw.text(title_position, title, fill=title_color, font=title_font)

    # Posicionar descrição (se existir)
    if description:
        bbox_desc = draw.textbbox((0, 0), description, font=description_font)
        desc_width = bbox_desc[2] - bbox_desc[0]
        desc_height = bbox_desc[3] - bbox_desc[1]
        description_position = ((image_size[0] - desc_width) // 2, title_position[1] + title_height + 20)
        draw.text(description_position, description, fill=title_color, font=description_font)

    # Salvar imagem
    output_path = os.path.join(output_dir, filename)
    base_image.save(output_path, "PNG")

# Gerar imagens para cada linha no CSV
for index, row in data.iterrows():
    title = row.get("meta_title", "Título Não Informado")
    description = row.get("meta_description", "")
    filename = clean_filename(title)  # Usar título como nome da imagem
    create_image(title, description, filename)

print(f"Imagens geradas e salvas no diretório '{output_dir}'")
