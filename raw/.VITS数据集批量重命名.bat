@echo off

title VITS���ݼ����������� 

echo=
echo -------------------------------------------------------------------------------
echo VITS���ݼ�����������  
echo=
echo �뽫������������Ŀ���ļ��к�������
echo=
echo �������Զ����������ļ���������wav��ʽ���ļ�Ϊ ��˵����ɫ_����.wav�� �����ı�������
echo=
echo=���������Ŀ���ļ�����
echo=
echo=�������رգ���ֹ�������޸�!
echo=
echo=��������ָ�ԭ���뱣��   �ļ����ձ�.txt  
echo=
echo=����ͬһĿ¼������ �ָ�ԭ��.bat
echo ----------------------------------------------------------------------------------
echo=

echo=
echo=

set a=1

echo ������˵����������ע��ֻ֧�ִ���ĸ�������

set /p name=:

setlocal EnableDelayedExpansion

for /f "delims=" %%i in ('dir /b *.*') do (

set "fn=%%~nxi" 

if "wav"=="!fn:~-3!" (ren "%%i" "%name%_!a!.wav" && echo "%%i->%name%_!a!.wav" & echo "%%i->%name%_!a!.wav">>�ļ����ձ�.txt & set /A a+=1) 

)

echo=
echo=
echo Done^^!

set /p u=
