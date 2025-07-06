FROM python:3.11-slim

# Usamos root para instalar dependencias
USER root

# Copiamos e instalamos dependencias
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Creamos un directorio para el usuario no root 
RUN mkdir -p /home/app && useradd -u 185 -d /home/app -m appuser && chown -R appuser:appuser /home/app

# Usamos un usuario no root
USER 185
ENV HOME=/home/app

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos fuente
COPY src/ /app/src
COPY scripts/ /app/scripts

# Comando de entrada
ENTRYPOINT ["python3", "/app/src/etl_2.py"]
