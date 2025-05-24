REM @echo off
REM:loop
REMcls
REM python starter.py
REM timeout /t 2 
REM goto loop

REM @echo off
REM :loop
REM cls
REM =======================================
REM Met à jour le code depuis le dépôt Git
IF EXIST .git (
    git pull
) ELSE (
    git clone <URL_DU_DEPOT_GIT> .
)
cls
REM Met à jour les dépendances Python
pip install -r upload.txt

cls
REM Démarre le bot
python starter.py

timeout /t 2 
goto loop