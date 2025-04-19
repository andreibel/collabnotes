# user_service/Dockerfile
FROM python:3.11-slim

# Set environment variables to ensure Python writes straight to stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . /app

# By default, run uvicorn on 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]