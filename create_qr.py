import qrcode
import qrcode.image.pil
from PIL import Image

def create_qr(url):
    # create qr code
    img = qrcode.make(f"ssh://{url}", image_factory=qrcode.image.pil.PilImage)
    # scale the image to have a maximum size of 128x128 pixels
    img = img.resize((128, 128), resample=Image.LANCZOS)
    # remove the white border
    img = img.crop((4, 4, 124, 124))

    with open('pic/qr.png', 'wb') as qr:
        img.save(qr)