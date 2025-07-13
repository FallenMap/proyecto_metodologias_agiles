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
