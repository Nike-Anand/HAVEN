"""Steganography module for hiding text in images using LSB (Least Significant Bit)."""
from PIL import Image
import io

def _gen_data(data):
    """Convert text data to binary strings."""
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

def _modify_pixels(pix, data):
    """Modify the least significant bit of pixels to store binary data."""
    datalist = _gen_data(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        # Extracting 3 pixels at a time (9 values since RGB)
        try:
            pix = [value for value in next(imdata)[:3] + next(imdata)[:3] + next(imdata)[:3]]
        except StopIteration:
            raise ValueError("Image is too small to encode this message.")

        # Pixel value should be made odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        
        # Eighth pixel decides whether to stop reading or continue
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def _encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in _modify_pixels(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode_image(image_bytes: bytes, secret_message: str) -> bytes:
    """Encode a secret message into an image's LSB."""
    if len(secret_message) == 0:
        raise ValueError("Data is empty")

    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != 'RGB':
        image = image.convert('RGB')
    newimg = image.copy()
    _encode_enc(newimg, secret_message)

    img_byte_arr = io.BytesIO()
    # Save as PNG to avoid compression artifacts breaking the LSB
    newimg.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def decode_image(image_bytes: bytes) -> str:
    """Decode a secret message from an image's LSB."""
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    imgdata = iter(image.getdata())
    data = ''

    while True:
        try:
            pixels = [value for value in next(imgdata)[:3] + next(imgdata)[:3] + next(imgdata)[:3]]
        except StopIteration:
            break

        binstr = ''
        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += '0'
            else:
                binstr += '1'
        
        data += chr(int(binstr, 2))
        
        # Stop if 8th pixel is odd
        if pixels[-1] % 2 != 0:
            return data
            
    return data
