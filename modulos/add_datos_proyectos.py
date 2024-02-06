import json

# Función para añadir un nuevo proyecto al archivo JSON
def añadir_proyecto(nombre: str, descripcion: str, repositorio: str, estado: str):
    # Verifica que todos los valores sean cadenas no vacías
    if all(isinstance(valor, str) and valor.strip() != "" for valor in [nombre, descripcion, repositorio, estado]):
        # Ruta al archivo JSON que contiene la información de los proyectos
        ruta_archivo = 'data_proyectos.json'

        # 1. Lee el contenido actual del archivo JSON
        with open(ruta_archivo, 'r') as archivo:
            datos_actuales = json.load(archivo)

        # 2. Modifica los datos según sea necesario (agregar un nuevo proyecto)
        nuevo_proyecto = {
            "nombre": nombre,
            "descripcion": descripcion,
            "repositorio": repositorio,
            "estado": estado
        }

        # Agrega el nuevo proyecto a la lista de proyectos
        datos_actuales["proyectos"].append(nuevo_proyecto)

        # 3. Escribe los datos actualizados en el mismo archivo
        with open(ruta_archivo, 'w') as archivo:
            json.dump(datos_actuales, archivo, indent=4)

        # Indicar que la operación fue exitosa
        return True
    else:
        # Indicar que al menos uno de los valores no es válido
        return False
