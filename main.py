# Open obj file
import sys
import numpy as np

import src.io as io
import src.inward as inward
import src.utils as utils
import src.tetrahedron as tetrahedron


class ObjToMshConverter:

    tetrahedron_instance = None

    def __init__(
        self,
        offset_distance=0.05,
    ):  # 5cm
        """
        Initialize the ObjeToMshConverter with the paths to the .obj and .msh files.
        """
        self.offset_distance = offset_distance

        self.vertices_str_list = []
        self.faces_str_list = []

        self.io_instance = io.io()

    def make_inward_obj(self):
        if (
            self.in_file_name is None
            or self.obj_file_path is None
            or self.out_file_name is None
            or self.obj_out_path is None
        ):
            raise ValueError(
                "File name, object file path, and output path must be set."
            )

        self.make_inward_obj(
            self.in_file_name, self.obj_file_path, self.out_file_name, self.obj_out_path
        )

    def make_inward_obj(self, in_file_name, obj_in_path, out_file_name, obj_out_path):
        """
        Creating a inward version of the object from the .obj file.
        """

        self.in_file_name = in_file_name
        self.obj_file_path = obj_in_path
        self.out_file_name = out_file_name
        self.obj_out_path = obj_out_path

        if not in_file_name.endswith(".obj"):
            in_file_name += ".obj"
        if not out_file_name.endswith(".obj"):
            out_file_name += ".obj"
        if not obj_in_path.endswith("/"):
            obj_in_path += "/"
        if not obj_out_path.endswith("/"):
            obj_out_path += "/"

        self.obj_file_full_path = obj_in_path + in_file_name
        self.obj_out_full_path = obj_out_path + out_file_name

        self.line_data_list = self.io_instance.read_file(self.obj_file_full_path)

        self.vertices_list, self.faces_list = (
            utils.vertice_and_face_list_from_obj_lines(self.line_data_list)
        )

        # Create an instance of the Inward class
        inward_obj = inward.Inward(
            self.vertices_list, self.faces_list, self.offset_distance
        )
        # Get the inward vertices
        inward_object_string_list = inward_obj.make_inward_object()

        # Write the inward object to a new .obj file
        self.io_instance.write_str_file(
            self.obj_out_full_path, inward_object_string_list
        )

    def make_msh_string_list(self, nod_list, element_list):

        return_list = []
        return_list.append("$NOD")
        return_list.append(str(len(nod_list)))
        for i, vertex in enumerate(nod_list):
            return_list.append(str(i + 1) + " " + f"{' '.join(map(str, vertex))}")
        return_list.append("$ENDNOD")
        return_list.append("$ELM")
        return_list.append(str(len(element_list)))
        for i, tetrahedron in enumerate(element_list):
            return_list.append(
                str(i + 1)
                + " 4 1 1 4 "
                + f"{' '.join(map(str, [index + 1 for index in tetrahedron]))}"
            )
        return_list.append("$ENDELM")

        return return_list

    def make_msh(self, in_file_name, obj_in_path, out_file_name, msh_out_path):
        """
        Creating a tetrahedron version of the object from the .obj file.
        """

        self.in_file_name = in_file_name
        self.obj_file_path = obj_in_path
        self.out_file_name = out_file_name
        self.msh_out_path = msh_out_path

        if not in_file_name.endswith(".obj"):
            in_file_name += ".obj"
        if not out_file_name.endswith(".msh"):
            out_file_name += ".msh"
        if not obj_in_path.endswith("/"):
            obj_in_path += "/"
        if not msh_out_path.endswith("/"):
            msh_out_path += "/"

        self.obj_file_full_path = obj_in_path + in_file_name
        self.msh_out_full_path = msh_out_path + out_file_name

        self.line_data_list = self.io_instance.read_file(self.obj_file_full_path)

        self.vertices_list, self.faces_list = (
            utils.vertice_and_face_list_from_obj_lines(self.line_data_list)
        )

        self.tetrahedron_instance = tetrahedron.TetrahedronDivier(
            len(self.vertices_list)
        )

        # Create an instance of the Inward class
        inward_obj = inward.Inward(
            self.vertices_list, self.faces_list, self.offset_distance
        )
        # Get the inward vertices
        inward_vertices_list = inward_obj.make_inward_vertices()

        # Create tetrahedrons between the original and inward vertices
        tetrahedron_list = self.tetrahedron_instance.generating_tetrahedrons(
            self.faces_list
        )

        string_list = self.make_msh_string_list(
            self.vertices_list + inward_vertices_list, tetrahedron_list
        )

        self.io_instance.write_str_file(self.msh_out_full_path, string_list)


test = ObjToMshConverter()
test.make_msh("cube_5x5", "./examples/", "cube_5x5", "./examples/")
