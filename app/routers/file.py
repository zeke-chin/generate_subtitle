from typing import List
from fastapi import APIRouter, File, UploadFile
from app import service
from utils import coroutine_timeit

router_file = APIRouter(prefix="/file", tags=["file-文件管理"])

@router_file.post("/coroutine", summary="上传文件")
@coroutine_timeit
async def coro_upload_file(up_files: List[UploadFile] = File(...)):
    res = []
    for file in up_files:
        r = await service.coro_upload_file(file)
        res.append(r)
    return res
# async def coro_upload_file(up_file: UploadFile = File(...)):
#     return await service.coro_upload_file(up_file)


@router_file.get("/coroutine/{uri:path}", summary="获取文件")
@coroutine_timeit
async def coro_get_file(uri: str):
    return await service.coro_get_file(uri)


# @router_file.post("", summary="上传文件")
# @web_try()
# @timeit
# def upload_file(up_file: UploadFile = File(...)):
#     return service.upload_file(up_file)
#
#
# @router_file.get("/{uri:path}", summary="获取文件")
# @timeit
# def get_file(uri: str):
#     return service.get_file(uri)
