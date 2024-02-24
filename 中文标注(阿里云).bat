@echo off
chcp 65001
@title VITS数据自动标注-ZH 
set path=.\env\Scripts;.\env;ffmpeg\bin;%path%
echo =====
echo 请确定所有的音频已经按标准处理完毕，否则必报错！
echo =====
echo.
.\workenv\python.exe DataLabeling_ali_ZH.py
pause
