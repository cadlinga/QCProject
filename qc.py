from typing import Union


class Qubit:
    """Quantum Bit Implementation"""

    def __init__(self, register=None, index: int = None):
        if (register, index) == (None, None):
            self._register = None
            self._index = None
        else:

            if index < 0:
                """
                If the index is negative, place bit
                that many places from the end of the register.
                """
                index += register.size

            if index >= register.size:
                """
                If the index is larger than the register size
                throw an exception.
                """
                raise Exception(
                    """
                    Index must `fit` within the register.
                    The index provided was too large.
                    (Remember 0 based indexing)
                    """
                )

            self._register = register
            self._index = index

    def __repr__(self) -> str:
        return f"Qubit({self._register, self._index})"


class Register:
    """Quantum Register Implementation."""

    def __init__(self, size: int):
        if size < 0:
            raise Exception(
                """
                Size of register must be a positive int.
                %s is not a acceptable.
                """
                % size
            )

        self._size = size
        self._bits = [Qubit(self, i) for i in range(size)]

    @property
    def size(self):
        return self._size

    @property
    def bits(self):
        return self._bits

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__qualname__, self.size)


class Circuit:

    def __init__(self, register: Register):
        self.register = register
        pass

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__qualname__, self.register)

    # def apply(self, gate: Gate, index: int):

    def h(self, target: Union[list[int], int]):
        if isinstance(target, int):
            # apply to single target
            print("Apply H gate to bit %d" % target)
            pass
        if isinstance(target, list):
            # apply to list of targets
            pass
