call rel

set logdir=C:\lf

touch %logdir%\ant.log
start tailit %logdir%\ant.log

title ant 

ant > c:\lf\ant.log



