"""
Collection of base classes for overall layer implementation.
"""
from typing import Self
import numpy as np
from dask import delayed


class Layer:
    def __init__(self, name: str = None) -> None:
        """
        Initialize a Layer object.

        Args:
            name (str, optional): Name of the layer. Defaults to None.
        """
        self.output = None
        self.name = name

    @delayed
    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Forward pass of the layer.

        Args:
            x (np.ndarray): Input array.

        Returns:
            np.ndarray: Output array.
        """
        raise NotImplementedError("Each subclass must implement the forward method")

    def __call__(self, input_layer: Self) -> Self:
        """
        Perform forward pass through the layer.

        Args:
            input_layer (Self): Input layer.

        Returns:
            Self: Output layer.
        """
        self.output = self.forward(input_layer.output)
        return self

    def __add__(self, other: Self) -> Self:
        """
        Add two layers.

        Args:
            other (Self): Layer to be added.

        Returns:
            Self: Resulting layer.
        """
        return Add()(self, other)

    def __sub__(self, other: Self) -> Self:
        """
        Subtract two layers.

        Args:
            other (Self): Layer to be subtracted.

        Returns:
            Self: Resulting layer.
        """
        return Subtract()(self, other)

    def __mul__(self, other: Self) -> Self:
        """
        Multiply two layers.

        Args:
            other (Self): Layer to be multiplied.

        Returns:
            Self: Resulting layer.
        """
        return Multiply()(self, other)

    def __truediv__(self, other: Self) -> Self:
        """
        Divide two layers.

        Args:
            other (Self): Layer to be divided.

        Returns:
            Self: Resulting layer.
        """
        return Divide()(self, other)


class Add(Layer):
    @delayed(nout=1)
    def add(self, x1: Layer, x2: Layer) -> Layer:
        """
        Add two layers.

        Args:
            x1 (Layer): First layer.
            x2 (Layer): Second layer.

        Returns:
            Layer: Resulting layer.
        """
        return x1 + x2

    def forward(self, x1: Layer, x2: Layer) -> Layer:
        """
        Forward pass of the addition layer.

        Args:
            x1 (Layer): First layer.
            x2 (Layer): Second layer.

        Returns:
            Layer: Resulting layer.
        """
        return self.add(x1, x2)

    def __call__(self, x1: Layer, x2: Layer) -> Layer:
        """
        Perform forward pass through the layer.

        Args:
            x1 (Layer): Left layer.
            x2 (Layer): Right layer.

        Returns:
            Self: Output layer.
        """
        self.output = self.forward(x1.output, x2.output)
        return self


class Subtract(Layer):
    @delayed(nout=1)
    def subtract(self, x1: Layer, x2: Layer) -> Layer:
        """
        Subtract two layers.

        Args:
            x1 (Layer): First layer.
            x2 (Layer): Second layer.

        Returns:
            Layer: Resulting layer.
        """
        return x1 - x2

    def forward(self, x1: Layer, x2: Layer) -> Layer:
        """
        Forward pass of the subtraction layer.

        Args:
            x1 (Layer): First layer.
            x2 (Layer): Second layer.

        Returns:
            Layer: Resulting layer.
        """
        return self.subtract(x1, x2)

    def __call__(self, x1: Layer, x2: Layer) -> Layer:
        """
        Perform forward pass through the layer.

        Args:
            x1 (Layer): Left layer.
            x2 (Layer): Right layer.

        Returns:
            Self: Output layer.
        """
        self.output = self.forward(x1.output, x2.output)
        return self


class Multiply(Layer):
    @delayed(nout=1)
    def multiply(self, x1: Layer, x2: Layer) -> Layer:
        """
        Multiply two layers.

        Args:
            x1 (Layer): First layer.
            x2 (Layer): Second layer.

        Returns:
            Layer: Resulting layer.
        """
        return x1 * x2

    def forward(self, x1: Layer, x2: Layer) -> Layer:
        """
        Forward pass of the multiplication layer.

        Args:
            x1 (Layer): First layer.
            x2 (Layer): Second layer.

        Returns:
            Layer: Resulting layer.
        """
        return self.multiply(x1, x2)

    def __call__(self, x1: Layer, x2: Layer) -> Layer:
        """
        Perform forward pass through the layer.

        Args:
            x1 (Layer): Left layer.
            x2 (Layer): Right layer.

        Returns:
            Self: Output layer.
        """
        self.output = self.forward(x1.output, x2.output)
        return self


class Divide(Layer):
    @delayed(nout=1)
    def divide(self, x1: Layer, x2: Layer) -> Layer:
        """
        Divide two layers.

        Args:
            x1 (Layer): First layer.
            x2 (Layer): Second layer.

        Returns:
            Layer: Resulting layer.
        """
        return x1 / x2

    def forward(self, x1: Layer, x2: Layer) -> Layer:
        """
        Forward pass of the division layer.

        Args:
            x1 (Layer): First layer.
            x2 (Layer): Second layer.

        Returns:
            Layer: Resulting layer.
        """
        return self.divide(x1, x2)

    def __call__(self, x1: Layer, x2: Layer) -> Layer:
        """
        Perform forward pass through the layer.

        Args:
            x1 (Layer): Left layer.
            x2 (Layer): Right layer.

        Returns:
            Self: Output layer.
        """
        self.output = self.forward(x1.output, x2.output)
        return self


class Input(Layer):
    def __init__(self, x: np.ndarray, name: str = None) -> None:
        """
        Initialize an Input layer.

        Args:
            x (np.ndarray): Input array.
        """
        super().__init__()
        self.output = self.forward(x)
        self.name = name

    @delayed(nout=1)
    def input(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Identity return.

        Args:
            x (np.ndarray): Input array.

        Returns:
            np.ndarray: Input array.
        """
        return x

    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Forward pass of the Input layer.

        Args:
            x (np.ndarray): Input array.

        Returns:
            np.ndarray: Output array.
        """
        return self.input(x, dask_key_name=self.name)


class Recovery(Layer):
    @delayed(nout=1)
    def recovery(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Retrieve the recovery array from the input dictionary.

        Args:
            x (np.ndarray): Input dictionary.

        Returns:
            dict[str, np.ndarray]: Dictionary containing the recovery array.
        """
        return x["recovery"]

    def forward(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Forward pass of the Recovery layer.

        Args:
            x (np.ndarray): Input dictionary.

        Returns:
            dict[str, np.ndarray]: Dictionary containing the recovery array.
        """
        return self.recovery(x)


class Commission(Layer):
    @delayed(nout=1)
    def commission(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Retrieve the commission array from the input dictionary.

        Args:
            x (np.ndarray): Input dictionary.

        Returns:
            dict[str, np.ndarray]: Dictionary containing the commission array.
        """
        return x["commission"]

    def forward(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Forward pass of the Commission layer.

        Args:
            x (np.ndarray): Input dictionary.

        Returns:
            dict[str, np.ndarray]: Dictionary containing the commission array.
        """
        return self.commission(x)


class ReinstatementPremium(Layer):
    @delayed(nout=1)
    def reinstatement_premium(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Retrieve the reinstatement premium array from the input dictionary.

        Args:
            x (np.ndarray): Input dictionary.

        Returns:
            dict[str, np.ndarray]: Dictionary containing the reinstatement
            premium array.
        """
        return x["reinstatement_premium"]

    def forward(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Forward pass of the ReinstatementPremium layer.

        Args:
            x (np.ndarray): Input dictionary.

        Returns:
            dict[str, np.ndarray]: Dictionary containing the reinstatement
            premium array.
        """
        return self.reinstatement_premium(x)
