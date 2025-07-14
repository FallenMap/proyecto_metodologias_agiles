import os
import io
from pathlib import Path
import pandas as pd
import numpy as np
from PIL import Image
import pyarrow as pa
import pyarrow.parquet as pq

# Configuración
IMAGE_SIZE = (128, 128)
NORMALIZAR = False
NUM_PIXELS = IMAGE_SIZE[0] * IMAGE_SIZE[1]

def preprocess_image(content_bytes):
    try:
        image = Image.open(io.BytesIO(content_bytes)).convert("L")
        image = image.resize(IMAGE_SIZE)

        image_array = np.asarray(image, dtype=np.float32) / 255.0

        if NORMALIZAR:
            mean = image_array.mean()
            std = image_array.std()
            if std > 0:
                image_array = (image_array - mean) / std

        return image_array.reshape(-1)
    except Exception as e:
        print(f"Error procesando imagen: {e}")
        return None

def process_split(split_path: Path, output_dir: Path):
    print(f"\nProcesando split desde {split_path}")

    split_output_dir = output_dir / split_path.name
    split_output_dir.mkdir(parents=True, exist_ok=True)
    output_file = split_output_dir / "data.parquet"

    table_batches = []

    for clase_folder in ["NORMAL", "PNEUMONIA"]:
        parquet_path = split_path / clase_folder / "data.parquet"
        if not parquet_path.exists():
            print(f"Parquet no encontrado: {parquet_path}")
            continue

        print(f"Procesando clase '{clase_folder}' desde: {parquet_path}")
        df = pd.read_parquet(parquet_path)

        batch = []

        for idx, row in df.iterrows():
            pixels = preprocess_image(row["content"])
            if pixels is not None:
                batch.append({
                    "imagen_id": row["imagen_id"],
                    "clase": row["clase"],
                    "clase_codificada": row["clase_codificada"],
                    "split": row["split"],
                    **{f"pixel_{i}": pixels[i] for i in range(NUM_PIXELS)}
                })

            # Escribir en bloques cada 500 imágenes
            if len(batch) >= 500:
                df_batch = pd.DataFrame(batch)
                table = pa.Table.from_pandas(df_batch)
                table_batches.append(table)
                batch = []

        if batch:
            df_batch = pd.DataFrame(batch)
            table = pa.Table.from_pandas(df_batch)
            table_batches.append(table)

    # Escribimos todos los datos juntos (fuera del loop de clases)
    if table_batches:
        pq.write_table(pa.concat_tables(table_batches), output_file)
        print(f"Guardado GOLD parquet para split '{split_path.name}' en: {output_file}")
    else:
        print(f"No se procesaron imágenes válidas para el split: {split_path.name}")