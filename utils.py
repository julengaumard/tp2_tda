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

def wrapper_leer_archivo(nombre_base, dicc):
    archivo_in = f"casos/{nombre_base}_in.txt"
    archivo_out = f"casos/{dicc}.txt"
    resultado_in = leer_archivo_como_list(archivo_in)
    resultado_out = leer_archivo_como_list(archivo_out)
    return resultado_in, resultado_out
