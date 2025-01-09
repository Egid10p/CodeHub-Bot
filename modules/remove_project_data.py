import json


def remove_project(project_id):
    # Load the JSON from the file or wherever you get it from
    # Cargar el JSON desde el archivo o de donde lo obtengas
    with open("data_projects.json", "r") as f:
        data = json.load(f)

    # Check if the project number is valid
    # Verificar si el número del proyecto es válido
    if 1 <= project_id <= len(data["projects"]):
        # Borrar el proyecto de la lista
        delete_project = data["projects"].pop(project_id - 1)

        # Save changes back to file
        # Guardar los cambios de nuevo en el archivo
        with open("data_projects.json", "w") as f:
            json.dump(data, f, indent=4)

        return f"Proyecto {project_id} borrado exitosamente:\n{delete_project}"
    else:
        return "Número de proyecto no válido."
