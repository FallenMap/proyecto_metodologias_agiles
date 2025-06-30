# ---------- Dockerfile ----------
FROM apache/spark:4.0.0-scala2.13-java17-python3-ubuntu

USER root
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir -p /home/spark && chown 185:185 /home/spark

USER 185
ENV HOME=/home/spark \
    PATH="/opt/spark/bin:${PATH}" \
    PYSPARK_PYTHON=python3

WORKDIR /app
COPY src/ /app/src

ENTRYPOINT ["spark-submit", "--master", "local[*]", "/app/src/spark_etl_2.py"]
