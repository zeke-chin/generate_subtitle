from fastapi import APIRouter
from app import service, schemas
from utils import web_try, timeit

router_model = APIRouter(prefix="/model", tags=["model-算法模型"])


@router_model.post("/init", summary="初始化模型")
@web_try()
@timeit
def init_model(asr_init: schemas.AsrInit, tsl_init: schemas.M2M100Init):
    return service.init_model(asr_init, tsl_init)


@router_model.post("/asr", summary="语音转文本")
@web_try()
@timeit
def asr_inference(item: schemas.AsrInference):
    return service.asr_inference(audio_path=service.get_file_path(item.audio_path),
                                 audio_lang=item.audio_lang,
                                 is_verbose=item.is_verbose,
                                 use_fp16=item.use_fp16)


@router_model.post("/tsl", summary="文本翻译")
@web_try()
@timeit
def tsl_inference(item: schemas.M2M100Inference):
    return service.tsl_inference(texts=item.texts,
                                 src_lang=item.src_lang,
                                 tgt_lang=item.tgt_lang,
                                 gs=item.gs)
