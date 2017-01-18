@echo off
cls
echo Now ...
which python.exe
echo .

echo .
echo After ...
set PATH=e:\apps\python35;e:\apps\python35\Scripts;%PATH%
set |grep Path

echo .
which python.exe
which pip.exe
which virtualenv.exe
which workon.bat
echo .

title Python 3.5