@echo off
REM auto_harvest.bat — Lance le moissonneur automatiquement
REM Tu peux planifier ce fichier dans le Planificateur de taches Windows :
REM   - toutes les heures
REM   - a la fermeture de session
REM   - le matin au demarrage
REM
REM Pour planifier : Win+R → taskschd.msc → Creer une tache de base

cd /d "c:\Users\augus\Desktop\WORKSPACE AICO"

REM Charger les variables d'environnement
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if not "%%a"=="" if not "%%b"=="" (
        set %%a=%%b
    )
)

REM Lancer le moissonneur en silencieux
python memory/self_harvester.py --last --quiet

REM Log minimal
echo [%date% %time%] Harvest done >> memory\harvest_cron.log
