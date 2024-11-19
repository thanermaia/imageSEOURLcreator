import os
import re
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import requests
from io import BytesIO
from unidecode import unidecode  # Biblioteca para remover acentos

# Configurações Gerais
FONT_TITLE_PATH = "TCM_____.ttf"
LOGO_PATH = "logoblah.png"
DEFAULT_BACKGROUND_PATH = "default_ad_agency.jpg"  # Caminho da imagem padrão
TITLE_COLOR = "#351C59"
BACKGROUND_OVERLAY_COLOR = (238, 85, 31, 204)  # Laranja com 80% de transparência
OUTPUT_DIR = "generated_images"
IMAGE_SIZE = (1200, 628)
TITLE_FONT_SIZE = 60
LOGO_WIDTH_RATIO = 0.2  # 20% da largura da imagem
MARGIN_RATIO = 0.1  # 10% para margens superiores/inferiores

CSV_PATH = "seopress-metadata-export-11-12-2024.csv"
DELIMITER = ";"  # Atualize conforme necessário

os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_background_image(query):
    """Busca uma imagem no Unsplash relacionada ao título."""
    url = f"https://source.unsplash.com/1200x628/?{query}"
    try:
        response = requests.get(url, timeout=5)  # Timeout de 5 segundos
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Erro ao buscar imagem para '{query}': {e}")
    return None

def make_seo_friendly_filename(title, index):
    """Gera um nome de arquivo SEO-friendly."""
    # Remover acentos e caracteres especiais
    title_cleaned = unidecode(title)
    title_cleaned = re.sub(r"[^\w\s-]", "", title_cleaned)  # Remove caracteres não alfanuméricos
    title_cleaned = re.sub(r"\s+", "-", title_cleaned.strip())  # Substitui espaços por hífens
    return f"{title_cleaned[:50]}_{index}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"

def create_image(title, filename):
    """Cria uma imagem com título, fundo e logotipo."""
    try:
        # Tenta buscar uma imagem para o título
        background = fetch_background_image(title)
        
        # Caso não encontre, usa a imagem padrão
        if background is None:
            if os.path.exists(DEFAULT_BACKGROUND_PATH):
                background = Image.open(DEFAULT_BACKGROUND_PATH).resize(IMAGE_SIZE)
            else:
                background = Image.new("RGB", IMAGE_SIZE, "#CCCCCC")

        # Aplicar sobreposição
        overlay = Image.new("RGBA", IMAGE_SIZE, BACKGROUND_OVERLAY_COLOR)
        background = Image.alpha_composite(background.convert("RGBA"), overlay)

        draw = ImageDraw.Draw(background)

        title_font = ImageFont.truetype(FONT_TITLE_PATH, TITLE_FONT_SIZE)

        # Margens
        margin_top = int(IMAGE_SIZE[1] * MARGIN_RATIO)
        margin_bottom = int(IMAGE_SIZE[1] * MARGIN_RATIO)

        # Centralizar título começando 10% abaixo do topo
        text_bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        title_x = (IMAGE_SIZE[0] - text_width) // 2
        title_y = margin_top
        draw.text((title_x, title_y), title, fill=TITLE_COLOR, font=title_font)

        # Logo centralizada no rodapé
        if os.path.exists(LOGO_PATH):
            logo = Image.open(LOGO_PATH).convert("RGBA")
            logo_width = int(IMAGE_SIZE[0] * LOGO_WIDTH_RATIO)
            logo_height = int(logo_width * logo.height / logo.width)
            logo = logo.resize((logo_width, logo_height))
            logo_x = (IMAGE_SIZE[0] - logo_width) // 2
            logo_y = IMAGE_SIZE[1] - logo_height - margin_bottom
            background.paste(logo, (logo_x, logo_y), logo)

        # Salvar imagem
        output_path = os.path.join(OUTPUT_DIR, filename)
        background.save(output_path, "PNG")
        print(f"Imagem gerada: {filename}")
        return True
    except Exception as e:
        print(f"Erro ao gerar imagem '{filename}': {e}")
        return False

try:
    data = pd.read_csv(CSV_PATH, encoding="utf-8-sig", delimiter=DELIMITER, on_bad_lines="skip")
    data.columns = data.columns.str.strip()
    print("CSV carregado com sucesso!")

    for index, row in data.iterrows():
        title = str(row.get("meta_title", "")).strip()

        if not title or pd.isna(title):
            print(f"Linha {index} ignorada: título ausente.")
            continue

        filename = make_seo_friendly_filename(title, index)
        if not create_image(title, filename):
            print(f"Erro ao gerar imagem para a linha {index}.")
except Exception as e:
    print(f"Erro geral: {e}")
