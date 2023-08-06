from keras.models \
    import Sequential

from keras.layers \
    import \
    Rescaling, \
    Flatten, \
    Dense, \
    Conv2D, \
    MaxPooling2D, \
    GlobalAveragePooling2D

from GameVisionTargetingModel.variables.model_settings \
    import \
    get_number_of_labels, \
    get_input_set, \
    get_last_layer_multiplier, \
    get_channels


def generate_input_layer(
    layers: list
):
    layers.append(
        Rescaling(
            1./255,
            input_shape=get_input_set()
        )
    )


def generate_preprocessing_layers(
        layers: list
):
    pass


def generate_middle_layer(
    layers: list
):
    generate_first_middle_layer(
        layers
    )

    generate_second_middle_layer(
        layers
    )

    generate_third_middle_layer(
        layers
    )
    
    generate_decision_middle_layer(
        layers
    )


def generate_first_middle_layer(
        layers: list
):
    
    first_layer_size = 512

    layers.append(
        Conv2D(
            first_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            first_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        MaxPooling2D(
            (2, 2)
        )
    )


def generate_second_middle_layer(
        layers: list
):
    second_layer_size = 256

    layers.append(
        Conv2D(
            second_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            second_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            second_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            second_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        MaxPooling2D(
            (2, 2)
        )
    )


def generate_third_middle_layer(
        layers: list
):
    third_layer_size = 128

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        MaxPooling2D(
            (2, 2)
        )
    )


def generate_decision_middle_layer(
        layers: list
):
    decision_layer_size = 64
    
    layers.append(
        Conv2D(
            decision_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            decision_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            decision_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            decision_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        GlobalAveragePooling2D()
    )


def generate_output_layer(
    layers: list
):
    layers.append(
        Flatten()
    )

    layers.append(
        Dense(
            get_number_of_labels()
            *
            get_last_layer_multiplier()
        )
    )

    layers.append(
        Dense(
            get_number_of_labels()
        )
    )


def generate_layers_for_map_classifier_v1(
        addition_of_preprocessing: bool = True
) -> list:
    return_layers: list = []

    generate_input_layer(return_layers)

    if addition_of_preprocessing:
        generate_preprocessing_layers(
            return_layers
        )

    generate_middle_layer(
        return_layers
    )

    generate_output_layer(
        return_layers
    )

    return return_layers


class MapClassifier(
    Sequential
):
    def __init__(self):
        super().__init__(
            generate_layers_for_map_classifier_v1()
        )



