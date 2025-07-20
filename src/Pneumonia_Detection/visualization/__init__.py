import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import seaborn as sns
import os
from sklearn.decomposition import PCA

NON_PIXEL_COLUMNS = ["imagen_id", "clase", "clase_codificada", "split"]

class Visualizer:
    def __init__(self, dwh_path, outputs_path, split='train'):
        self.dwh_path = Path(dwh_path)
        self.outputs_path = Path(outputs_path)
        self.outputs_path.mkdir(parents=True, exist_ok=True)
        self.split = split
        self.df = None

    def load_data(self, max_rows=5000):
        data_path = self.dwh_path / "gold" / self.split / "data.parquet"
        print(f"Cargando datos desde: {data_path}")
        df = pd.read_parquet(data_path)

        if len(df) > max_rows:
            print(f"Reduciendo de {len(df)} a {max_rows} filas (batching)")
            df = df.sample(n=max_rows, random_state=42).reset_index(drop=True)

        self.df = df

    def generate_sample_images_report(self, max_images=10):
        if self.df is None:
            raise ValueError("Los datos aún no han sido cargados. Invoque load_data()")

        df_sample = self.df.sample(n=min(max_images, len(self.df)))
        pixel_columns = [col for col in self.df.columns if col not in NON_PIXEL_COLUMNS]
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
        sns.countplot(data=self.df, x="clase", hue="clase", palette="pastel", legend=False)
        plt.title("Distribución de etiquetas")
        plt.xlabel("Clase")
        plt.ylabel("Cantidad")

        out_path = self.outputs_path / f"{self.split}_label_distribution.png"
        plt.savefig(out_path)
        plt.close()
        print(f"Label distribution plot saved to: {out_path}")

    def plot_pca_projection(self, n_components=2, batch_size=3000):
        if self.df is None:
            raise ValueError("Datos no cargados. Invoque load_data()")

        pixel_columns = [col for col in self.df.columns if col not in NON_PIXEL_COLUMNS]
        X = self.df[pixel_columns].values
        y = self.df["clase"].values

        if X.shape[0] > batch_size:
            print(f"Reduciendo datos para PCA: de {X.shape[0]} a {batch_size} imágenes")
            idx = np.random.choice(X.shape[0], batch_size, replace=False)
            X = X[idx]
            y = y[idx]

        pca = PCA(n_components=n_components)
        X_pca = pca.fit_transform(X)

        df_pca = pd.DataFrame(X_pca, columns=[f"PC{i+1}" for i in range(n_components)])
        df_pca["clase"] = y

        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df_pca, x="PC1", y="PC2", hue="clase", palette="Set2", alpha=0.6)
        plt.title("Proyección PCA de imágenes")
        plt.xlabel("Componente Principal 1")
        plt.ylabel("Componente Principal 2")
        plt.legend(title="Clase")

        out_path = self.outputs_path / f"{self.split}_pca_projection.png"
        plt.savefig(out_path)
        plt.close()
        print(f"PCA projection plot saved to: {out_path}")

    def plot_training_(self, n_components=2, batch_size=3000):
        if self.df is None:
            raise ValueError("Datos no cargados. Invoque load_data()")

        pixel_columns = [col for col in self.df.columns if col not in NON_PIXEL_COLUMNS]
        X = self.df[pixel_columns].values
        y = self.df["clase"].values

        if X.shape[0] > batch_size:
            print(f"Reduciendo datos para PCA: de {X.shape[0]} a {batch_size} imágenes")
            idx = np.random.choice(X.shape[0], batch_size, replace=False)
            X = X[idx]
            y = y[idx]

        pca = PCA(n_components=n_components)
        X_pca = pca.fit_transform(X)

        df_pca = pd.DataFrame(X_pca, columns=[f"PC{i+1}" for i in range(n_components)])
        df_pca["clase"] = y

        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df_pca, x="PC1", y="PC2", hue="clase", palette="Set2", alpha=0.6)
        plt.title("Proyección PCA de imágenes")
        plt.xlabel("Componente Principal 1")
        plt.ylabel("Componente Principal 2")
        plt.legend(title="Clase")

        out_path = self.outputs_path / f"{self.split}_pca_projection.png"
        plt.savefig(out_path)
        plt.close()
        print(f"PCA projection plot saved to: {out_path}")