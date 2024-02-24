import os
import argparse
from faster_whisper import WhisperModel



def transcribe_whisper(audio_path, model, model_size="large-v3", device="cuda", compute_type="float16"):
    local_dir = "./Model/faster-whisper-large-v3"
    model = WhisperModel(model_size_or_path=local_dir, device=device, compute_type=compute_type)

    segments, info = model.transcribe(audio_path, beam_size=5,vad_filter=True,
                                      vad_parameters=dict(min_silence_duration_ms=1000))

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    # 将生成器对象转换为列表
    segments_list = list(segments)

    for segment in segments_list:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    # 返回语言和文本信息
    return info.language, segments_list  # 返回整个分段列表

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--languages", default="CJE")
    parser.add_argument("--model_size", default="large-v3")
    parser.add_argument("--local_dir", default="./Model/faster-whisper-large-v3")
    parser.add_argument("--input_dir", default="./raw")
    args = parser.parse_args()

    model = WhisperModel(model_size_or_path=args.local_dir, device="cuda", compute_type="float16")

    lang2token = {
        'zh': "ZH",
        'ja': "JP",
        'en': "EN",
    }

    speaker_annos = ""  # 使用字符串存储整个文本
    processed_files = 0

for file in list(os.walk(args.input_dir))[0][2]:
    try:
        if file[-3:] != 'wav':
            print(f"{file} not supported, ignoring...\n")
            continue

        lang, segments = transcribe_whisper(audio_path=os.path.join(args.input_dir, file), model=model)

        # 对每个文件的分段文本进行累加
        file_text = ""
        for segment in segments:
            file_text += segment.text + "，"  # 使用逗号连接分段文本

        # 将文本追加到整个文本中
        prefix = file.rsplit('_', 1)[0]  # 去除最后一个下划线及其后面的内容
        speaker_annos += f"./data/{prefix}/wavs/{file}|{prefix}|{lang2token[lang]}|{file_text[:-1]}\n"  # 去除末尾多余的逗号

        processed_files += 1
        print(f"Processed: {processed_files}/{len(list(os.walk(args.input_dir))[0][2])}")

    except Exception as e:
        print(f"Error processing {file}: {str(e)}")

with open("./speakers_index.txt", 'w', encoding='utf-8') as f:
    f.write(speaker_annos)

os.rename("./speakers_index.txt", "./esd.list")



