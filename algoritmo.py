
def procesar_texto(oraciones, diccionario):
    """
    Procesa una lista de oraciones y un diccionario, y devuelve una lista de oraciones segmentadas.
    :param oraciones: Lista de oraciones a procesar.
    :param diccionario: Diccionario utilizado para la segmentación.
    """
    resultado = []


    for oracion in oraciones:
        oracion_segmentada = segmentar_oracion(oracion, diccionario)

        if len("".join(oracion_segmentada)) < len(oracion):
            resultado.append("No es un mensaje")
        else:
            resultado.append(" ".join(oracion_segmentada))

    return resultado


def segmentar_oracion(oracion, diccionario):
    n = len(oracion)
    conjunto_diccionario = set(diccionario)
    max_long_palabra = max(len(palabra) for palabra in diccionario)

    existencia_parcial = [False] * (n + 1)
    existencia_parcial[0] = True
    path = [None] * (n + 1)

    for i in range(1, n + 1):
        for j in range(max(0, i - max_long_palabra), i):
            if existencia_parcial[j] and oracion[j:i] in conjunto_diccionario:
                existencia_parcial[i] = True
                path[i] = (j, oracion[j:i])
                break

    if not existencia_parcial[n]:
        return []

    return reconstruir_segmentacion(path, n)


def reconstruir_segmentacion(path, n):
    """
    Reconstruye la segmentación de una oración a partir del camino dado.
    :param path: Lista de tuplas que representan el camino de segmentación.
    :param n: Longitud de la oración original.
    :return: Lista de palabras segmentadas.
    """
    resultado = []
    idx = n
    while idx > 0:
        j, palabra = path[idx]
        resultado.append(palabra)
        idx = j

    return resultado[::-1]