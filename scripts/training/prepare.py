import os
from pathlib import Path
import numpy as np
import pandas as pd
from skimage import filters
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from collections import Counter

IMAGE_SIZE = (128, 128)
NUM_PIXELS = IMAGE_SIZE[0] * IMAGE_SIZE[1]
BATCH_SIZE = 500

def reconstruir_imagen(row):
    return row.astype(np.float32).values.reshape(IMAGE_SIZE)

def aplicar_filtros(imagen_2d):
    if imagen_2d.max() > 1.0:
        imagen_2d = imagen_2d / 255.0

    sobel_x = filters.sobel_h(imagen_2d)
    sobel_y = filters.sobel_v(imagen_2d)
    laplacian = filters.laplace(imagen_2d)
    scharr = filters.scharr(imagen_2d)
    gaussian = filters.gaussian(imagen_2d, sigma=1)

    return np.stack([imagen_2d, sobel_x, sobel_y, laplacian, scharr, gaussian], axis=-1)

def procesar_y_guardar_por_lotes(path_parquet, output_dir, split_name):
    print(f"Procesando {split_name} desde {path_parquet}")
    df = pd.read_parquet(path_parquet)
    pixel_cols = [f"pixel_{i}" for i in range(NUM_PIXELS)]

    X_out, y_out = [], []

    for start in range(0, len(df), BATCH_SIZE):
        end = min(start + BATCH_SIZE, len(df))
        batch = df.iloc[start:end]
        X_batch, y_batch = [], []

        for _, row in batch.iterrows():
            img_2d = reconstruir_imagen(row[pixel_cols])
            img_multi = aplicar_filtros(img_2d)
            X_batch.append(img_multi)
            y_batch.append(row["clase_codificada"])

        # Guardar batch
        X_batch = np.array(X_batch, dtype=np.float32)
        y_batch = np.array(y_batch)

        np.save(output_dir / f"X_{split_name}_{start//BATCH_SIZE}.npy", X_batch)
        np.save(output_dir / f"y_{split_name}_{start//BATCH_SIZE}.npy", y_batch)

def augmentar_datos(X_train):
    datagen = ImageDataGenerator(
        rotation_range=30,
        zoom_range=0.2,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        vertical_flip=False
    )
    datagen.fit(X_train)
    return datagen

def cargar_datos_divididos(output_dir, split_name):
    X, y = [], []
    archivos = sorted(output_dir.glob(f"X_{split_name}_*.npy"))
    for archivo in archivos:
        X.append(np.load(archivo))
        y_path = output_dir / archivo.name.replace("X_", "y_")
        y.append(np.load(y_path))
    return np.concatenate(X), np.concatenate(y)

def guardar_datos_por_lotes(X, y, output_dir, split_name):
    for i in range(0, len(X), BATCH_SIZE):
        X_batch = X[i:i+BATCH_SIZE]
        y_batch = y[i:i+BATCH_SIZE]
        np.save(output_dir / f"X_{split_name}_{i//BATCH_SIZE}.npy", X_batch)
        np.save(output_dir / f"y_{split_name}_{i//BATCH_SIZE}.npy", y_batch)

def aumentar_clase_minoria(X, y, output_dir, split_name):
    print(f"Aumentando clase minoritaria para {split_name}...")
    counter = Counter(y)
    clases = list(counter.keys())
    cantidades = list(counter.values())

    clase_min = clases[np.argmin(cantidades)]
    cantidad_objetivo = max(cantidades)

    # Extraer datos de la clase minoritaria
    X_min = X[y == clase_min]
    y_min = y[y == clase_min]

    # Augmentación
    datagen = augmentar_datos(X_min)
    generador = datagen.flow(X_min, y_min, batch_size=32, shuffle=True)

    nuevas_imgs, nuevas_labels = [], []
    total_generados = 0

    while total_generados < (cantidad_objetivo - len(X_min)):
        X_batch, y_batch = next(generador)
        nuevas_imgs.append(X_batch)
        nuevas_labels.append(y_batch)
        total_generados += len(X_batch)

    if total_generados > 0:
        # Limitar si se pasa del objetivo
        nuevas_imgs = np.concatenate(nuevas_imgs)[:cantidad_objetivo - len(X_min)]
        nuevas_labels = np.concatenate(nuevas_labels)[:cantidad_objetivo - len(y_min)]

        # Concatenar con datos originales
        X_balanceado = np.concatenate([X, nuevas_imgs])
        y_balanceado = np.concatenate([y, nuevas_labels])

        # Guardar
        guardar_datos_por_lotes(X_balanceado, y_balanceado, output_dir, split_name)
        print(f"{split_name}: Datos aumentados y guardados.")

def main():
    BASE_ETL_PATH = os.getenv("BASE_ETL_PATH")
    project_root = Path(BASE_ETL_PATH).resolve()
    gold_dir = project_root / "gold"
    output_dir = gold_dir / "processed_gold"
    output_dir.mkdir(parents=True, exist_ok=True)

    for split in ["train", "val", "test"]:
        path_split = gold_dir / split / "data.parquet"
        procesar_y_guardar_por_lotes(path_split, output_dir, split)

    print("Procesamiento completado")

    # Aumentar datos de clase minoritaria
    for split in ["train", "val", "test"]:
        X, y = cargar_datos_divididos(output_dir, split)
        aumentar_clase_minoria(X, y, output_dir, split)

    print("¡Procesamiento y aumento completado!")

if __name__ == "__main__":
    main()
