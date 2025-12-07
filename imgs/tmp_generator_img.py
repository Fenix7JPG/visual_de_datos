from PIL import Image, ImageDraw, ImageFont
CANTIDAD = 20


ANCHO = 200
ALTO = 200


COLOR_FONDO = (240, 240, 240)
COLOR_TEXTO = (0, 0, 0)


try:
    font = ImageFont.truetype("arial.ttf", 120)
except:
    font = ImageFont.load_default()

for i in range(1, CANTIDAD + 1):
    img = Image.new("RGB", (ANCHO, ALTO), COLOR_FONDO)
    draw = ImageDraw.Draw(img)

    text = str(i)

    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # Centrado
    x = (ANCHO - w) / 2
    y = (ALTO - h) / 2

    draw.text((x, y), text, fill=COLOR_TEXTO, font=font)

    img.save(f"{i}.png")

print("Listo: imágenes generadas (compatible con Pillow 10+).")
