import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Crear el código QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4
)
qr.add_data("https://nicomedinap.github.io/decosmos/NGC4254/JWST/04Septiembre2024/NGC4254.html")
qr.make(fit=True)

# Convertir el QR en una imagen
img = qr.make_image(fill="black", back_color="white")

# Suavizar los bordes del QR
img = img.filter(ImageFilter.SMOOTH_MORE)

# Crear una nueva imagen con espacio para el título
width, height = img.size
new_height = height + 50  # Espacio para el título
new_img = Image.new('RGB', (width, new_height), 'white')
new_img.paste(img, (0, 0))

# Añadir el título
draw = ImageDraw.Draw(new_img)
font = ImageFont.load_default()  # Puedes cargar una fuente personalizada si lo deseas
text = "Galaxia NGC 4254"
text_width, text_height = draw.textsize(text, font=font)
text_position = ((width - text_width) // 2, height + 10)
draw.text(text_position, text, font=font, fill="black")

# Guardar la imagen con el QR y el título
new_img.save("output_qr_with_title.png")

# Mostrar la imagen (opcional)
new_img.show()
