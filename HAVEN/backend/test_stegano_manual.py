import io
import requests
from PIL import Image

def test():
    # Create a dummy RGB image
    img = Image.new('RGB', (100, 100), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()
    
    # Needs auth, let's just test the functions directly for simplicity
    from app.steganography import encode_image, decode_image
    
    secret = "This is a hidden secret about abuse."
    encoded = encode_image(img_bytes, secret)
    
    extracted = decode_image(encoded)
    assert extracted == secret
    print("SUCCESS: Steganography works! Hidden text extracted successfully.")

if __name__ == "__main__":
    test()
