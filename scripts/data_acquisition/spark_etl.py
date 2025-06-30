from pyspark.sql import SparkSession
from pyspark.sql.functions import input_file_name, regexp_extract, lit, col, when
import os

def to_file_url(path):
    return "file:///" + path.replace("\\", "/")

def get_image_paths(directory):
    paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".jpeg"):
                paths.append(os.path.join(root, file))
    return paths

def process_split(spark, base_path, split, output_base):
    input_dir = os.path.join(base_path, split)
    output_dir = os.path.join(output_base, split)

    if not os.path.exists(input_dir):
        print(f"Carpeta inexistente: {input_dir}")
        return

    all_images = get_image_paths(input_dir)
    if not all_images:
        print(f"No se encontraron imágenes en: {input_dir}")
        return

    print(f"\nProcesando split: {split} con {len(all_images)} imágenes")

    df = spark.read.format("binaryFile").load([to_file_url(p) for p in all_images])

    df = df.withColumn("ruta_origen", input_file_name()) \
           .withColumn("imagen_id", regexp_extract("ruta_origen", r"([^/\\]+)\.jpeg$", 1)) \
           .withColumn("clase", regexp_extract("ruta_origen", r"(NORMAL|PNEUMONIA)", 1)) \
           .withColumn("clase_codificada", when(col("clase") == "NORMAL", 0)
                                       .when(col("clase") == "PNEUMONIA", 1)
                                       .otherwise(None)) \
           .withColumn("split", lit(split)) \
           .select("imagen_id", "ruta_origen", "clase", "clase_codificada", "split")

    df.write.mode("overwrite").option("header", True).csv(to_file_url(output_dir))  # CSV directo

    print(f"✅ Guardado CSV en: {output_dir}")
