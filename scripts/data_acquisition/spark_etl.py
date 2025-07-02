from pyspark.sql import SparkSession
from pyspark.sql.functions import input_file_name, regexp_extract, lit, col, when
from pathlib import Path
import os

to_file_url = lambda p: "file:///" + str(p).replace("\\", "/")

def get_image_paths(directory):
    return [
        os.path.join(root, f)
        for root, _, files in os.walk(directory)
        for f in files if f.lower().endswith(".jpeg")
    ]

def process_split(spark, base_path, split, output_base):
    input_dir  = base_path / split
    output_dir = output_base / f"split={split}"

    if not input_dir.exists():
        print(f"Carpeta inexistente: {input_dir}")
        return

    all_images = get_image_paths(input_dir)
    if not all_images:
        print(f"No se encontraron imágenes en: {input_dir}")
        return

    print(f"\nProcesando split: {split} con {len(all_images)} imágenes")

    df = spark.read.format("binaryFile").load([to_file_url(p) for p in all_images])

    df = (df.withColumn("ruta_origen", input_file_name())
            .withColumn("imagen_id", regexp_extract("ruta_origen", r"([^/\\]+)\.jpeg$", 1))
            .withColumn("clase",      regexp_extract("ruta_origen", r"(NORMAL|PNEUMONIA)", 1))
            .withColumn("clase_codificada",
                        when(col("clase") == "NORMAL", 0)
                       .when(col("clase") == "PNEUMONIA", 1))
            .withColumn("split", lit(split))
            .select("imagen_id", "ruta_origen", "clase", "clase_codificada", "split"))
    

    for clase in ["NORMAL", "PNEUMONIA"]:
        clase_df = df.filter(col("clase") == clase)
        clase_output = output_dir / clase
        clase_df.write.mode("overwrite").parquet(to_file_url(clase_output))
        print(f"Gaurdado parquet de clase '{clase}' en: {clase_output}")

#Rutas automatizadas
def main():
    project_root = Path(__file__).resolve().parent.parent.parent
    base_path   = project_root / "src" / "Pneumonia_Detection" / "database" / "bronze" / "raw"
    output_base = project_root / "src" / "Pneumonia_Detection" / "database" / "silver" 
    output_base.mkdir(parents=True, exist_ok=True)

    spark = (SparkSession.builder
                .appName("PneumoniaETL")
                .config("spark.hadoop.io.native.lib.available", "false")
                .config("spark.hadoop.native.lib", "false")
                .config("spark.hadoop.fs.file.impl.disable.cache", "true")
                .getOrCreate())

    for split in ["train", "val", "test"]:
        process_split(spark, base_path, split, output_base)

    spark.stop()

if __name__ == "__main__":
    main()
