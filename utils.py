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


def parsear_resultados(path):
    """
    Extrae los casos de prueba de un archivo de texto.
    Busca patrones como 'Palabras: file1.txt, entrada: file2.txt'
    """
    casos = []

    with open(path, 'r', encoding='utf-8') as f:
        contenido = f.read()

    patron = r'Palabras:\s*([^,\s]+),\s*entrada:\s*([^\s]+)'
    matches = re.finditer(patron, contenido)

    for match in matches:
        palabras_file = match.group(1)
        entrada_file = match.group(2)

        caso = {
            "palabras": f"casos/{palabras_file}",
            "entrada": f"casos/{entrada_file}",
            "mensajes": []
        }
        casos.append(caso)

    return casos


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