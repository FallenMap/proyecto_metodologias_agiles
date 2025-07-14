import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import json

sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from Pneumonia_Detection.models.cnn_model import \
        PneumoniaCNN
from Pneumonia_Detection.models.utils import load_prepared_data

def train_cnn_model(
        output_dir: str, version : str,
    ):
    """
    Entrenar modelo CNN:
        Red convolucional para clasificación de imágenes
    """

    print("Creando modelo CNN")
    model = PneumoniaCNN(
        version,
    )

    (X_train, X_val, X_test), (y_train, y_val, y_test) = load_prepared_data()

    (X_train, X_val, X_test), (y_train, y_val, y_test) = model.prepare_data((X_train, X_val, X_test), (y_train, y_val, y_test))

    print("Entrenando modelo CNN")
    tmp_path = Path(output_dir) / Path("tmp") / Path("train.keras")

    model.build_model()

    model.train(
        X_train, y_train, X_test, y_test, epochs = 10, batch_size = 32,
        model_save_path = tmp_path
    )

    print("Evaluando modelo CNN")
    _, test_accuracy, _ = model.evaluate(X_test, y_test)

    model_path = Path(output_dir) / Path("models")
    saved_path = model.save_model(model_path)

    results_path = Path(output_dir) / Path("results")
    saved_results_path = model.save_results(results_path)

    print(f"Modelo guardado a: {saved_path}")
    print(f"Resultados guardados en: {saved_results_path}")
    print(f"Precisión test: {test_accuracy:.4f}")

    return model, model.output_results


def main():
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "../database/Silver/train/data.parquet")
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    print("Entrenando modelo de linea base")

    model, results = train_cnn_model(
        output_dir=OUTPUT_DIR, version='v1',
    )

    print("Entrenamiento finalizado")


if __name__ == "__main__":
    main()