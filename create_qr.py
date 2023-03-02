import qrcode
import qrcode.image.pil
from PIL import Image

img = qrcode.make('http://www.google.com/', image_factory=qrcode.image.pil.PilImage)
# scale the image to have a maximum size of 128x128 pixels
img = img.resize((128, 128), resample=Image.LANCZOS)

with open('qr.png', 'wb') as qr:
    img.save(qr)