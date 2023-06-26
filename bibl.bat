@echo off

call %~dp0venv\Scripts\activate

python  %~dp0bibl\manage.py runserver 127.0.0.1:80

pause