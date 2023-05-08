from typing import List

from pydantic import BaseModel


class M2M100Init(BaseModel):
    model_path: str
    device: str

    class Config:
        schema_extra = {
            "example": {
                "model_type": "facebook/m2m100_418M-->39M, facebook/m2m100_1.2B-->74M（建议下载后使用绝对路径）",
                "device": "cpu or cuda or cuda:1"
            }
        }


class M2M100Inference(BaseModel):
    texts: List[str]
    src_lang: str
    tgt_lang: str
    gs: int = 10

    class Config:
        schema_extra = {
            "example": {
                "texts": ["Hello world"],
                "src_lang": "en",
                "tgt_lang": "zh",
                "gs": 10,
            }
        }
