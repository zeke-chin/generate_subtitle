import copy
from typing import List

from tqdm import tqdm


def convert_to_subtitle(tsr_res: List[dict], format='srt'):
    if format == 'srt':
        sub = segments_to_srt(tsr_res)
    elif format == 'txt':
        sub = transcribed_text(tsr_res)
    else:
        raise ValueError(f"format {format} is not supported!")
    return sub


def merge_translated(tsr_res, trl_res, format, type='top'):
    tsr_res = copy.deepcopy(tsr_res['segments'])
    keep_both = type != 'translation only'
    comb = []
    for s, tr in zip(tsr_res, trl_res):
        if not keep_both:
            c = f"{tr}\n"
        elif type == 'top':
            c = f"{tr.strip()}\\N\\N{s['text'].strip()}\n"
        else:
            c = f"{s['text'].strip()}\\N{tr.strip()}\n"
        s['text'] = c
        comb.append(s)
    return convert_to_subtitle(comb, format)


def segments_to_srt(tsr_res):
    # sourcery skip: merge-list-appends-into-extend, use-fstring-for-concatenation
    text = []
    for i, s in tqdm(enumerate(tsr_res)):
        text.append(str(i + 1))

        time_start = s['start']
        hours, minutes, seconds = int(time_start / 3600), (time_start / 60) % 60, (time_start) % 60
        timestamp_start = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
        timestamp_start = timestamp_start.replace('.', ',')
        time_end = s['end']
        hours, minutes, seconds = int(time_end / 3600), (time_end / 60) % 60, (time_end) % 60
        timestamp_end = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
        timestamp_end = timestamp_end.replace('.', ',')
        text.append(timestamp_start + " --> " + timestamp_end)

        text.append(s['text'].strip() + "\n")

    return "\n".join(text)


def transcribed_text(tsr_res):
    texts = [s['text'] for s in tsr_res]
    return '\n'.join(texts)
