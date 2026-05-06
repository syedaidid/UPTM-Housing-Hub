FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure media directory and default image exist
RUN mkdir -p /app/media && \
    if [ ! -f /app/media/default.jpg ]; then \
        cp /app/static/default.jpg /app/media/default.jpg 2>/dev/null || \
        python -c "from PIL import Image; img = Image.new('RGB', (300,300), color=(200,200,200)); img.save('/app/media/default.jpg')"; \
    fi

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
