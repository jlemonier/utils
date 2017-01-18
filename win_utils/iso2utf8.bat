REM Expects %1 to be quoted already
copy /y %1 %1.bak
iconv -f iso-8859-1 -t utf-8 %1.bak > %1
diff %1.bak %1 > %1.latin1_utf8_diff.log
cat %1.latin1_utf8_diff.log
