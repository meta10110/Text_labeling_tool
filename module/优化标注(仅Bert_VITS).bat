@echo off
@title Bert_VITS2 ��ע���� 
set path=.\env\Scripts;.\env;ffmpeg\bin;%path%
echo =====
echo ��ע�⣡����Ҫ����ɱ�ע��������ִ�н�ɾ�����к�Ӣ����ĸ�����̵ı�ע����
echo =====
echo.
pause
.\workenv\python.exe auto_DataLabeling_clean_list.py
pause
