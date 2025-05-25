@echo off
color 0A

:loop
cls
echo ==================================================
echo   [SYNCHRONISATION DU CODE AVEC LE REPOSITORY GIT]
echo ==================================================
echo.

REM Met à jour le code depuis le dépôt Git (évite les doublons)
echo [1/3] Recuperation des dernieres modifications du depot distant...
git pull
IF ERRORLEVEL 1 (
    echo [ERREUR] Echec du git pull. Verifiez votre connexion ou le repository.
    timeout /t 5 >nul
    goto loop
)
echo --------------------------------------------------

REM Met à jour les dépendances Python
echo [2/3] Mise a jour des dependances Python...
pip install -r upload.txt
IF ERRORLEVEL 1 (
    echo [ERREUR] Echec de l'installation des dependances Python.
    timeout /t 5 >nul
    goto loop
)
echo --------------------------------------------------

echo.
echo =====================[ DEMARRAGE DU BOT ]=====================
timeout /t 2 >nul
echo [3/3] Lancement du bot...
cls
python starter.py
IF ERRORLEVEL 1 (
    echo [ERREUR] Le bot s'est arrete avec une erreur.
    timeout /t 5 >nul
)
timeout /t 2 >nul
goto loop