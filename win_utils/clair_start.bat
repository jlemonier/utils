call e:\apps\python35\Scripts\workon.bat clair5

e:
cd \apps\django\clair

pip install pymysql
pip install django
pip install E:\apps\PythonEnv\python_wheel\mysqlclient-1.3.9-cp35-cp35m-win32.whl

set DJANGO_SETTINGS_MODULE=project_clair.settings
set |grep DJANGO

python manage.py runserver 0.0.0.0:8000