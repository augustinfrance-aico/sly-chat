FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy titan as a package inside /app/titan/
COPY . ./titan/

CMD ["python", "-m", "titan"]
