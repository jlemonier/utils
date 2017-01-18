@echo off
title %1 WebLogic -64bit ++ %2 %3 %4 %5 %6

if "%1" == "" goto usage

set stdout=c:\lf\wl_%1.log
set stderr=c:\lf\wl_%1.err
echo startApp -64bit %2 %3 %4 %5 %6 now -- see %stdout% 
startApp -64bit %2 %3 %4 %5 %6          > %stdout%  

REM and %stderr%
REM startApp -64bit %2 %3 %4 %5 %6          > %stdout%  2> %stderr%

goto done

:usage
echo Usage: startWL App  OR  startWL WebApp 

:done