from typing import Tuple
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
from pathlib import Path
import joblib
import json

from Pneumonia_Detection.models.base_model import BaseModel

class PneumoniaRandomForestHyperparameters:
    def __init__(
            self,
            n_estimators = [100],
            max_depth = [10, 20],
            min_samples_split = [2, 5],
            min_samples_leaf = [1, 2]
        ):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf

class PneumoniaRandomForest(BaseModel):
    def __init__(
            self,
            version,
            n_estimators=100,
            max_depth=None, random_state=42,
            hyperparameters : PneumoniaRandomForestHyperparameters = None
        ):
        super(PneumoniaRandomForest, self).__init__("Random Forest baseline", version)
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.model = None
        self.feature_importance = None
        self.hyperparameters = hyperparameters
        self.original_shape = None

    def build_model(self):
        self.model = RandomForestClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            random_state=self.random_state,
            n_jobs=-1
        )

    def prepare_data(
        self, X : Tuple[np.array], y : Tuple[np.array]
    ) -> Tuple[Tuple[np.array], Tuple[np.array]]:
        X_flat = []
        y_flat = []

        for X_data, y_data in zip(X, y):
            if len(X_data.shape) == 4:
                n_samples = X_data.shape[0]
                X_flat_data = X_data.reshape(n_samples, -1)
                X_flat.append(X_flat_data)
                y_flat.append(y_data)
            else:
                X_flat.append(X_data)
                y_flat.append(y_data)

        return tuple(X_flat), tuple(y_flat)

    def train(
            self,
            X : np.array, y : np.array,
        ):

        if self.hyperparameters is not None:
            param_grid = {
                'n_estimators': self.hyperparameters.n_estimators,
                'max_depth': self.hyperparameters.max_depth,
                'min_samples_split': self.hyperparameters.min_samples_split,
                'min_samples_leaf': self.hyperparameters.min_samples_leaf
            }

            grid_search = GridSearchCV(
                RandomForestClassifier(
                    random_state=self.random_state
                ),
                param_grid,
                cv=2,
                scoring='accuracy',
                n_jobs=-1,
                verbose=1
            )

            grid_search.fit(X, y)
            self.model = grid_search.best_estimator_
            print(f"Best parameters: {grid_search.best_params_}")
        else:
            self.model.fit(X, y)

        self.feature_importance = self.model.feature_importances_

        return self.model

    def predict(self, X):
        if len(X.shape) == 4:
            n_samples = X.shape[0]
            X = X.reshape(n_samples, -1)
        return self.model.predict(X)

    def predict_proba(self, X):
        if len(X.shape) == 4:
            n_samples = X.shape[0]
            X = X.reshape(n_samples, -1)
        return self.model.predict_proba(X)

    def evaluate(self, X, y):
        if len(X.shape) == 4:
            n_samples = X.shape[0]
            X = X.reshape(n_samples, -1)

        y_pred = self.predict(X)

        self.results = {
            'accuracy': accuracy_score(y, y_pred),
            'classification_report': classification_report(y, y_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(y, y_pred).tolist()
        }

        return self.results

    def get_feature_importance(self, feature_names=None):
        if feature_names is None:
            feature_names = [f'pixel_{i}' for i in range(len(self.feature_importance))]

        self.importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': self.feature_importance
        }).sort_values('importance', ascending=False)

        return self.importance_df

    def generate_path(self, model_path: Path):
        return model_path / Path(self.name)

    def save_model(self, model_path : Path):
        final_path = self.generate_path(model_path) / Path(f"{self.version}.pkl")
        Path(final_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, final_path)
        return final_path

    def load_model(self, model_path):
        final_path = self.generate_path(model_path) / Path(f"{self.version}.pkl")
        self.model = joblib.load(final_path)
        return self.model

    def save_results(self, result_path: Path):
        final_path = self.generate_path(result_path) / Path(f"{self.version}.json")
        Path(final_path).parent.mkdir(parents=True, exist_ok=True)
        self.output_results = {
            'test_accuracy': self.results['accuracy'],
            'classification_report': self.results['classification_report'],
            'confusion_matrix': self.results['confusion_matrix'],
            'feature_importance_top_10': self.importance_df.head(10).to_dict('records'),
            'model_params': {
                'n_estimators': self.n_estimators,
                'max_depth': self.max_depth,
                'random_state': self.random_state
            }
        }

        with open(final_path, 'w') as f:
            json.dump(self.output_results, f, indent=2)

        return final_path

    def load_results(self, result_path: Path):
        final_path = self.generate_path(result_path) / Path(f"{self.version}.json")
        with open(final_path, 'r') as f:
            self.output_results = json.load(f)

        return self.output_results