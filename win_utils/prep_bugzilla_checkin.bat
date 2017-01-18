
REM CoffeeCup Editor tradintra1 
REM   => C:\Users\jlemonier\Documents\CoffeeCup Software\HTML Editor\Projects\data_www\testenv\bugzilla\html

REM Eclipse Bugzilla project
REM   => E:\src\rel_trunk\Bugzilla\data\www\bugzilla\html

set srcdir=C:\Users\jlemonier\Documents\CoffeeCup Software\HTML Editor\Projects\data_www\testenv\bugzilla\html
set destdir=E:\src\rel_trunk\Bugzilla\data\www\bugzilla\html

copy "%srcdir%\*.cgi" "%destdir%\"

copy "%srcdir%\*.pl" "%destdir%\"