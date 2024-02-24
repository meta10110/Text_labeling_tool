# 导入必要的模块和库
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os

'''
# 示例代码，用于测试语音识别模型的输出结果
inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='./Model/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
)

rec_result = inference_pipeline(audio_in='ge_1570_2.wav')
print(rec_result)
# {'text': '欢迎大家来体验达摩院推出的语音识别模型'}
'''

# 设置输入目录、模型目录等变量
parent_dir = "./raw/"
local_dir_root = "./Model/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
target_sr = 44100

# 创建空列表用于存储已处理过的音频文件路径
complete_list = []

# 获取输入目录中的文件列表
filelist = list(os.walk(parent_dir))[0][2]

# 如果存在已完成的音频注释文件，读取已完成的音频列表
if os.path.exists('fast_vits.list'):
    with open("./fast_vits.list", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            pt, _, _ = line.strip().split('|')
            complete_list.append(pt)

# 创建自动语音识别管道
inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model=local_dir_root,
)

# 对每个音频文件进行处理
for file in filelist:
    # 如果文件不是.wav格式，忽略
    if file[-3:] != 'wav':
        print(f"{file} 不支持，忽略...\n")
        continue
    print(f"转录 {parent_dir + file}...\n")

    # 提取角色名
    character_name = file.rstrip(".wav").split("_")[0]
    savepth1 = "./dataset/" + character_name + "/" "wavs" + "/" + file
    savepth2 = "./data/" + character_name + "/" "wavs" + "/" + file

    # 如果文件已经处理过，跳过
    if savepth1 in complete_list:
        print(f'{file} 已完成，跳过!')
        continue
    if savepth2 in complete_list:
        print(f'{file} 已完成，跳过!')
        continue

    # 进行语音识别
    rec_result = inference_pipeline(audio_in=parent_dir + file)

    # 如果未识别到文本，跳过
    if 'text' not in rec_result:
        print("文本未被识别，忽略...\n")
        continue

    # 处理识别结果，生成注释文本
    annos_text = rec_result['text']
    annos_text = '[ZH]' + annos_text.replace("\n", "") + '[ZH]'
    annos_text = annos_text + "\n"

    # 将结果写入文件
    line1 = savepth1 + "|" + character_name + "|" + annos_text
    line2 = savepth2 + "|" + character_name + "|ZH|" + rec_result['text'] + "\n"
    with open("./fast_vits.list", 'a', encoding='utf-8') as f:
        f.write(line1)
    with open(f"./esd.list", 'a', encoding='utf-8') as f:
        f.write(line2)

    print(rec_result)

print("完成!\n")
