from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np
from pathlib import Path

class BaseModel(ABC):
    def __init__(
            self,
            name, version
        ):
        self.name = name
        self.version = version

    def prepare_data(
        self, X : Tuple[np.array], y : Tuple[np.array]
    ) -> Tuple[Tuple[np.array], Tuple[np.array]]:
        """
        Pasos de preparación específicos del modelo
        """
        return X, y

    @abstractmethod
    def build_model(self):
        pass

    @abstractmethod
    def save_model(
        self, model_path: Path
    ):
        pass

    @abstractmethod
    def load_model(
        self, model_path: Path
    ):
        pass

    @abstractmethod
    def generate_path(self, model_path: Path):
        pass

    @abstractmethod
    def save_results(self, result_path: Path):
        pass

    @abstractmethod
    def load_results(self, result_path: Path):
        pass

    def get_name(self) -> str:
        return self.name