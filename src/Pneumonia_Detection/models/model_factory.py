from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

from Pneumonia_Detection.models.cnn_model import PneumoniaCNN
from Pneumonia_Detection.models.baseline_model import PneumoniaRandomForest
class ModelFactory:
    """
    Clase fábrica de modelos CNN / Random Forest Baseline
    """

    @staticmethod
    def create_model(model_type: str, **kwargs):
        if model_type.lower() == 'tensorflow':
            return PneumoniaCNN(**kwargs)
        elif model_type.lower() == 'baseline':
            return PneumoniaRandomForest(**kwargs)
        else:
            raise ValueError(f"Unknown model type: {model_type}")