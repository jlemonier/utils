@REM Sets title

call wldir

set logdir=C:\lf

touch %logdir%\startApp.log
touch %logdir%\startApp.err
start tailit %logdir%\startApp.log
start tailit %logdir%\startApp.err

title Start WL - %logdir%\startApp.log .err

startApp -autoload -debug > %logdir%\startApp.log 2> %logdir%\startApp.err

