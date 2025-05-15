from src import c_math as math_utils


class Inward:

    inward_vertice_list = None

    def __init__(self, vertice_list, face_list, offset_distance=0.01):  # Default is 1cm
        """

        Parameters:
        vertice_list (List[List[float]]): The list of original vertices.
        face_list (List[List[int]]): The list of faces.
        offset_distance (float): The distance to offset the vertices inward.
        """
        self.offset_distance = offset_distance
        self.vertice_list = vertice_list
        self.face_list = face_list

        self.inward_vertice_list = self.make_inward_vertices()

    def make_inward_vertices(self):
        """
        Make inward vertices from the original vertices.

        Parameters:

        Returns:
        inward_vertice_list (List[List[float]]): The list of inward vertices.
        """

        # Calculate the normals of the vertices
        vertex_normal_list = self.__vertex_normals(self.vertice_list, self.face_list)

        # Calculate the inward vertices
        inward_vertice_list = self.__inward_vertices(
            self.vertice_list, vertex_normal_list
        )

        return inward_vertice_list

    def make_inward_object(self):

        if self.inward_vertice_list is None:
            self.inward_vertice_list = self.make_inward_vertices()

        object_string_list = []

        for i_vertice in range(len(self.inward_vertice_list)):
            object_string_list.append(
                f"v {self.inward_vertice_list[i_vertice][0]} {self.inward_vertice_list[i_vertice][1]} {self.inward_vertice_list[i_vertice][2]}"
            )
        for i_face in range(len(self.face_list)):
            str_face = "f "
            for i in range(len(self.face_list[i_face])):
                str_face += f"{self.face_list[i_face][i] + 1} "
            object_string_list.append(str_face[:-1])

        return object_string_list

    def __vertex_normals(self, vertice_list, face_list):
        """
        Calculate the normals of the vertices.

        Parameters:
        vertice_list (List[List[float]]): The list of original vertices.
        face_list (List[List[int]]): The list of faces.

        Returns:
        vertex_normal_list List[List[float]]: The list of vertex normals.
        """

        # initialize the vertex normal list for result
        vertex_normal_list = []
        for _ in range(len(vertice_list)):
            vertex_normal_list.append([0, 0, 0])

        # Calculate the normals of the vertices
        for face in face_list:

            # Calculate the edge vectors
            edge_0 = [
                vertice_list[face[0]][0] - vertice_list[face[1]][0],
                vertice_list[face[0]][1] - vertice_list[face[1]][1],
                vertice_list[face[0]][2] - vertice_list[face[1]][2],
            ]

            edge_1 = [
                vertice_list[face[1]][0] - vertice_list[face[2]][0],
                vertice_list[face[1]][1] - vertice_list[face[2]][1],
                vertice_list[face[1]][2] - vertice_list[face[2]][2],
            ]

            # Calculate the normal vector of the face
            face_normal = math_utils.cross_2_3d_vectors_dtype_list(edge_0, edge_1)

            for vertex_index in face:
                # Add the normal vector to the vertex normal
                vertex_normal_list[vertex_index][0] += face_normal[0]
                vertex_normal_list[vertex_index][1] += face_normal[1]
                vertex_normal_list[vertex_index][2] += face_normal[2]

        # Normalize the vertex normals
        for i in range(len(vertex_normal_list)):
            vertex_normal_list[i] = math_utils.normalize_vector_dtype_list(
                vertex_normal_list[i]
            )

        return vertex_normal_list

    def __inward_vertices(self, vertice_list, vertex_normal_list):
        """
        Calculate the inward vertices.

        Parameters:
        vertice_list (List[List[float]]): The list of original vertices.
        vertex_normal_list (List[List[float]]): The list of vertex normals.

        Returns:
        inward_vertices List[List[float]]: The list of inward vertices.
        """

        # Calculate the inward vertices
        inward_vertices = []
        for i in range(len(vertice_list)):
            inward_vertices.append(
                [
                    vertice_list[i][0]
                    - self.offset_distance * vertex_normal_list[i][0],
                    vertice_list[i][1]
                    - self.offset_distance * vertex_normal_list[i][1],
                    vertice_list[i][2]
                    - self.offset_distance * vertex_normal_list[i][2],
                ]
            )

        return inward_vertices
