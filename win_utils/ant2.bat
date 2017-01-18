call rel

set logdir=C:\lf

touch %logdir%\ant_copyconfig.log
start tailit %logdir%\ant_copyconfig.log

title ant copyconfig

call rel
ant copyconfig > c:\lf\ant_copyconfig.log



