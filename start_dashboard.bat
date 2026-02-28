@echo off
chcp 65001 >nul
title TITAN-COMMAND Dashboard Server

cd /d "%~dp0"

:: Activate venv if exists
if exist ".venv\Scripts\activate.bat" call .venv\Scripts\activate.bat

:: Get local IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4"') do (
    set LOCAL_IP=%%a
    goto :found
)
:found
set LOCAL_IP=%LOCAL_IP: =%

echo.
echo  ========================================
echo   TITAN-COMMAND Dashboard
echo  ========================================
echo.
echo   PC : http://localhost:7777
echo.
echo   Lancement du serveur + tunnel mobile...
echo  ========================================
echo.

:: 1. Start command_server in background
start /B python -m execution.titan.command_server > nul 2>&1

:: 2. Wait for server to be ready
timeout /t 3 /nobreak > nul

:: 3. Start cloudflared tunnel and capture URL
set TUNNEL_LOG=%TEMP%\cloudflared_titan.log
del "%TUNNEL_LOG%" 2>nul

start /B cloudflared tunnel --url http://localhost:7777 > "%TUNNEL_LOG%" 2>&1

:: 4. Wait for tunnel URL
echo  En attente du lien mobile...
:wait_url
timeout /t 2 /nobreak > nul
findstr /C:"trycloudflare.com" "%TUNNEL_LOG%" > nul 2>&1
if errorlevel 1 goto wait_url

:: 5. Extract the URL
for /f "tokens=*" %%u in ('findstr /C:"trycloudflare.com" "%TUNNEL_LOG%"') do set TUNNEL_LINE=%%u
:: Parse out just the URL
for /f "tokens=2 delims=|" %%u in ('findstr /C:"https://" "%TUNNEL_LOG%" ^| findstr /C:"trycloudflare"') do set TUNNEL_URL=%%u
:: Clean spaces
for /f "tokens=* delims= " %%a in ("%TUNNEL_URL%") do set TUNNEL_URL=%%a

echo.
echo  ========================================
echo   TITAN-COMMAND — ONLINE
echo  ========================================
echo.
echo   PC     : http://localhost:7777/titan_command.html
echo   MOBILE : %TUNNEL_URL%/titan_command.html
echo.
echo   (Tower + RPG = tabs dans le dashboard)
echo  ========================================
echo.

:: 6. Send ONE link to Telegram (dashboard = single entry point)
curl -s -X POST "https://api.telegram.org/bot8297302366:AAF238_hmMiNswfAzjPde1lEsNdL_O9k30o/sendMessage" --data-urlencode "chat_id=7296657097" --data-urlencode "text=TITAN-COMMAND: %TUNNEL_URL%/titan_command.html" > nul 2>&1

echo   Lien envoye sur Telegram !
echo.
echo   (Ne ferme pas cette fenetre)
echo.

:: Keep alive
:keep_alive
timeout /t 60 /nobreak > nul
goto keep_alive
