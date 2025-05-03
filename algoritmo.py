
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
    conjunto_diccionaria = set(diccionario)

    lista_encontrada = [[] for _ in range(n + 1)]
    lista_encontrada[0] = []

    for i in range(1, n + 1):
        for j in range(i):
            palabra = oracion[j:i]
            if palabra in conjunto_diccionaria:
                lista_encontrada[i] = lista_encontrada[j] + [palabra]
                # print(lista_encontrada[i], "\n")
                break

    return lista_encontrada[n]
