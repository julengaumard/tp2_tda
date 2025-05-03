import re

def leer_archivo_como_set(nombre_archivo):
    resultado = set()
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            resultado.add(linea.rstrip('\n'))
    return resultado


def leer_archivo_como_list(nombre_archivo):
    resultado = []
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            resultado.append(linea.rstrip('\n'))
    return resultado


def wrapper_leer_archivo(path_oraciones, path_diccionario):
    """
    Lee un archivo de oraciones y un archivo de diccionario, y devuelve su contenido como listas.
    :param path_oraciones: Ruta del archivo de oraciones.
    :param path_diccionario: Ruta del archivo de diccionario.
    """
    resultado_in    = leer_archivo_como_list(path_oraciones)
    resultado_out   = leer_archivo_como_list(path_diccionario)
    return resultado_in, resultado_out


# def parsear_resultados(path):
#     with open(path, 'r', encoding='utf-8') as f:
#         lineas = [line.strip() for line in f if line.strip()]

#     bloques = []
#     bloque_actual = None

#     for linea in lineas:
#         if linea.startswith("Palabras:") and "entrada:" in linea:

#             if bloque_actual:
#                 bloques.append(bloque_actual)

#             palabras_file = re.search(r"Palabras:\s*([^\s,]+)", linea).group(1)
#             entrada_file = re.search(r"entrada:\s*([^\s,]+)", linea).group(1)

#             bloque_actual = {
#                 "palabras": 'casos/' + palabras_file,
#                 "entrada": 'casos/' + entrada_file,
#                 "mensajes": []
#             }
#         else:
#             if bloque_actual is not None:
#                 bloque_actual["mensajes"].append(linea)

#     if bloque_actual:
#         bloques.append(bloque_actual)

#     return bloques


def parsear_resultados(path):
    with open(path, 'r', encoding='utf-8') as f:
        lineas = [line.strip() for line in f if line.strip()]

    bloques = []
    bloque_actual = None

    for linea in lineas:
        # Si encontramos un encabezado de bloque nuevo
        if linea.startswith("Palabras:") and "entrada:" in linea:
            # Si ya estábamos en un bloque anterior, lo guardamos
            if bloque_actual is not None:
                bloques.append(bloque_actual)

            palabras_file = re.search(r"Palabras:\s*([^\s,]+)", linea).group(1)
            entrada_file = re.search(r"entrada:\s*([^\s,]+)", linea).group(1)

            # Comenzamos un nuevo bloque
            bloque_actual = {
                "palabras": 'casos/' + palabras_file,
                "entrada": 'casos/' + entrada_file,
                "mensajes": []
            }

        # Si no es encabezado, agregamos la línea como mensaje al bloque actual
        elif bloque_actual is not None:
            bloque_actual["mensajes"].append(linea)

    # Guardamos el último bloque si existe
    if bloque_actual is not None:
        bloques.append(bloque_actual)

    return bloques



def performance(funcion):
    """
    Decorador para medir el tiempo de ejecución de una función.
    :param funcion: Función a medir.
    """
    import time

    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = funcion(*args, **kwargs)
        fin = time.time()
        print(f"Tiempo de ejecución: {fin - inicio:.4f} segundos")
        return resultado

    return wrapper