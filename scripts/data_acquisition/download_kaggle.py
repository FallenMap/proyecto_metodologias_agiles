import kagglehub
import os

def main():
    kaggle_dataset = "paultimothymooney/chest-xray-pneumonia"
    
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    project_root = os.path.abspath(os.path.join(current_dir, "..", "..")) 
    raw_path = os.path.join(project_root, "src", "Pneumonia_Detection", "database", "bronze", "raw")

    #  /app/src/download_kaggle.py  →  /app  (raíz del proyecto)
    project_root = pathlib.Path(__file__).resolve().parent.parent

    #   /app/database/bronze
    raw_path = project_root / "database" / "bronze" 

    # ¿Ya existe el dataset?
    if all((raw_path / split).exists() for split in ["train", "val", "test"]):
        print(f"Dataset ya presente en: {raw_path}")
        return

    print("Descargando dataset desde Kaggle…")
    downloaded_path = pathlib.Path(kagglehub.dataset_download(kaggle_dataset))

    # Dentro del zip: …/versions/<n>/chest_xray
    extracted = next(downloaded_path.glob("**/chest_xray"))
    print(f"Creando carpeta destino: {raw_path}")
    raw_path.mkdir(parents=True, exist_ok=True)

    print(f"Copiando datos a {raw_path}")
    shutil.copytree(extracted, raw_path, dirs_exist_ok=True)
    print("✅ Copia completa")

if __name__ == "__main__":
    main()
