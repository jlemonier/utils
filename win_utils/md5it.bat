@echo off
title Run md5 On %1 - compare to %1.md5
echo See %1.md5 ...
cat %1.md5
echo.
echo.
echo See %1 - calculated MD5 ...
d:\utils\md5 %1
pause