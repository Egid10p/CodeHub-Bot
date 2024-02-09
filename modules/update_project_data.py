import json

# Function to update a specific project in the JSON file
# Función para actualizar un proyecto específico en el archivo JSON
def update(project_id: int, new_name: str, new_description: str, new_state: str, new_repository: str):
    # Path to the JSON file containing project information
    # Ruta del archivo JSON que contiene la información de los proyectos
    file_path = "data_projects.json"
    project_id = int(project_id)

    # Load the JSON in read and write mode
    # Cargar el JSON en modo lectura y escritura
    with open(file_path, 'r+') as file:
        # Load the projects from the JSON file
        # Cargar los proyectos desde el archivo JSON
        project_json = json.load(file)

        # Modify the specific project if the ID is valid
        # Modificar el proyecto específico si el ID es válido
        if project_id <= len(project_json["projects"]):
            # Update the project properties
            # Actualizar las propiedades del proyecto
            project_json["projects"][project_id - 1]["name"] = new_name
            project_json['projects'][project_id - 1]['description'] = new_description
            project_json['projects'][project_id - 1]['state'] = new_state
            project_json['projects'][project_id - 1]['repository'] = new_repository

            # Move the pointer to the beginning of the file
            # Mover el puntero al inicio del archivo
            file.seek(0)

            # Truncate the file to remove existing content
            # Truncar el archivo para eliminar el contenido existente
            file.truncate()

            # Convert back to JSON and write to the file
            # Convertir de nuevo a JSON y escribir en el archivo
            json.dump(project_json, file, indent=2)

            # Indicate that the update was successful
            # Indicar que la actualización fue exitosa
            return True
        else:
            # Indicate that the project ID is not valid
            # Indicar que el ID de proyecto no es válido
            return False

