import time
import uuid
import magic
from pathlib import Path

import aiofiles
from fastapi.responses import StreamingResponse

root = Path(__file__).parent.parent.parent

Buffer_Size = 1024 ** 2 * 10


async def coro_upload_file(file):
    # file_byte = file.file.read()
    real_path, res_path = get_realP_and_resP(file)
    try:
        async with aiofiles.open(real_path, "wb") as out_file:
            while content := await file.read(Buffer_Size):
                await out_file.write(content)
        return res_path
    except Exception as e:
        raise Exception(400, f"上传失败{e}") from e


async def coro_get_file(file_path: str):
    real_path = root / "files" / file_path

    async def file_stream():
        async with aiofiles.open(real_path, "rb") as f:
            while chunk := await f.read(Buffer_Size):
                yield chunk

    content_type = await async_get_content_type(str(real_path))

    return StreamingResponse(file_stream(), media_type=content_type)


def upload_file(file):
    real_path, res_path = get_realP_and_resP(file)
    with open(real_path, "wb") as f:
        while content := file.file.read(Buffer_Size):
            f.write(content)
    return res_path


def get_file(file_path: str):
    real_path = root / "files" / file_path
    file_byte = open(real_path, "rb").read()
    content_type = magic.from_buffer(file_byte, mime=True)
    return StreamingResponse(file_byte, media_type=content_type)


def get_file_path(file_path):
    return str(root / "files" / file_path)


# ======================================================================================================================


def get_realP_and_resP(file):
    file_dir = f'{time.strftime("%Y%m", time.localtime())}/{uuid.uuid1()}'
    real_file_dir = root / Path('files') / file_dir
    if not real_file_dir.exists():
        real_file_dir.mkdir(parents=True, exist_ok=True)
    real_path = root / Path('files') / file_dir / file.filename
    res_path = f'{file_dir}/{file.filename}'
    return real_path, res_path


def save_sub(audio_path, sub_str, sub_label, format_='srt'):
    sub_path = Path(audio_path).parent / f'{Path(audio_path).stem}_{sub_label}.{format_}'
    with open(sub_path, 'w') as f:
        f.write(sub_str)
    return str(sub_path).split('files/')[-1]


# 读取文件头部来获取MIME类型
async def async_get_content_type(file_path: str) -> str:
    async with aiofiles.open(file_path, "rb") as f:
        file_header = await f.read(1024)
    return magic.from_buffer(file_header, mime=True)