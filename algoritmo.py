def segmentar_oracion(oracion, diccionario):
    n = len(oracion)
    conjunto_diccionaria = set(diccionario)
 
    lista_encontrada = [list()] * (n + 1)
    lista_encontrada[0] = []

    for i in range(1, n + 1):
        for j in range(i):
            palabra = oracion[j:i] 
            if palabra in conjunto_diccionaria:
                lista_encontrada[i] = lista_encontrada[j] + [palabra]
                print(lista_encontrada[i], "\n")
                break
 
    return lista_encontrada[n]
