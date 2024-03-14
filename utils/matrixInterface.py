from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union

from numpy._typing import ArrayLike
from scipy.sparse import coo_array


class matrixInterface(ABC):

    def __init__(self, size, elements):
        pass

    @property
    @abstractmethod
    def matrix(
        self,
    ) -> Union[coo_array, ArrayLike]:
        pass

    @property
    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def tensor(self, other: matrixInterface) -> matrixInterface:
        pass

    @abstractmethod
    def reshape(self, rows: int, cols: int) -> matrixInterface:
        pass

    @abstractmethod
    def update(self, row: int, col: int, value: float) -> matrixInterface:
        pass

    @abstractmethod
    def multiply(self, other: matrixInterface) -> matrixInterface:
        pass

    @abstractmethod
    def power(self, exponent: int) -> matrixInterface:
        pass

    @abstractmethod
    def add(self, other: matrixInterface) -> matrixInterface:
        pass

    @abstractmethod
    def subtract(self, other: matrixInterface) -> matrixInterface:
        pass

    @abstractmethod
    def equal(self, other: matrixInterface) -> matrixInterface:
        pass

    @abstractmethod
    def negate(self) -> matrixInterface:
        pass

    @abstractmethod
    def scale(self, factor: float) -> matrixInterface:
        pass

    @abstractmethod
    def toVector(self) -> matrixInterface:
        pass

    @abstractmethod
    def dimension(self) -> matrixInterface:
        pass

    @abstractmethod
    def flat(self) -> ArrayLike:
        pass

    #            CONCRETE            #
    def __mul__(self, other: matrixInterface) -> matrixInterface:
        self.multiply(other)
        return self

    def __pow__(self, exponent: int) -> matrixInterface:
        self.power(exponent)
        return self

    def __add__(self, other: matrixInterface) -> matrixInterface:
        self.add(other)
        return self

    def __sub__(self, other: matrixInterface) -> matrixInterface:
        self.subtract(other)
        return self
