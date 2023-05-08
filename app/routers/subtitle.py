from fastapi import APIRouter
from app import service, schemas
from utils import web_try, timeit

router_subtitle = APIRouter(prefix="/subtitle", tags=["subtitle-字幕服务"])


@router_subtitle.post("/transcription2sub", summary="语音转字幕")
@web_try()
@timeit
def transcription(item: schemas.Transcription):
    return service.get_tsr_sub(audio_path=service.get_file_path(item.audio_path),
                               audio_lang=item.audio_lang,
                               is_verbose=item.is_verbose,
                               use_fp16=item.use_fp16,
                               format_=item.format_)


@router_subtitle.post("/translation2sub", summary="语音转双语字幕")
@web_try()
@timeit
def translation(item: schemas.Translation):
    return service.get_tsl_sub(audio_path=service.get_file_path(item.audio_path),
                               audio_lang=item.audio_lang,
                               target_lang=item.target_lang,
                               gs=item.gs,
                               is_verbose=item.is_verbose,
                               use_fp16=item.use_fp16,
                               format_=item.format_)
