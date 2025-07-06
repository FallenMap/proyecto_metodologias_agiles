import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import seaborn as sns
import os

NON_PIXEL_COLUMNS = ["imagen_id", "clase", "clase_codificada", "split"]

class Visualizer:
    def __init__(self, dwh_path, outputs_path, split='train'):
        self.dwh_path = Path(dwh_path)
        self.outputs_path = Path(outputs_path)
        self.outputs_path.mkdir(parents=True, exist_ok=True)
        self.split = split
        self.df = None
    
    def load_data(self):
        self.df = pd.read_parquet(self.dwh_path / "gold" / self.split / "data.parquet")

    def generate_sample_images_report(self, max_images=10):
        if self.df is None:
            raise ValueError("Los datos aùn no han sido cargados. Invoque load_data()")

        df_sample = self.df.sample(n=min(max_images, len(self.df)))
        pixel_columns = [
            col for col in self.df.columns 
                if col not in NON_PIXEL_COLUMNS
        ]
        img_size = int(np.sqrt(len(pixel_columns)))

        fig, axes = plt.subplots(len(df_sample), 2, figsize=(6, len(df_sample) * 2))

        for i, (_, row) in enumerate(df_sample.iterrows()):
            image = row[pixel_columns].values.reshape((img_size, img_size)).astype(np.float32)
            label = row["clase"]

            axes[i, 0].imshow(image, cmap='gray')
            axes[i, 0].axis('off')

            axes[i, 1].text(0.5, 0.5, str(label), fontsize=14, ha='center', va='center')
            axes[i, 1].axis('off')

        plt.tight_layout()
        out_path = self.outputs_path / f"{self.split}_sample_images.png"
        plt.savefig(out_path)
        plt.close()
        print(f"Sample images report saved to: {out_path}")

    def plot_pixel_distribution(self):
        if self.df is None:
            raise ValueError("Datos no cargados. Invoque load_data()")
        
        pixel_columns = [col for col in self.df.columns if col not in NON_PIXEL_COLUMNS]
        pixel_values = self.df[pixel_columns].values.flatten()

        plt.figure(figsize=(8, 4))
        sns.histplot(pixel_values, bins=20, color='gray')
        plt.title("Distribución de valores de pixel")
        plt.xlabel("Valor de pixel")
        plt.ylabel("Cantidad")

        out_path = self.outputs_path / f"{self.split}_pixel_distribution.png"
        plt.savefig(out_path)
        plt.close()
        print(f"Pixel value distribution plot saved to: {out_path}")

    def plot_label_distribution(self):
        if self.df is None:
            raise ValueError("Datos no cargados. Invoque load_data()")

        plt.figure(figsize=(6, 4))
        sns.countplot(x="clase", data=self.df, palette="pastel")
        plt.title("Distribución de etiquetas")
        plt.xlabel("Clase")
        plt.ylabel("Cantidad")

        out_path = self.outputs_path / f"{self.split}_label_distribution.png"
        plt.savefig(out_path)
        plt.close()
        print(f"Label distribution plot saved to: {out_path}")



def main():

    BASE_ETL_PATH = os.getenv("BASE_ETL_PATH")
    OUTPUTS_PATH = os.getenv("OUTPUTS_PATH")

    project_root = Path(BASE_ETL_PATH).resolve()
    output_root = Path(OUTPUTS_PATH).resolve()

    visualizer = Visualizer(
        project_root, output_root
    )

    visualizer.load_data()
    visualizer.generate_sample_images_report()
    visualizer.plot_pixel_distribution()
    visualizer.plot_label_distribution()

if __name__ == "__main__":
    main()