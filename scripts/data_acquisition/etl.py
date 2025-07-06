import os
from pathlib import Path
import pandas as pd
import re

def get_image_paths(directory):
    return [
        os.path.join(root, f)
        for root, _, files in os.walk(directory)
        for f in files if f.lower().endswith(".jpeg")
    ]

def extract_metadata(image_path):
    filename = os.path.basename(image_path)
    match_clase = re.search(r"(NORMAL|PNEUMONIA)", image_path)
    imagen_id = filename.replace(".jpeg", "")
    clase = match_clase.group(1) if match_clase else None
    clase_codificada = 0 if clase == "NORMAL" else 1 if clase == "PNEUMONIA" else None
    return imagen_id, image_path, clase, clase_codificada

def process_split(base_path, split, output_base):
    input_dir = base_path / split
    output_dir = output_base / split

    if not input_dir.exists():
        print(f"Carpeta inexistente: {input_dir}")
        return

    all_images = get_image_paths(input_dir)
    if not all_images:
        print(f"No se encontraron imágenes en: {input_dir}")
        return

    print(f"\nProcesando split: {split} con {len(all_images)} imágenes")

    data = []
    for path in all_images:
        imagen_id, ruta_origen, clase, clase_codificada = extract_metadata(path)
        try:
            with open(path, "rb") as f:
                content = f.read()
            data.append({
                "imagen_id": imagen_id,
                "ruta_origen": ruta_origen,
                "clase": clase,
                "clase_codificada": clase_codificada,
                "split": split,
                "content": content
            })
        except Exception as e:
            print(f"Error leyendo {path}: {e}")

    df = pd.DataFrame(data)

    for clase in ["NORMAL", "PNEUMONIA"]:
        clase_df = df[df["clase"] == clase]
        clase_output = output_dir / clase
        clase_output.mkdir(parents=True, exist_ok=True)
        output_file = clase_output / "data.parquet"
        clase_df.to_parquet(output_file, index=False)
        print(f"Guardado parquet de clase '{clase}' en: {output_file}")

def main():
    BASE_ETL_PATH = os.getenv("BASE_ETL_PATH")
    project_root = Path(BASE_ETL_PATH).resolve()
    base_path = project_root / "bronze"
    output_base = project_root / "silver"
    output_base.mkdir(parents=True, exist_ok=True)

    for split in ["train", "val", "test"]:
        process_split(base_path, split, output_base)

if __name__ == "__main__":
    main()
