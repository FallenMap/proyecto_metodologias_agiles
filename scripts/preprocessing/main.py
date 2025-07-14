import os
import io
from pathlib import Path
import pandas as pd
import numpy as np
from PIL import Image
import pyarrow as pa
import pyarrow.parquet as pq
import sys

# Agregar al path el directorio src para importar los módulos personalizados
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from Pneumonia_Detection.preprocessing import process_split

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