import os
import aiofiles
from fastapi import UploadFile

UPLOAD_DIRECTORY = "uploads"

async def save_file(file: UploadFile) -> str:
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    
    return file_path