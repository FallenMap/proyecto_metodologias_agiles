import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import json

sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from Pneumonia_Detection.models.baseline_model import \
        PneumoniaRandomForest, PneumoniaRandomForestHyperparameters
from Pneumonia_Detection.models.utils import load_prepared_data

def train_baseline_model(
        output_dir: str, version : str,
        n_estimators: int = 100, max_depth: int = None,
        optimize_hyperparams: PneumoniaRandomForestHyperparameters = None
    ):
    """
    Entrenar modelo baseline:
        Random Forest para clasificación de imágenes
    """

    print("Creando modelo baseline")
    model = PneumoniaRandomForest(
        version,
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=None,
        hyperparameters=optimize_hyperparams
    )

    (X_train, X_val, X_test), (y_train, y_val, y_test) = load_prepared_data()

    (X_train, X_val, X_test), (y_train, y_val, y_test) = model.prepare_data((X_train, X_val, X_test), (y_train, y_val, y_test))

    model.build_model()

    print("Entrenando modelo baseline")
    model.train(
        X_train, y_train
    )

    print("Evaluando modelo baseline")
    results = model.evaluate(X_val, y_val)

    model.get_feature_importance()

    model_path = Path(output_dir) / Path("models")
    saved_path = model.save_model(model_path)

    results_path = Path(output_dir) / Path("results")
    saved_results_path = model.save_results(results_path)

    print(f"Modelo guardado a: {saved_path}")
    print(f"Resultados guardados en: {saved_results_path}")
    print(f"Precisión test: {results['accuracy']:.4f}")

    return model, model.output_results


def main():
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "../database/Silver/train/data.parquet")
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    print("Entrenando modelo de linea base")

    model, results = train_baseline_model(
        output_dir=OUTPUT_DIR, version='v2',
    )

    print("Entrenamiento finalizado")


if __name__ == "__main__":
    main()