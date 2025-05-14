# Open obj file
import sys
import numpy as np

import src.io as io
import src.inward as inward
import src.utils as utils


class ObjToMshConverter:

    def __init__(
        self,
        file_name,
        obj_file_path,
        msh_file_path,
        prefix="",
        surfix="",
        offset_distance=0.05,
    ):  # 5cm
        """
        Initialize the ObjeToMshConverter with the paths to the .obj and .msh files.
        """
        if not file_name.endswith(".obj"):
            file_name += ".obj"
        if not obj_file_path.endswith("/"):
            obj_file_path += "/"

        self.obj_file_path = obj_file_path
        self.obj_file_full_path = obj_file_path + file_name
        self.msh_file_path = msh_file_path
        self.offset_distance = offset_distance

        self.vertices_str_list = []
        self.faces_str_list = []

        self.io_instance = io.io()
        self.line_data_list = self.io_instance.read_file(self.obj_file_full_path)

        self.vertices_list, self.faces_list = (
            utils.vertice_and_face_list_from_obj_lines(self.line_data_list)
        )

    def make_inward_obj(self, file_path, file_name):
        """
        Creating a inward version of the object from the .obj file.
        """

        # Create a new .obj file path
        if not file_path.endswith("/"):
            file_path += "/"
        if not file_name.endswith(".obj"):
            file_name += ".obj"
        inward_obj_file_path = file_path + file_name

        # Create an instance of the Inward class
        inward_obj = inward.Inward(
            self.vertices_list, self.faces_list, self.offset_distance
        )
        # Get the inward vertices
        inward_object_string_list = inward_obj.make_inward_object()

        # Write the inward object to a new .obj file
        self.io_instance.write_str_file(inward_obj_file_path, inward_object_string_list)


test = ObjToMshConverter("cube_5x5", "./examples/", "./examples/")
test.make_inward_obj(test.obj_file_path, "inward_cube_5x5.obj")

quit()


def read_obj_file(file_path):
    # Open the .obj file
    with open(file_path, "r") as file:
        # Read the lines of the file
        lines = file.readlines()
        # Initialize lists to store vertices and faces
        vertices = []
        faces = []
        # Loop through each line in the file
        for line in lines:
            # Split the line into parts
            parts = line.split()
            # If the line starts with 'v', it's a vertex
            if parts and parts[0] == "v":
                # Append the vertex to the vertices list
                vertices.append([float(coord) for coord in parts[1:]])
            # If the line starts with 'f', it's a face
            elif parts and parts[0] == "f":
                # Append the face to the faces list
                # Convert the face indices to integers and subtract 1 for 0-based indexing
                face = [int(index.split("/")[0]) - 1 for index in parts[1:]]
                faces.append(face)
    return vertices, faces


def get_center_of_obj(vertices):
    # Calculate the center of the object
    x_coords = [vertex[0] for vertex in vertices]
    y_coords = [vertex[1] for vertex in vertices]
    z_coords = [vertex[2] for vertex in vertices]
    center_x = sum(x_coords) / len(vertices)
    center_y = sum(y_coords) / len(vertices)
    center_z = sum(z_coords) / len(vertices)
    return [center_x, center_y, center_z]


def compute_vertex_normals(vertices, faces):
    vertex_normals = np.zeros_like(vertices)

    for face in faces:
        if len(face) < 3:
            continue
        v0, v1, v2 = [vertices[i] for i in face[:3]]
        face_normal = np.cross(v1 - v0, v2 - v0)
        face_normal /= np.linalg.norm(face_normal) + 1e-10

        for idx in face:
            vertex_normals[idx] += face_normal

    norms = np.linalg.norm(vertex_normals, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vertex_normals / norms


def offset_vertices(vertices, normals, offset):
    return vertices - normals * offset


def create_smaller_obj_vertices(vertices, faces, offset_distance=0.3):
    np_vertices = np.array(vertices)
    normals = compute_vertex_normals(np_vertices, faces)
    new_vertices = offset_vertices(np_vertices, normals, offset_distance)

    return new_vertices


def create_smaller_obj_old(vertices, faces, scale_factor=0.8):
    # Get the center of the object
    center = get_center_of_obj(vertices)
    # Create a new list to store the smaller vertices
    smaller_vertices = []

    vertex_normal = np.zeros_like(vertices)

    for i, face in enumerate(faces):
        for vertex_index in face:
            vertex_normal[vertex_index] += np.array(vertices[vertex_index])

    # Loop through each vertex
    for vertex in vertices:
        # Scale the vertex coordinates
        smaller_vertex = [
            center[0] + (vertex[0] - center[0]) * scale_factor,
            center[1] + (vertex[1] - center[1]) * scale_factor,
            center[2] + (vertex[2] - center[2]) * scale_factor,
        ]
        # Append the smaller vertex to the list
        smaller_vertices.append(smaller_vertex)
    # Return the smaller vertices and the original faces
    return smaller_vertices, faces


def generate_smaller_obj(obj_file_path, smaller_obj_file_path):
    # Read the .obj file
    vertices, faces = read_obj_file(obj_file_path)
    # Create a smaller version of the object
    smaller_vertices = create_smaller_obj_vertices(vertices, faces)
    # Write the smaller .obj file
    write_obj_file(smaller_obj_file_path, smaller_vertices, faces)


def merge_vertices(vertices_original, vertices_smaller):
    merged_vertices = []
    for vertices in vertices_original:
        merged_vertices.append(vertices)
    for vertices in vertices_smaller:
        merged_vertices.append(vertices)

    return merged_vertices


def create_tetrahedron(vertices_original, faces_original):
    tetrahedron_pairs = []
    vertices_length = len(vertices_original)
    for i in range(len(faces_original)):
        face_original = faces_original[i]
        if len(faces_original[i]) == 3:
            tetrahedron_pairs.append(
                [
                    face_original[0],
                    face_original[1],
                    face_original[2],
                    face_original[0] + vertices_length,
                ]
            )
            tetrahedron_pairs.append(
                [
                    face_original[0] + vertices_length,
                    face_original[1] + vertices_length,
                    face_original[2] + vertices_length,
                    face_original[1],
                ]
            )
            tetrahedron_pairs.append(
                [
                    face_original[1],
                    face_original[2],
                    face_original[2] + vertices_length,
                    face_original[0] + vertices_length,
                ]
            )

        if len(faces_original[i]) > 3:
            # 1,2,3
            tetrahedron_pairs.append(
                [
                    face_original[0],
                    face_original[1],
                    face_original[2],
                    face_original[0] + vertices_length,
                ]
            )
            tetrahedron_pairs.append(
                [
                    face_original[0] + vertices_length,
                    face_original[1] + vertices_length,
                    face_original[2] + vertices_length,
                    face_original[1],
                ]
            )
            tetrahedron_pairs.append(
                [
                    face_original[1],
                    face_original[2],
                    face_original[2] + vertices_length,
                    face_original[0] + vertices_length,
                ]
            )

            # 1,3,4
            tetrahedron_pairs.append(
                [
                    face_original[0],
                    face_original[2],
                    face_original[3],
                    face_original[0] + vertices_length,
                ]
            )
            tetrahedron_pairs.append(
                [
                    face_original[0] + vertices_length,
                    face_original[2] + vertices_length,
                    face_original[3] + vertices_length,
                    face_original[2],
                ]
            )
            tetrahedron_pairs.append(
                [
                    face_original[2],
                    face_original[3],
                    face_original[3] + vertices_length,
                    face_original[0] + vertices_length,
                ]
            )

    return tetrahedron_pairs


def write_msh_file(file_path, vertices, tetrahedrons):
    # Open the .msh file for writing
    with open(file_path, "w") as file:
        file.write("$NOD\n")
        # Write the number of vertices
        file.write(f"{len(vertices)}\n")
        # Write the vertices to the file
        for i, vertex in enumerate(vertices):
            file.write(str(i + 1) + " " + f"{' '.join(map(str, vertex))}\n")

        file.write("$ENDNOD\n")
        # Write the tetrahedrons to the file
        file.write("$ELM\n")
        # Write the number of tetrahedrons
        file.write(f"{len(tetrahedrons)}\n")
        for i, tetrahedron in enumerate(tetrahedrons):
            file.write(
                str(i + 1)
                + " 4 1 1 4 "
                + f"{' '.join(map(str, [index + 1 for index in tetrahedron]))}\n"
            )

        file.write("$ENDELM\n")
        # Write the end of the file


def generate_msh_file(obj_file_path, msh_file_path):
    # Read the .obj file
    vertices, faces = read_obj_file(obj_file_path)
    # Create a smaller version of the object
    smaller_vertices = create_smaller_obj_vertices(vertices, faces)
    # Merge the original and smaller vertices
    merged_vertices = merge_vertices(vertices, smaller_vertices)
    # Create tetrahedrons from the faces
    tetrahedrons = create_tetrahedron(vertices, faces)
    # Write the .msh file
    write_msh_file(msh_file_path, merged_vertices, tetrahedrons)


def write_obj_file(file_path, vertices, faces):
    # Open the .obj file for writing
    with open(file_path, "w") as file:
        # Write the vertices to the file
        for vertex in vertices:
            file.write(f"v {' '.join(map(str, vertex))}\n")
        # Write the faces to the file
        for face in faces:
            file.write(f"f {' '.join(map(str, [index + 1 for index in face]))}\n")


if __name__ == "__main__":
    path = ""
    if len(sys.argv) < 2:
        print("Please provide the path to the .obj file")
        sys.exit(1)

    path = sys.argv[1]

    if not path.endswith(".obj"):
        print("Please provide a valid .obj file")
        sys.exit(1)
    try:
        generate_smaller_obj(path, path.replace(".obj", "_smaller.obj"))
        # generate_msh_file(path, path.replace(".obj", ".msh"))
    except FileNotFoundError:
        print(f"File not found: {path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
