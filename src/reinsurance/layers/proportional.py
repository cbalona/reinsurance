"""
Collection of proportional reinsurance structures.
"""

import numpy as np
from dask import delayed

from reinsurance.layers.core import Layer


class QuotaShare(Layer):
    def __init__(
        self, cession: float, commission: float = 0.0, name: str = None
    ) -> None:
        """
        Initialize a QuotaShare layer.

        Args:
            cession (float): Cession value.
            commission (float, optional): Commission value. Defaults to 0.0.
            name (str, optional): Name of the layer. Defaults to None.
        """
        super().__init__(name=name)
        self.cession = cession
        self.commission = commission

    @delayed(nout=1)
    def quota_share(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Perform quota share calculations.

        Args:
            x (np.ndarray): Input array.

        Returns:
            dict[str, np.ndarray]: Dictionary containing gross, recovery, and
            commission arrays.
        """
        return {
            "gross": x,
            "recovery": x * self.cession,
            "commission": x * self.commission,
        }

    def forward(self, x: np.ndarray) -> dict[str, np.ndarray]:
        """
        Forward pass of the QuotaShare layer.

        Args:
            x (np.ndarray): Input array.

        Returns:
            dict[str, np.ndarray]: Dictionary containing gross, recovery, and commission
            arrays.
        """
        return self.quota_share(x, dask_key_name=self.name)
