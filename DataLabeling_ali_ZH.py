# 导入所需的库和模块
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os

# 定义自动语音识别任务的模型路径
local_dir_model = "./Model/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch"

# 初始化自动语音识别任务的管道
inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model=local_dir_model
)

# 指定存储原始音频文件的父目录
parent_dir = "./raw/"
filelist = list(os.walk(parent_dir))[0][2]

# 读取已完成处理的文件列表
complete_list = []
if os.path.exists('fast_vits.txt'):
    with open("./fast_vits.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            pt, _, _ = line.strip().split('|')
            complete_list.append(pt)

# 遍历音频文件列表进行语音识别和处理
for file in filelist:
    # 检查文件格式是否为wav
    if file[-3:] != 'wav':
        print(f"{file} not supported, ignoring...\n")
        continue

    print(f"转录 {parent_dir + file}...\n")

    # 提取角色名称和存储路径
    character_name = file.rstrip(".wav").split("_")[0]
    savepth1 = "./dataset/" + character_name + "/" "wavs" + "/" + file
    savepth2 = "./data/" + character_name + "/" "wavs" + "/" + file

    # 检查文件是否已处理过
    if savepth1 in complete_list:
        print(f'{file} is already done, skip!')
        continue
    if savepth2 in complete_list:
        print(f'{file} is already done, skip!')
        continue

    # 进行语音识别
    rec_result = inference_pipeline(audio_in=parent_dir + file)

    # 检查是否成功识别文本
    if 'text' not in rec_result:
        print("Text is not recognized，ignoring...\n")
        continue

    # 处理识别结果并写入文件
    annos_text = rec_result['text']
    annos_text = '[ZH]' + annos_text.replace("\n", "") + '[ZH]'
    annos_text = annos_text + "\n"
    line1 = savepth1 + "|" + character_name + "|" + annos_text
    line2 = savepth2 + "|" + character_name + "|ZH|" + rec_result['text'] + "\n"

    with open("./fast_vits.list", 'a', encoding='utf-8') as f:
        f.write(line1)
    with open(f"./esd.list", 'a', encoding='utf-8') as f:
        f.write(line2)
    print(rec_result['text'])

print("完成!\n")
