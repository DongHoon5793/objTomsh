"""
This module contains functions for reading and writing data to and from files.
It includes functions to read and write .obj files, as well as .msh files.
It also includes a class for handling the file operations.
"""


class io:
    def __init__(self, dtype="str"):
        """
        Initialize the io class with a specified data type.

        Parameters:
        dtype (str): The data type to be used for reading and writing files.
                      Default is "str".
        """
        # Initialize the data type
        # dtype can be "str", "int", "float", etc.
        # depending on the requirements of the file operations.

        self.dtype = dtype

    def read_file(self, file_path):

        self.data_line_list = self.__read_obj_file(file_path)

        # Filter the lines to remove line breaks
        self.data_line_list = self.__line_breaker_filter(self.data_line_list)

        return self.data_line_list

    def write_str_file(self, file_path, string_list):
        """
        Write a list of strings to a file.

        Parameters:
        file_path (str): The path to the file.
        string_list (List[str]): The list of strings to be written to the file.
        """
        # Open the file for writing
        with open(file_path, "w") as file:
            # Write each string in the list to the file
            for string in string_list:
                file.write(string + "\n")
        # Close the file

    def __read_obj_file(self, file_path):
        """
        Read a .obj file and extract each line as strings.
        """
        # Open the .obj file
        with open(file_path, "r") as file:
            lines = file.readlines()

        return lines

    def __write_obj_file(self, file_path, vertices, faces):
        # Open the .obj file for writing
        with open(file_path, "w") as file:
            # Write the vertices to the file
            for vertex in vertices:
                file.write(f"v {' '.join(map(str, vertex))}\n")
            # Write the faces to the file
            for face in faces:
                file.write(f"f {' '.join(map(str, [index + 1 for index in face]))}\n")

    def __write_msh_file(self, file_path, vertices, faces):
        # Open the .msh file for writing
        with open(file_path, "w") as file:
            # Write the header
            file.write("$MeshFormat\n2.2 0 8\n$EndMeshFormat\n")
            # Write the vertices
            file.write("$Nodes\n")
            file.write(f"{len(vertices)}\n")
            for i, vertex in enumerate(vertices):
                file.write(f"{i + 1} {' '.join(map(str, vertex))}\n")
            file.write("$EndNodes\n")
            # Write the elements
            file.write("$Elements\n")
            file.write(f"{len(faces)}\n")
            for i, face in enumerate(faces):
                file.write(
                    f"{i + 1} 2 2 0 {' '.join(map(str, [index + 1 for index in face]))}\n"
                )
            file.write("$EndElements\n")

    def __line_breaker_filter(self, lines):
        """
        Filter the lines to remove line breaks.
        """
        filtered_lines = []
        for line in lines:
            if line.endswith("\n"):
                line = line[:-1]
            filtered_lines.append(line)

        return filtered_lines
