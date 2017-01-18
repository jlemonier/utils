@echo off
cls
echo Now ...
which python.exe
echo .

echo .
echo After ...
set PATH=C:\apps\python27;C:\apps\python27\Scripts;%PATH%
set |grep Path

echo .
which python.exe
which pip.exe
which virtualenv.exe
which workon.bat
echo .
