FROM python:3.12-slim

WORKDIR /app

# ffmpeg requis par pydub pour les conversions audio
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy titan as a package inside /app/titan/
COPY . ./titan/

CMD ["python", "-m", "titan"]
