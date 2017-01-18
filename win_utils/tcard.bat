@echo off

set relpath=C:\code\gtnexus\development\modules\main\tcard

title GTNexus tcard Project - %relpath%
cd %relpath%

call ant generateMBOs
