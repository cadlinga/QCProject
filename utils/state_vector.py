from utils.tensor import Vector


def makeStateVector(value: int, size: int = 0):
    r"""
    Creates a state vector based on the given integer value.

    The function takes an integer `value` and an optional `size` parameter. It converts
    the integer to its binary representation and creates a tensor product of individual
    qubit state vectors corresponding to each binary digit.

    If the `size` parameter is not provided, the size of the state vector is determined
    by the length of the binary representation of the `value`.

    Args:
        value (int): The integer value to create the state vector from.
        size (int): The desired size of the state vector. If not provided, the size is
                    determined by the length of the binary representation of `value`.

    Returns:
        Vector: The state vector created as a tensor product of individual qubit state vectors.
    """

    length = len(f"{value: b}")

    if int is None:
        size = length

    binary = [*format(value, "0" + str(size) + "b")]

    vectors = []
    for i in binary:
        vectors.append(Vector(int(i)))

    product = vectors[0]
    j = 1
    while j < len(vectors):
        product = product.tensor(vectors[j])
        j += 1
    return product


# TODO write tests to verify - examples below
# print(makeStateVector(6))
# print(Vector([1, 0]).tensor(Vector([1, 0])).tensor(Vector([0, 1])))
