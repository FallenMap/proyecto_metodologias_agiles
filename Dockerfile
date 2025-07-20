FROM python:3.11-slim

# Usamos root para instalar dependencias
USER root

# Copiamos e instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos fuente
COPY src/ /app/src
COPY scripts/ /app/scripts
COPY artifacts/ /app/artifacts

ENV MODEL_PATH=/app/artifacts/models/CNN/v2.h5
ENV PYTHONPATH=/app/src

EXPOSE 8000
CMD ["uvicorn", "scripts.deploy.deploy:app", "--host", "0.0.0.0", "--port", "8000"]