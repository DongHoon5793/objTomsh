def cross_2_3d_vectors_dtype_list(a: list, b: list):
    """
    Calculate the cross product of two vectors.

    Parameters:
    a (List[number]): The first list of vectors.
    b (List[number]): The second list of vectors.
    """
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def normalize_vector_dtype_list(vector: list):
    """
    Normalize a vector.

    Parameters:
    vector (List[number]): The vector to be normalized.
    """
    length = sum([i**2 for i in vector]) ** 0.5
    return [i / length for i in vector] if length != 0 else vector
