FROM python:3.11-slim

WORKDIR /app

# Másoljuk a függőségeket és telepítjük
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Másoljuk a scriptet (Figyelj, hogy a fájlneved pontos legyen!)
COPY rss_sorter.py .

# Amikor elindul a konténer, lefut a script
CMD ["python", "rss_sorter.py"]