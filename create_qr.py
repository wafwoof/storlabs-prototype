import qrcode
import qrcode.image.pil
from PIL import Image

def create_qr(url):
    # create qr code
    img = qrcode.make(f"ssh://{url}", image_factory=qrcode.image.pil.PilImage)
    # get w/h of image
    w, h = img.size
    # subtract 40 pixels from each side
    area = (40, 40, w-40, h-40)
    img = img.crop(area)
    img = img.resize((112, 112), resample=Image.LANCZOS)

    with open('pic/qr.png', 'wb') as qr:
        img.save(qr)

# for testing
if __name__ == "__main__":
    create_qr("https://www.google.com")
    img = Image.open('pic/qr.png')
    img.show()