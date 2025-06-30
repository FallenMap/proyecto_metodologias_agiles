from pyspark.sql import SparkSession
import os
import shutil

def main():
    # Crear la sesión de Spark
    spark = SparkSession.builder \
        .appName("TestWrite") \
        .config("spark.hadoop.io.native.lib.available", "false") \
        .config("spark.driver.extraJavaOptions", "-Dos.name=Windows 10") \
        .getOrCreate()

    # Datos de ejemplo
    data = [
        ("img_001", "NORMAL", 0),
        ("img_002", "PNEUMONIA", 1),
        ("img_003", "NORMAL", 0)
    ]
    columnas = ["imagen_id", "clase", "clase_codificada"]
    df = spark.createDataFrame(data, columnas)

    # Mostra datos
    print(" Mostrando datos:")
    df.show()

    # Rutas de salida seguras
    output_path_parquet = "C:/temp_spark_test/parquet"
    output_path_csv = "C:/temp_spark_test/csv"

    # Eliminar rutas si existen
    if os.path.exists(output_path_parquet):
        shutil.rmtree(output_path_parquet)
    if os.path.exists(output_path_csv):
        shutil.rmtree(output_path_csv)

    # Guardar como Parquet
    try:
        df.write.mode("overwrite").parquet(output_path_parquet)
        print(f"Parquet guardado en: {output_path_parquet}")
    except Exception as e:
        print("Error al guardar Parquet:", e)

    # Guardar como CSV
    try:
        df.write.mode("overwrite").option("header", True).csv(output_path_csv)
        print(f" CSV guardado en: {output_path_csv}")
    except Exception as e:
        print("Error al guardar CSV:", e)

    spark.stop()

if __name__ == "__main__":
    main()
