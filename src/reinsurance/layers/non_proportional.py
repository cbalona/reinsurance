"""
Collection of non-proportional reinsurance structures.
"""

import numpy as np
from dask import delayed

from reinsurance.layers.core import Layer


class ExcessOfLossLayer(Layer):
    def __init__(
        self,
        attachment: float,
        width: float,
        deductible: float = 0,
        rate_on_line: float = 0,
        reinstatements: int = 0,
        free_reinstatements: int = 0,
        name: str = None,
    ):
        """
        Initialize an ExcessOfLossLayer.

        Args:
            attachment (float): Attachment point.
            width (float): Width of the layer.
            deductible (float, optional): Deductible value. Defaults to 0.
            rate_on_line (float, optional): Rate on line value. Defaults to 0.
            reinstatements (int, optional): Number of reinstatements. Defaults to 0.
            free_reinstatements (int, optional): Number of free reinstatements. Defaults
            to 0.
            name (str, optional): Name of the layer. Defaults to None.
        """
        super().__init__(name=name)
        self.attachment = attachment
        self.width = width
        self.deductible = deductible
        self.rate_on_line = rate_on_line
        self.reinstatements = reinstatements
        self.free_reinstatements = free_reinstatements

    def _burn(self, x: np.ndarray) -> np.ndarray:
        """
        Calculate the burn values.

        Args:
            x (np.ndarray): Input array.

        Returns:
            np.ndarray: Array containing burn values.
        """
        init_recovery = np.minimum(self.width, np.maximum(0, x - self.attachment))
        layer_burn = np.clip(
            (init_recovery / self.width).cumsum(axis=1), 0, self.reinstatements + 1
        )
        layer_burn = np.diff(layer_burn, prepend=0)
        return layer_burn

    def _recovery(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Calculate the recovery array.

        Args:
            x (np.ndarray): Input array.

        Returns:
            dict[str, np.ndarray]: Dictionary containing the recovery array.
        """
        recovery = self._burn(x) * self.width * (1 - self.deductible)
        return recovery

    def _reinstatement_premium(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Calculate the reinstatement premium array.

        Args:
            x (np.ndarray): Input array.

        Returns:
            dict[str, np.ndarray]: Dictionary containing the reinstatement
            premium array.
        """
        return (
            np.diff(
                np.clip(
                    self._burn(x).cumsum(axis=1),
                    self.free_reinstatements,
                    self.reinstatements,
                ),
                prepend=self.free_reinstatements,
            )
        ) * (self.rate_on_line * self.width)

    @delayed(nout=1)
    def excess_of_loss(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Calculate the excess of loss arrays.

        Args:
            x (np.ndarray): Input array.

        Returns:
            dict[str, np.ndarray]: Dictionary containing gross, recovery, and
            reinstatement premium arrays.
        """
        return {
            "gross": x,
            "recovery": self._recovery(x),
            "reinstatement_premium": self._reinstatement_premium(x),
        }

    def forward(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Forward pass of the ExcessOfLossLayer.

        Args:
            x (np.ndarray): Input array.

        Returns:
            dict[str, np.ndarray]: Dictionary containing gross, recovery, and
            reinstatement premium arrays.
        """
        return self.excess_of_loss(x)
