"""
Model classes used to define a model graph.
"""

import dask
import numpy as np

from reinsurance.layers.core import Layer


class Model:
    def __init__(self, input_layers: list[Layer], output_layers: list[Layer]):
        """
        Initialize a Model.

        Args:
            input_layers (list[Layer]): List of input layers.
            output_layers (list[Layer]): List of output layers.
        """
        self.input_layers = input_layers
        self.output_layers = output_layers

    def compute(
        self, scheduler: str = None
    ) -> list[np.ndarray | dict[str, np.ndarray]]:
        """
        Compute the outputs of the model.

        Args:
            scheduler (str, optional): Dask scheduler to use. Defaults to None.

        Returns:
            list[np.ndarray | dict[str, np.ndarray]]: List of computed outputs.
        """
        computed_outputs = []
        for output_layer in self.output_layers:
            if isinstance(output_layer.output, np.ndarray):
                computed_outputs.append(output_layer.output)
                continue

            if isinstance(output_layer.output, dict):
                for key in output_layer.output.keys():
                    if isinstance(output_layer.output[key], np.ndarray):
                        continue
                    output_layer.output[key] = output_layer.output[key].compute(
                        scheduler=scheduler
                    )
                computed_outputs.append(output_layer.output)
                continue

            computed_outputs.append(output_layer.output.compute(scheduler=scheduler))

        return computed_outputs

    def visualize(self) -> None:
        """
        Visualize the computation graph of the model.
        """
        return dask.visualize([layer.output for layer in self.output_layers])
