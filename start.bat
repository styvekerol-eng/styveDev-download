@echo off
setlocal
cd /d "%~dp0"
title StyveDev Download Pro - PWA v4.0

set PYTHON_BIN="C:\Users\StyveDev-PC\AppData\Local\Programs\Python\Python315\python.exe"
if not exist %PYTHON_BIN% set PYTHON_BIN=python

echo ======================================================================
echo           STYVEDEV DOWNLOAD PRO - PWA INSTALLABLE v4.0
echo ======================================================================
echo.
echo [*] Demarrage du serveur PWA...
echo [*] Le navigateur va s'ouvrir sur http://127.0.0.1:8765...
echo.

%PYTHON_BIN% "%~dp0server.py"

if errorlevel 1 (
    echo.
    echo [ERREUR] Le serveur s'est arrete.
    pause
)
