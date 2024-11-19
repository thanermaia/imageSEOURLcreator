from PIL import Image, ImageDraw, ImageFont

IMAGE_SIZE = (1200, 628)
TITLE_FONT_SIZE = 60
TITLE_COLOR = "#351C59"
FONT_TITLE_PATH = "TCM_____.ttf"

def test_image_creation():
    try:
        image = Image.new("RGB", IMAGE_SIZE, "#FFFFFF")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT_TITLE_PATH, TITLE_FONT_SIZE)
        draw.text((100, 100), "Teste de Imagem", font=font, fill=TITLE_COLOR)
        image.save("teste_output.png")
        print("Imagem teste criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar imagem teste: {e}")

test_image_creation()
