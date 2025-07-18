from Pneumonia_Detection.models.base_model import BaseModel
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import numpy as np
from pathlib import Path
import json
import joblib

class PneumoniaCNN(BaseModel):
    def __init__(self, version, input_shape=(128, 128, 6), num_classes=2):
        super(PneumoniaCNN, self).__init__("CNN", version)
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = None
        self.history = None
        self.test_loss = None
        self.test_accuracy = None
        self.test_crossentropy = None

    def build_model(self):
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation='softmax')
        ])

        model.summary()

        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy', 'sparse_categorical_crossentropy']
        )

        self.model = model
        return model

    def train(self, X_train, y_train, X_val, y_val,
              epochs=50, batch_size=32, model_save_path=None):

        callbacks = [
            EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True),
            ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7),
        ]

        if model_save_path:
            callbacks.append(
                ModelCheckpoint(
                    model_save_path,
                    monitor='val_accuracy',
                    save_best_only=True,
                    save_weights_only=False
                )
            )

        self.history = self.model.fit(
            X_train, y_train,
            # validation_split=0.2,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )

        return self.history

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        test_loss, test_accuracy, test_crossentropy = self.model.evaluate(X_test, y_test, verbose=0)
        self.test_loss = test_loss
        self.test_accuracy = test_accuracy
        self.test_crossentropy = test_crossentropy
        return test_loss, test_accuracy, test_crossentropy

    def generate_path(self, model_path: Path):
        return model_path / Path(self.name)

    def save_model(self, model_path):
        final_path = self.generate_path(model_path) / Path(f"{self.version}.h5")
        Path(final_path).parent.mkdir(parents=True, exist_ok=True)
        self.model.save(final_path)

        history_path = str(final_path).replace('.h5', '_history.json')
        with open(history_path, 'w') as f:
            json.dump(self.history.history, f)

        return final_path

    def load_model(self, model_path):
        final_path = self.generate_path(model_path) / Path(f"{self.version}.h5")
        self.model = tf.keras.models.load_model(final_path)
        return self.model

    def save_results(self, result_path: Path):
        final_path = self.generate_path(result_path) / Path(f"{self.version}.json")
        Path(final_path).parent.mkdir(parents=True, exist_ok=True)
        self.output_results = {
            'test_loss': self.test_loss,
            'test_accuracy': self.test_accuracy,
            'test_crossentropy': self.test_crossentropy,
            'training_history': {
                'loss': [float(x) for x in self.history.history['loss']],
                'accuracy': [float(x) for x in self.history.history['accuracy']],
                'val_loss': [float(x) for x in self.history.history['val_loss']],
                'val_accuracy': [float(x) for x in self.history.history['val_accuracy']]
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