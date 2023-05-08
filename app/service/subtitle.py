import utils
from app.service import file
from server import Asr_Model, Tsl_Model


def get_tsr_sub(audio_path, audio_lang, is_verbose=False, use_fp16=False, format_='srt'):
    """
    语音转字幕
    :param audio_path: 语音文件路径
    :param audio_lang: 语音语言
    :param is_verbose: 是否输出推理信息
    :param use_fp16: 是否使用 fp16 推理
    :param format_: 字幕格式
    :return: 字幕路径
    """
    # sourcery skip: inline-immediately-returned-variable
    # 转录结果
    tsr_result = Asr_Model.transcribe(audio_path=audio_path,
                                      audio_lang=audio_lang,
                                      is_verbose=is_verbose,
                                      use_fp16=use_fp16)
    # 转换为字幕
    sub_result = utils.convert_to_subtitle(tsr_res=tsr_result['segments'],
                                           format=format_)
    # 保存字幕
    sub_path = file.save_sub(audio_path=audio_path,
                             sub_str=sub_result,
                             sub_label=audio_lang,
                             format_=format_)
    return sub_path


def get_tsl_sub(audio_path, audio_lang, target_lang, gs=10, is_verbose=False, use_fp16=False, type_='top',
                format_='srt'):
    """
    语音转双语字幕
    :param audio_path: 语音文件路径
    :param audio_lang: 语音语言
    :param target_lang: 目标语言
    :param gs: 翻译模型一次推理的句子数量(根据现存调整 越大越快，但是可能会 OOM)
    :param is_verbose: 是否输出推理信息
    :param use_fp16: 是否使用 fp16 推理
    :param type_: 双语字幕类型 ["top", "bottom", "translation only"]
    :param format_: 字幕格式
    :return: 字幕路径
    """
    # sourcery skip: inline-immediately-returned-variable, use-fstring-for-concatenation
    # 转录结果
    tsr_result = Asr_Model.transcribe(audio_path=audio_path,
                                      audio_lang=audio_lang,
                                      is_verbose=is_verbose,
                                      use_fp16=use_fp16)
    # 翻译结果
    trl_result = Tsl_Model.translate(transcription_res=tsr_result,
                                     src_lang=audio_lang,
                                     tgt_lang=target_lang,
                                     gs=gs)
    # 转换为字幕
    sub_result = utils.merge_translated(tsr_res=tsr_result,
                                        trl_res=trl_result,
                                        type=type_,
                                        format=format_)
    # 保存字幕
    sub_path = file.save_sub(audio_path=audio_path,
                             sub_str=sub_result,
                             sub_label=target_lang + '_' + audio_lang,
                             format_=format_)
    return sub_path
