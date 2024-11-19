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
