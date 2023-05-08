import whisper


class AsrModel(object):
    def __init__(self, model_type, device):
        self.model_type = model_type
        self.device = device
        self.model = None

        self.model_load(model_type, device)

    def model_load(self, model_type, device):
        print('whisper 模型加载中')
        self.model = whisper.load_model(name=model_type, device=device, download_root='/workspace/models/whisper_models')
        print(f"whisper 模型加载完成 {model_type} {device}")
        return True

    def transcribe(self, audio_path, audio_lang, is_verbose=False, use_fp16=False):
        # 构建解码器
        options = whisper.DecodingOptions(fp16=use_fp16, language=audio_lang)
        # 解码
        res = self.model.transcribe(audio_path, **options.__dict__, verbose=is_verbose)
        print("whisper 模型推理完成")
        return res
