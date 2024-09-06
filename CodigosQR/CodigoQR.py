import qrcode
from PIL import Image, ImageDraw, ImageFont

# Función para redondear las esquinas de una imagen
# (esta función no funciona bien, todavía)
def add_rounded_corners(image, radius):
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
    alpha = Image.new('L', image.size, 255)
    w, h = image.size

    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))

    image.putalpha(alpha)
    return image

# Crear el código QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=2
)
qr.add_data("https://nicomedinap.github.io/decosmos/M16/JWST/30Agosto2024/M16.html")
qr.make(fit=True)

# Convertir el QR en una imagen y cambiar a modo RGBA
img = qr.make_image(fill="black", back_color="white").convert("RGBA")

# Redondear las esquinas del QR
rounded_qr = add_rounded_corners(img, radius=5)

# Crear una nueva imagen con espacio para el título
width, height = rounded_qr.size
new_height = height + int(0.1 * height)  # Espacio adicional para el título (10% del tamaño QR)
new_img = Image.new('RGBA', (width, new_height), 'white')

# Pegar el QR con bordes redondeados en la nueva imagen
new_img.paste(rounded_qr, (0, 0), rounded_qr)

# Añadir el título con fuente proporcional
draw = ImageDraw.Draw(new_img)
font_size = int(width * 0.5)  # Ajusta el tamaño de la fuente al 10% del tamaño QR

# Fuente: intentar usar DejaVuSans-Bold, o cargar una predeterminada
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
except IOError:
    font = ImageFont.load_default()

# Título que deseas poner
text = "Región de formación estelar M16"

# Ajuste automático del tamaño del texto si es más grande que el espacio disponible
text_width, text_height = draw.textsize(text, font=font)
if text_width > width:
    font_size = int(width * 0.5)  # Reducir el tamaño de la fuente
    font = ImageFont.load_default()

# Centrar el texto debajo del QR
text_position = ((width - text_width) // 2, height + 10)
draw.text(text_position, text, font=font, fill="black")

# Guardar la imagen final
new_img.save("M16_qr_with_title.png")

# Mostrar la imagen (opcional)
new_img.show()
