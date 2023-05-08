from pydantic import BaseModel


class AsrInit(BaseModel):
    model_type: str
    device: str

    class Config:
        schema_extra = {
            "example": {
                "model_type": "tiny-->39M, base-->74M, small-->244M, medium-->769M, large-->1550M",
                "device": "cpu or cuda or cuda:1"
            }
        }


class AsrInference(BaseModel):
    audio_path: str
    audio_lang: str
    is_verbose: bool = False
    use_fp16: bool = False

    class Config:
        schema_extra = {
            "example": {
                "audio_path": "audio.wav",
                "audio_lang": "en",
                "is_verbose": False,
                "use_fp16": False,
            }
        }
