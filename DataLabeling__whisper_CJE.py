import whisper
import os
import json
import torchaudio
import argparse
import torch
import whisper

lang2token = {
            'zh': "[ZH]",
            'ja': "[JP]",
            "en": "[EN]",
        }

def transcribe_one(audio_path):
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_path)  # 函数加载音频文件
    audio = whisper.pad_or_trim(audio)      # 函数对音频进行填充或修剪，以确保其长度适合30秒

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)   # 生成音频的对数梅尔频谱图

    # detect the spoken language
    _, probs = model.detect_language(mel)                # 利用模型的 detect_language 方法，检测音频中的语言
    print(f"Detected language: {max(probs, key=probs.get)}")  
    lang = max(probs, key=probs.get)                     # 获取语言检测的结果概率，并输出概率最高的语言
    # decode the audio
    options = whisper.DecodingOptions(beam_size=5)       # 创建 whisper.DecodingOptions 对象，指定解码的选项，例如束搜索的大小。
    result = whisper.decode(model, mel, options)         # 利用 whisper.decode 函数对梅尔频谱图进行解码，生成识别结果。

    # print the recognized text
    print(result.text)                                   # 打印检测到的语言和识别的文本结果
    return lang, result.text                             # 返回检测到的语言和识别的文本结果


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--languages", default="CJE")
    parser.add_argument("--whisper_size", default="Model/whisper/medium.pt")
    parser.add_argument("--input_dir", default="./raw")
    args = parser.parse_args()
    if args.languages == "CJE":
        lang2token = {
            'zh': "ZH",
            'ja': "JP",
            "en": "EN",
        }
    elif args.languages == "CJ":
        lang2token = {
            'zh': "ZH",
            'ja': "JP",
        }
    elif args.languages == "C":
        lang2token = {
            'zh': "ZH",
        }
    elif args.languages == "J":
        lang2token = {
            'ja': "JP",
        }

    if len(lang2token) == 0:
        pass
    else:
        pass
    assert (torch.cuda.is_available()), "Please enable GPU in order to run Whisper!"
    model = whisper.load_model(args.whisper_size)
    parent_dir = args.input_dir

    target_sr = 44100
    processed_files = 0

    
    filelist = list(os.walk(parent_dir))[0][2]


    speaker_annos = []
    # resample audios
    # 2023/4/21: Get the target sampling rate
    for file in filelist:
        # transcribe text
        character_name = file.rstrip(".wav").split("_")[0]
        savepth = "./data/" + character_name + "/" + "wavs" + "/" + file
        total_files = sum([len(files) for r, d, files in os.walk(parent_dir)])
        
        if file[-3:] != 'wav':
            print(f"{file} not supported, ignoring...\n")
            continue
        
        lang, text = transcribe_one(audio_path=os.path.join(parent_dir, file))
        
        if lang not in lang2token:
            print(f"{lang} not supported, ignoring...\n")
            continue

        text = lang2token[lang] + "|" + text  + "\n"
        speaker_annos.append(savepth + "|" + character_name + "|" + text)

        processed_files += 1
        print(f"Processed: {processed_files}/{total_files}")

    with open("./speakers_index.txt", 'w', encoding='utf-8') as f:
        for line in speaker_annos:
            f.write(line)
    
    os.rename("./speakers_index.txt","./esd.list")
    
    
    # if len(speaker_annos) == 0:
    #     print("Warning: no short audios found, this IS expected if you have only uploaded long audios, videos or video links.")
    #     print("this IS NOT expected if you have uploaded a zip file of short audios. Please check your file structure or make sure your audio language is supported.")
    # with open("./filelists/speakers_index.txt", 'w', encoding='utf-8') as f:
    #     for line in speaker_annos:
    #         f.write(line)
    
    # os.rename("./filelists/speakers_index.txt","./filelists/speaker.list")
    # # import json
    # # # generate new config
    # # with open("./configs/finetune_speaker.json", 'r', encoding='utf-8') as f:
    # #     hps = json.load(f)
    # # # modify n_speakers
    # # hps['data']["n_speakers"] = 1000 + len(speaker2id)
    # # # add speaker names
    # # for speaker in speaker_names:
    # #     hps['speakers'][speaker] = speaker2id[speaker]
    # # # save modified config
    # # with open("./configs/modified_finetune_speaker.json", 'w', encoding='utf-8') as f:
    # #     json.dump(hps, f, indent=2)
    # # print("finished")