class TetrahedronDivier:
    number_of_original_vertices = None

    def __init__(self, number_of_original_vertices):
        self.number_of_original_vertices = number_of_original_vertices

    def generating_tetrahedrons(self, faces):
        """
        Divide two layer diagrams into non-overlapping tetrahedrons.
        """

        # Divide the diagram into triangles
        triangles_indexs_list = []
        for face in faces:
            buff = self.__generating_triangles(face)
            for triangle in buff:
                triangles_indexs_list.append(triangle)

        total_tetrahedrons_points_index_list = []
        # Divide the triangles into tetrahedrons
        for triangle_indexs in triangles_indexs_list:
            # Divide the triangle into tetrahedrons
            tetrahedrons_list = self.__generating_tetrahedrons_from_triangles(
                triangle_indexs
            )
            for tetrahedron_indexs in tetrahedrons_list:
                total_tetrahedrons_points_index_list.append(tetrahedron_indexs)

        return total_tetrahedrons_points_index_list

    def __generating_triangles(self, face):
        """
        Divide the face into triangles.

        Parameters:
        face (List(int))
        """

        triangles_indexs_list = [[face[0], face[1], face[2]]]

        for i in range(3, len(face)):
            triangles_indexs_list.append([face[0], face[i - 1], face[i]])

        return triangles_indexs_list

    def __generating_tetrahedrons_from_triangles(self, triangle_indexs):
        """
        Divide two layer triangles into non-overlapping tetrahedrons.
        """
        # Divide the triangle into tetrahedrons
        tetrahedrons_indexs_list = []
        tetrahedrons_indexs_list.append(
            [
                triangle_indexs[0],
                triangle_indexs[1],
                triangle_indexs[2],
                triangle_indexs[0] + self.number_of_original_vertices,
            ]
        )
        tetrahedrons_indexs_list.append(
            [
                triangle_indexs[0] + self.number_of_original_vertices,
                triangle_indexs[1] + self.number_of_original_vertices,
                triangle_indexs[2] + self.number_of_original_vertices,
                triangle_indexs[1],
            ]
        )
        tetrahedrons_indexs_list.append(
            [
                triangle_indexs[1],
                triangle_indexs[2],
                triangle_indexs[2] + self.number_of_original_vertices,
                triangle_indexs[0] + self.number_of_original_vertices,
            ]
        )

        return tetrahedrons_indexs_list
