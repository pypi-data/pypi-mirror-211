import json
import numpy as np
import tensorflow as tf
import importlib_resources

from tensorflow import keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (Dense, Flatten, Conv2D, MaxPooling2D)


class BeerClassifier:

    def __init__(self) -> None:
        pass

    @staticmethod
    def predict(path_img):

        width = 128
        height = 128
        size = (width, height)
        channels = 3
        learning_rate = 1e-4

        PATH_METADATA = BeerClassifier.get_path_from_filename('metadata.json')
        json_obj = BeerClassifier.get_object_from_json(PATH_METADATA)

        N_NEURONS_OUT = len(json_obj)

        model = Sequential()

        # Extração de caracteristicas
        model.add(Conv2D(256, (3, 3), activation='relu',
                         input_shape=(width, height, channels)))
        model.add(MaxPooling2D((2, 2)))

        model.add(Conv2D(128, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2, 2)))

        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2, 2)))

        model.add(Conv2D(32, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2, 2)))

        # Achatamento
        model.add(Flatten())

        # classificadores
        model.add(Dense(128, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(N_NEURONS_OUT, activation='softmax'))

        model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss='binary_crossentropy',
            metrics=[
                'accuracy',
                tf.keras.metrics.Precision(),
                tf.keras.metrics.Recall()
            ]
        )

        PATH_CNN_WEIGHTS = BeerClassifier.get_path_from_filename(
            'trained_model.h5')
        model = keras.models.load_model(PATH_CNN_WEIGHTS)

        image_original = tf.keras.utils.load_img(
            path_img,
            grayscale=False,
            color_mode="rgb",
            target_size=None,
            interpolation="nearest"
        )

        image_resized = image_original.resize(size)

        image_prepared = np.expand_dims(image_resized, axis=0)

        return model.predict(image_prepared)

    @staticmethod
    def get_path_from_filename(filename: str):
        return importlib_resources.files('ebeer').joinpath(filename)

    @staticmethod
    def get_object_from_json(path_metadata):
        json_obj = None
        with open(path_metadata, 'r') as file_reader:
            json_obj = json.load(file_reader)
        return json_obj
