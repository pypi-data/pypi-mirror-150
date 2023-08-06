from subprocess import CalledProcessError
try:
    import samna
    from samna.dynapcnn.configuration import DynapcnnConfiguration
except (ImportError, ModuleNotFoundError, CalledProcessError):
    SAMNA_AVAILABLE = False
else:
    SAMNA_AVAILABLE = True

import torch
from typing import List
from sinabs.backend.dynapcnn.config_builder import ConfigBuilder
from sinabs.backend.dynapcnn.mapping import LayerConstraints

from sinabs.backend.dynapcnn.dvs_layer import DVSLayer
from sinabs.backend.dynapcnn.dynapcnn_layer import DynapcnnLayer


class DynapcnnConfigBuilder(ConfigBuilder):

    @classmethod
    def get_samna_module(cls):
        return samna.dynapcnn

    @classmethod
    def get_default_config(cls) -> "DynapcnnConfiguration":
        return DynapcnnConfiguration()


    @classmethod
    def write_dvs_layer_config(cls, layer: DVSLayer, config: "DvsLayerConfig"):
        for param, value in layer.get_config_dict().items():
            setattr(config, param, value)

    @classmethod
    def write_dynapcnn_layer_config(cls, layer: DynapcnnLayer, chip_layer: "CNNLayerConfig"):
        """
        Write a single layer configuration to the dynapcnn conf object.

        Parameters
        ----------
            layer:
                The dynapcnn layer to write the configuration for
            chip_layer: CNNLayerConfig
                DYNAPCNN configuration object representing the layer to which
                configuration is written.
        """
        config_dict = layer.get_config_dict()
        # Update configuration of the DYNAPCNN layer
        chip_layer.dimensions = config_dict["dimensions"]
        config_dict.pop("dimensions")
        for i in range(len(config_dict["destinations"])):
            if "pooling" in config_dict["destinations"][i]:
                chip_layer.destinations[i].pooling = config_dict["destinations"][i]["pooling"]
        config_dict.pop("destinations")
        for param, value in config_dict.items():
            try:
                setattr(chip_layer, param, value)
            except TypeError as e:
                raise TypeError(f"Unexpected parameter {param} or value. {e}")

    @classmethod
    def build_config(cls, model: "DynapcnnNetwork", chip_layers: List[int]):
        layers = model.sequence
        config = cls.get_default_config()

        i_cnn_layer = 0  # Instantiate an iterator for the cnn cores
        for i, chip_equivalent_layer in enumerate(layers):
            if isinstance(chip_equivalent_layer, DVSLayer):
                chip_layer = config.dvs_layer
                cls.write_dvs_layer_config(chip_equivalent_layer, chip_layer)
            elif isinstance(chip_equivalent_layer, DynapcnnLayer):
                chip_layer = config.cnn_layers[chip_layers[i_cnn_layer]]
                cls.write_dynapcnn_layer_config(chip_equivalent_layer, chip_layer)
                i_cnn_layer += 1
            else:
                # in our generated network there is a spurious layer...
                # should never happen
                raise TypeError("Unexpected layer in the model")

            if i == len(layers) - 1:
                # last layer
                chip_layer.destinations[0].enable = False
            else:
                # Set destination layer
                chip_layer.destinations[0].layer = chip_layers[i_cnn_layer]
                chip_layer.destinations[0].enable = True

        return config

    @classmethod
    def get_constraints(cls) -> List[LayerConstraints]:
        ## Chip specific constraints
        weight_memory_size = [
            16 * 1024,  # 0
            16 * 1024,  # 1
            16 * 1024,  # 2
            32 * 1024,  # 3
            32 * 1024,  # 4
            64 * 1024,  # 5
            64 * 1024,  # 6
            16 * 1024,  # 7
            16 * 1024,
        ]  # _WEIGHTS_MEMORY_SIZE

        neurons_memory_size = [
            64 * 1024,  # 0
            64 * 1024,  # 1
            64 * 1024,  # 2
            32 * 1024,  # 3
            32 * 1024,  # 4
            16 * 1024,  # 5
            16 * 1024,  # 6
            16 * 1024,  # 7
            16 * 1024,
        ]  # 8
        bias_memory_size = [1024] * 9

        constraints = [
            LayerConstraints(km, nm, bm) for (km, nm, bm) in
            zip(weight_memory_size, neurons_memory_size, bias_memory_size)
        ]
        return constraints

    @classmethod
    def monitor_layers(cls, config: "DynapcnnConfiguration", layers: List):
        """
        Updates the config object in place.

        Parameters
        ----------
        config:
            samna config object
        monitor_chip_layers:
            The layers to be monitored on the chip.

        Returns
        -------
        config:
            Returns the modified config. (The config object is modified in place)
        """
        monitor_layers = layers.copy()
        if "dvs" in monitor_layers:
            config.dvs_layer.monitor_enable = True
            monitor_layers.remove("dvs")
        for lyr_indx in monitor_layers:
            config.cnn_layers[lyr_indx].monitor_enable = True
        return config

    @classmethod
    def get_output_buffer(cls):
        return samna.BufferSinkNode_dynapcnn_event_output_event()

    @classmethod
    def reset_states(cls, config: DynapcnnConfiguration, randomize=False):
        for idx, lyr in enumerate(config.cnn_layers):
            shape = torch.tensor(lyr.neurons_initial_value).shape
            # set the config's neuron initial state values into zeros
            if randomize:
                new_state = torch.randint(lyr.threshold_low, lyr.threshold_high, shape).tolist()
            else:
                new_state = torch.zeros(shape, dtype=torch.int).tolist()
            config.cnn_layers[idx].neurons_initial_value = new_state
        return config
