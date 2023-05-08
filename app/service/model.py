from typing import List

import utils
from app import schemas
from app.service import file
from server import Asr_Model, Tsl_Model


def init_model(asr_init: schemas.AsrInit, tsl_init: schemas.M2M100Init):
    Asr_Model.model_load(model_type=asr_init.model_type,
                         device=utils.get_device(asr_init.device))

    Tsl_Model.model_load(model_path=tsl_init.model_path,
                         device=utils.get_device(tsl_init.device))
    return "模型初始化完成"


def asr_inference(audio_path, audio_lang, is_verbose=False, use_fp16=False):
    return Asr_Model.transcribe(audio_path=audio_path,
                                audio_lang=audio_lang,
                                is_verbose=is_verbose,
                                use_fp16=use_fp16)


def tsl_inference(texts, src_lang, tgt_lang, gs=10):
    return Tsl_Model.translate(transcription_res=texts,
                               src_lang=src_lang,
                               tgt_lang=tgt_lang,
                               gs=gs,
                               is_whisper=False)
