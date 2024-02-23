from utils.tensor import Vector


def makeStateVector(value: int, size: int = 0):

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
