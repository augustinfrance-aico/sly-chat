@echo off
title TITAN-COMMAND Dashboard Server
echo.
echo  ████████╗██╗████████╗ █████╗ ███╗   ██╗
echo  ╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║
echo     ██║   ██║   ██║   ███████║██╔██╗ ██║
echo     ██║   ██║   ██║   ██╔══██║██║╚██╗██║
echo     ██║   ██║   ██║   ██║  ██║██║ ╚████║
echo     ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
echo.
echo  TITAN-COMMAND — Dashboard Server
echo  ================================
echo.

cd /d "%~dp0"

:: Get local IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4"') do (
    set LOCAL_IP=%%a
    goto :found
)
:found
set LOCAL_IP=%LOCAL_IP: =%

echo  PC     : http://localhost:7777/titan_command.html
echo  Mobile : http://%LOCAL_IP%:7777/titan_command.html
echo.
echo  UN SEUL LIEN = tout (Dashboard + Moon Tower + RPG)
echo.
echo  Ajouter comme app sur ton tel :
echo  iPhone  : Safari ^> Partager ^> Sur l'ecran d'accueil
echo  Android : Chrome ^> Menu 3 points ^> Ajouter a l'ecran d'accueil
echo.
echo  ================================
echo.

python -m execution.titan.command_server
pause
