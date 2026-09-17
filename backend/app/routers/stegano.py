from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response

from ..deps import get_current_user
from ..steganography import encode_image, decode_image

router = APIRouter(prefix="/stegano", tags=["stegano"])

@router.post("/hide")
async def hide_data(
    file: UploadFile = File(...),
    secret_text: str = Form(...),
    user_id: str = Depends(get_current_user)
):
    """Hide secret text inside an image using LSB steganography."""
    try:
        content = await file.read()
        encoded = encode_image(content, secret_text)
        return Response(content=encoded, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/extract")
async def extract_data(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):
    """Extract hidden text from an image."""
    try:
        content = await file.read()
        secret_text = decode_image(content)
        return {"secret_text": secret_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
