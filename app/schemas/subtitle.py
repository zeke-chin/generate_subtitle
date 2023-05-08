from pydantic import BaseModel


class Transcription(BaseModel):
    # audio_path, audio_lang, is_verbose = False, use_fp16 = False, format_ = 'srt'
    audio_path: str
    audio_lang: str
    is_verbose: bool = False
    use_fp16: bool = False
    format_: str = 'srt'

    class Config:
        schema_extra = {
            "example": {
                "audio_path": "audio.wav",
                "audio_lang": "en",
                "is_verbose": False,
                "use_fp16": False,
                "format_": "srt"
            }
        }

class Translation(BaseModel):
    # audio_path, audio_lang, target_lang, gs = 10, is_verbose = False, use_fp16 = False, type_ = 'top', format_ = 'srt'
    audio_path: str
    audio_lang: str
    target_lang: str
    gs: int = 10
    is_verbose: bool = False
    use_fp16: bool = False
    type_: str = 'top'
    format_: str = 'srt'

    class Config:
        schema_extra = {
            "example": {
                "audio_path": "audio.wav",
                "audio_lang": "en",
                "target_lang": "zh",
                "gs": 10,
                "is_verbose": False,
                "use_fp16": False,
                "type_": "top",
                "format_": "srt"
            }
        }