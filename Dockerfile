FROM python:3.12-slim

WORKDIR /app

# ffmpeg requis par pydub pour les conversions audio
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY execution/titan/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code titan comme package
COPY execution/titan/ ./titan/

# Copier les portfolios HTML (servis par command_server)
COPY portfolios/ ./portfolios/

CMD ["python", "-m", "titan"]
