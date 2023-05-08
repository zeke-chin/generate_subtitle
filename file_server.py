import os
from typing import List

import aiofiles
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

AUDIO_STORAGE_PATH = "files/"


@app.post("/upload_audio/")
async def upload_audio_files(files: List[UploadFile] = File(...)):
    for file in files:
        # file_ext = file.filename.split(".")[-1] in ("mp3", "wav", "ogg", "flac")
        #
        # if not file_ext:
        #     raise HTTPException(status_code=400, detail="Invalid file extension.")

        async with aiofiles.open(f"{AUDIO_STORAGE_PATH}{file.filename}", "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
    return {"result": "Audio files uploaded successfully."}


@app.get("/get_audio/{file_name}")
async def get_audio_file(file_name: str):
    file_path = f"{AUDIO_STORAGE_PATH}{file_name}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found.")
    return FileResponse(file_path, media_type="audio/mpeg")
