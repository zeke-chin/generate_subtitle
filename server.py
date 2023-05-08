import torch
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import utils
from app.models.Asr import AsrModel
from app.models.Translation import M2MModel

# **********************************************************************************************************************
app = FastAPI(docs_url='/docs', title="语音/视频 转录/翻译 字幕服务")
# CORS 跨源资源共享
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
utils.format_print()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)
# model_type = ["tiny", "base", "small", "medium", "large"]
Asr_Model = AsrModel(model_type='tiny', device=device)
Tsl_Model = M2MModel(model_path='/workspace/models/m2m100_418M', device=device)

print("服务初始化完成")
# **********************************************************************************************************************
from app import routers


app.include_router(routers.router_file)
app.include_router(routers.router_model)
app.include_router(routers.router_subtitle)


#
# @app.post("/model/init", tags=["model"], summary="初始化模型")
# async def init_model(asr_init: schemas.AsrInit, tsl_init: schemas.M2M100Init):
#     global asr_model, tsl_model
#     asr_model = models.AsrModel(model_type=asr_init.model_type,
#                                 device=utils.get_device(asr_init.device))
#     tsl_model = models.M2MModel(model_path=tsl_init.model_path,
#                                 device=utils.get_device(tsl_init.device))
#     return "模型初始化完成"
#
#
# @app.post("/transcription", tags=["asr"], summary="语音转字幕")
# async def asr(asr: schemas.Asr):
#     pass
#
#
# @app.post("/tsl", tags=["tsl"], summary="翻译")
# async def tsl(tsl: schemas.Tsl):
#     pass
@app.get("/ping")
async def ping():
    return "pong"


if __name__ == '__main__':
    import argparse
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=8080)
    opt = parser.parse_args()

    # app_str = 'file_server:app'  # make the app string equal to whatever the name of this file is
    app_str = 'server:app'  # make the app string equal to whatever the name of this file is
    uvicorn.run(app_str, host=opt.host, port=int(opt.port), reload=True, timeout_keep_alive=60)
