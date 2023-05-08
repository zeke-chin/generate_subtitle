from typing import List

from tqdm import tqdm
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


class M2MModel(object):
    def __init__(self, model_path, device):
        self.model_path = model_path
        self.device = device
        self.model = None
        self.tokenizer = None

        self.model_load(model_path, device)

    def model_load(self, model_path, device):
        print('m2m100 模型加载中')
        self.model = M2M100ForConditionalGeneration.from_pretrained(model_path).to(self.device)
        self.tokenizer = M2M100Tokenizer.from_pretrained(model_path)
        print(f"m2m100 模型加载完成 {model_path} {device}")
        return True

    def translate(self, transcription_res, src_lang, tgt_lang, gs, is_whisper=True):
        self.texts = batch_whisper_text(transcription_res, gs=gs) if is_whisper else batch_text(transcription_res, gs=gs)
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        res = self._batch_translate
        print("m2m100 模型推理完成")
        return res

    @property
    def _batch_translate(self):
        """
        Translate a long list of texts
        翻译一个长文本列表
        :param src_lang:
        :param tgt_lang:
        :return:
        """
        translated = []
        for t in tqdm(self.texts):
            tt = self._translate(t)
            translated += tt
        return translated

    def _translate(self, text: List[str]):
        """
        Call the model for translation
        调用模型进行翻译
        :param text:
        :param src_lang:
        :param tgt_lang:
        :return:
        """
        # 设置编码器的语言
        self.tokenizer.src_lang = self.src_lang
        # 构建编码器
        encoded = self.tokenizer(text, return_tensors="pt", padding=True).to(self.device)
        # 生成tokens
        generated_tokens = self.model.generate(**encoded,
                                               forced_bos_token_id=self.tokenizer.get_lang_id(self.tgt_lang))
        # 解码
        return self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

def batch_whisper_text(transcription_res, gs):
    """
    split list into small groups of group size `gs`.
    将长列表分割成小列表，每个小列表的长度为gs，目的是为了防止一次性将长列表传入模型，导致内存(显存)溢出
    :param transcription_res: 语音识别结果
    :param gs: 小列表的长度
    :return:
    """
    segs = transcription_res['segments']
    length = len(segs)
    mb = length // gs
    text_batches = []
    for i in range(mb):
        text_batches.append([s['text'] for s in segs[i*gs:(i+1)*gs]])
    if mb*gs != length:
        text_batches.append([s['text'] for s in segs[mb*gs:length]])
    return text_batches

def batch_text(lst: List[str], gs: int) -> List[List[str]]:
    return [lst[i:i + gs] for i in range(0, len(lst), gs)]

# def chunk_list(lst: List[str], chunk_size: int) -> List[List[str]]:
#     return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


