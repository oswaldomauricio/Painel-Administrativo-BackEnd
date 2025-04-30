@echo off
cd /d "C:\Users\oswaldo.adm\Documents\GitHub\Painel-Administrativo-BackEnd\server"
call .\.venv\Scripts\activate
flask run --reload --host=0.0.0.0
pause