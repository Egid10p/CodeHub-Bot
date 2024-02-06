import json

# Función para actualizar un proyecto específico en el archivo JSON
def actualizar(proyecto_id: int, nombre_nuevo: str, descripcion_nueva: str, repositorio_nuevo: str, estado_nuevo: str):
    # Ruta del archivo JSON que contiene la información de los proyectos
    ruta_archivo = "data_proyectos.json"
    proyecto_id = int(proyecto_id)

    # Cargar el JSON en modo lectura y escritura
    with open(ruta_archivo, 'r+') as archivo:
        # Cargar los proyectos desde el archivo JSON
        proyectos_json = json.load(archivo)

        # Modificar el proyecto específico si el ID es válido
        if proyecto_id <= len(proyectos_json["proyectos"]):
            # Actualizar las propiedades del proyecto
            proyectos_json["proyectos"][proyecto_id - 1]["nombre"] = nombre_nuevo
            proyectos_json['proyectos'][proyecto_id - 1]['descripcion'] = descripcion_nueva
            proyectos_json['proyectos'][proyecto_id - 1]['repositorio'] = repositorio_nuevo
            proyectos_json['proyectos'][proyecto_id - 1]['estado'] = estado_nuevo

            # Mover el puntero al inicio del archivo
            archivo.seek(0)

            # Truncar el archivo para eliminar el contenido existente
            archivo.truncate()

            # Convertir de nuevo a JSON y escribir en el archivo
            json.dump(proyectos_json, archivo, indent=2)

            # Indicar que la actualización fue exitosa
            return True
        else:
            # Indicar que el ID de proyecto no es válido
            return False
