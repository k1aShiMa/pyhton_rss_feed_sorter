FROM python:3.11-slim

WORKDIR /app

#Copy and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the file
COPY rss_sorter.py .

# When the container is running it's just launches the script xd
CMD ["python", "rss_sorter.py"]
