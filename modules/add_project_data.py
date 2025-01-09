import json


# Function to add a new project to the JSON file
# Función para añadir un nuevo proyecto al archivo JSON
def add_project_func(name: str, description: str, state: str, repository: str):

    # Verify that all values are non-empty strings
    # Verifica que todos los valores sean cadenas no vacías
    if all(
        isinstance(value, str) and value.strip() != ""
        for value in [name, description, repository, state]
    ):
        # Path to the JSON file containing project information
        # Ruta al archivo JSON que contiene la información de los proyectos
        file_path = "data_projects.json"

        # 1. Read the current content of the JSON file
        # 1. Lee el contenido actual del archivo JSON
        with open(file_path, "r") as file:
            current_data = json.load(file)

        # 2. Modify the data as needed (add a new project)
        # 2. Modifica los datos según sea necesario (agregar un nuevo proyecto)
        new_project = {
            "name": name,
            "description": description,
            "state": state,
            "repository": repository,
        }

        # Add the new project to the list of projects
        # Agrega el nuevo proyecto a la lista de proyectos
        current_data["projects"].append(new_project)

        # 3. Write the updated data to the same file
        # 3. Escribe los datos actualizados en el mismo archivo
        with open(file_path, "w") as file:
            json.dump(current_data, file, indent=4)

        # Indicate that the operation was successful
        # Indicar que la operación fue exitosa
        return True
    else:
        # Indicate that at least one of the values is not valid
        # Indicar que al menos uno de los valores no es válido
        return False
