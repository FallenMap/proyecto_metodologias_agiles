import numpy as np
import os
from pathlib import Path
import glob

def load_prepared_data():
    """
    Cargar información de datos preprocesados

    Retorna:
        tuple: (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    base_path = Path(__file__).parent.parent / "database" / "gold" / "processed_gold"

    X_train_list = []
    y_train_list = []
    X_val_list = []
    y_val_list = []
    X_test_list = []
    y_test_list = []

    train_x_files = sorted(glob.glob(str(base_path / "X_train_*.npy")))
    train_y_files = sorted(glob.glob(str(base_path / "y_train_*.npy")))

    for x_file, y_file in zip(train_x_files, train_y_files):
        if os.path.exists(x_file) and os.path.exists(y_file):
            X_train_list.append(np.load(x_file))
            y_train_list.append(np.load(y_file))

    val_x_files = sorted(glob.glob(str(base_path / "X_val_*.npy")))
    val_y_files = sorted(glob.glob(str(base_path / "y_val_*.npy")))

    for x_file, y_file in zip(val_x_files, val_y_files):
        if os.path.exists(x_file) and os.path.exists(y_file):
            X_val_list.append(np.load(x_file))
            y_val_list.append(np.load(y_file))

    test_x_files = sorted(glob.glob(str(base_path / "X_test_*.npy")))
    test_y_files = sorted(glob.glob(str(base_path / "y_test_*.npy")))

    for x_file, y_file in zip(test_x_files, test_y_files):
        if os.path.exists(x_file) and os.path.exists(y_file):
            X_test_list.append(np.load(x_file))
            y_test_list.append(np.load(y_file))

    X_train = np.concatenate(X_train_list, axis=0) if X_train_list else np.array([])
    y_train = np.concatenate(y_train_list, axis=0) if y_train_list else np.array([])
    X_val = np.concatenate(X_val_list, axis=0) if X_val_list else np.array([])
    y_val = np.concatenate(y_val_list, axis=0) if y_val_list else np.array([])
    X_test = np.concatenate(X_test_list, axis=0) if X_test_list else np.array([])
    y_test = np.concatenate(y_test_list, axis=0) if y_test_list else np.array([])

    print(f"\nDatos cargados:")
    print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"X_val: {X_val.shape}, y_val: {y_val.shape}")
    print(f"X_test: {X_test.shape}, y_test: {y_test.shape}")

    return (X_train, X_val, X_test), (y_train, y_val, y_test)
