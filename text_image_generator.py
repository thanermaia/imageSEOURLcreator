from PIL import Image, ImageDraw

# Criação de uma imagem básica
img = Image.new('RGB', (500, 300), color='#EE551F')
draw = ImageDraw.Draw(img)
draw.text((50, 150), "Teste de Imagem", fill="#351C59")
img.save('teste_imagem.png')
print("Imagem gerada com sucesso!")
