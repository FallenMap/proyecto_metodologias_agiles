import os
import io
from pathlib import Path
import pandas as pd
import numpy as np
from PIL import Image

# Configuración
IMAGE_SIZE = (128, 128)
NORMALIZAR = True
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

    registros = []

    for clase_folder in ["NORMAL", "PNEUMONIA"]:
        parquet_path = split_path / clase_folder / "data.parquet"
        if not parquet_path.exists():
            print(f"Parquet no encontrado: {parquet_path}")
            continue

        print(f"Procesando clase '{clase_folder}' desde: {parquet_path}")
        df = pd.read_parquet(parquet_path)
        
        for _, row in df.iterrows():
            pixels = preprocess_image(row["content"])
            if pixels is not None:
                registros.append({
                    "imagen_id": row["imagen_id"],
                    "clase": row["clase"],
                    "clase_codificada": row["clase_codificada"],
                    "split": row["split"],
                    **{f"pixel_{i}": pixels[i] for i in range(NUM_PIXELS)}
                })

    if not registros:
        print(f"No se procesaron imágenes válidas para el split: {split_path.name}")
        return

    processed_df = pd.DataFrame(registros)

    split_output_dir = output_dir / split_path.name
    split_output_dir.mkdir(parents=True, exist_ok=True)
    output_file = split_output_dir / "data.parquet"

    processed_df.to_parquet(output_file, index=False)
    print(f"Guardado GOLD parquet para split '{split_path.name}' en: {output_file}")

def main():
    BASE_ETL_PATH = os.getenv("BASE_ETL_PATH")
    project_root = Path(BASE_ETL_PATH).resolve()
    silver_base = project_root / "silver"
    gold_base   = project_root / "gold"
    gold_base.mkdir(parents=True, exist_ok=True)

    for split in ["train", "val", "test"]:
        split_path = silver_base / split
        process_split(split_path, gold_base)

if __name__ == "__main__":
    main()
