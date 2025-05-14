def vertice_and_face_list_from_obj_lines(
    lines: list,
) -> tuple[list[list[float]], list[list[int]]]:
    """
    Convert lines from an OBJ file to vertex and face lists.

    Parameters:
    lines (List[str]): The lines from the OBJ file.

    Returns:
    vertice_list (List[List[float]]): The list of vertices.
    face_list (List[List[int]]): The list of faces INDEX of vertexs (0-(N-1)) NOT the actual number of vertexs (1-N).
    """
    vertice_list = []
    face_list = []

    for line in lines:
        if line.startswith("v "):
            vertice_list.append([float(i) for i in line.split()[1:]])
        elif line.startswith("f "):
            face_list.append([int(i.split("/")[0]) - 1 for i in line.split()[1:]])

    return vertice_list, face_list
