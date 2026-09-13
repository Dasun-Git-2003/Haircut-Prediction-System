import os
import uuid
import aiofiles
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import ImageValidationError

class ImageService:
    @staticmethod
    async def save_upload(file: UploadFile) -> str:
        if not file.content_type.startswith("image/"):
            raise ImageValidationError("File is not an image")
            
        # check size limit (mock, ideally read chunks)
        
        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(settings.UPLOAD_DIR, filename)
        
        async with aiofiles.open(filepath, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            
        return filepath
        
    @staticmethod
    def get_image_url(filepath: str) -> str:
        return f"/uploads/{os.path.basename(filepath)}"
