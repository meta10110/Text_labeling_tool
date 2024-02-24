# 导入必要的模块和库
import os
import re

# 创建空列表用于存储原始注释和清理后的注释
new_annos = []
cleaned_new_annos = []

# 如果存在原始注释文件"esd.list"，读取其中的注释
if os.path.exists("./esd.list"):
    with open("./esd.list", 'r', encoding='utf-8') as f:
        long_character_anno = f.readlines()
        new_annos += long_character_anno
else:
    print('esd.list，请确认路径是否正确')
    exit()

# 对每一行注释进行处理
for line in new_annos:
    path, name, lang, text = line.split("|")
    text += "\n" if not text.endswith("\n") else ""  # 如果文本末尾不是换行符，添加一个换行符
    if len(text) >= 5:  # 仅处理长度大于等于5的文本
        my_re = re.compile(r'[A-Za-z]', re.S)
        res = re.findall(my_re, text)
        if len(res):
            print(f'跳过非汉字文本: {text}')
        else:
            cleaned_new_annos.append(path + "|" + name + "|" + lang+ "|" + text)
    else:
        print(f'跳过过短的wav文本: {text}')

# 将清理后的注释写入新文件"clean_esd.list"
with open("./clean_esd.list", 'w', encoding='utf-8') as f:
    for line in cleaned_new_annos:
        f.write(line)

print('完成！保存为clean_esd.list')
