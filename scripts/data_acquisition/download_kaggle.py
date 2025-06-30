import kagglehub
import os

def main():
    kaggle_dataset = "paultimothymooney/chest-xray-pneumonia"
    
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    project_root = os.path.abspath(os.path.join(current_dir, "..", "..")) 
    raw_path = os.path.join(project_root, "src", "Pneumonia_Detection", "database", "bronze", "raw")

    if all(os.path.exists(os.path.join(raw_path, split)) for split in ["train", "val", "test"]):
        print(f"Dataset ya está presente en: {raw_path}. No se realizará descarga.")
        return

    print("Descargando dataset desde Kaggle...")
    downloaded_path = kagglehub.dataset_download(kaggle_dataset)
    print(f"Dataset descagrado en: {downloaded_path}")

if __name__ == "__main__":
    main()
