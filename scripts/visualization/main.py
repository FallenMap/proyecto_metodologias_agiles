import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import seaborn as sns
import os
from sklearn.decomposition import PCA
import sys

# Agregar al path el directorio src para importar los módulos personalizados
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from Pneumonia_Detection.visualization import Visualizer

def main():
    BASE_ETL_PATH = os.getenv("BASE_ETL_PATH", "../database/Silver")
    OUTPUTS_PATH = os.getenv("OUTPUTS_PATH", "../visualization")
    MAX_ROWS = int(os.getenv("MAX_ROWS"))
    project_root = Path(BASE_ETL_PATH).resolve()
    output_root = Path(OUTPUTS_PATH).resolve()

    visualizer = Visualizer(project_root, output_root)

    # Cambia max_rows según capacidad
    visualizer.load_data(max_rows=MAX_ROWS)

    visualizer.generate_sample_images_report()
    visualizer.plot_pixel_distribution()
    visualizer.plot_label_distribution()
    visualizer.plot_pca_projection(batch_size=MAX_ROWS)

if __name__ == "__main__":
    main()