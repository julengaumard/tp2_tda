from random import randint
from tests.generador import Generador
from algoritmo import procesar_texto

def procesar_texto_explicativo(oraciones, diccionario):

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
        print(f"\n--- Iniciando segmentación de: '{oracion}' ---")
        n = len(oracion)
        conjunto_diccionario = set(diccionario)
        max_long_palabra = max(len(palabra) for palabra in diccionario)
        print(f"Longitud máxima de palabra en diccionario: {max_long_palabra}")

        existencia_parcial = [False] * (n + 1)
        existencia_parcial[0] = True
        path = [None] * (n + 1)

        for i in range(1, n + 1):
            print(f"\nAnalizando posición {i}:")
            for j in range(max(0, i - max_long_palabra), i):
                subcadena = oracion[j:i]
                if existencia_parcial[j] and subcadena in conjunto_diccionario:
                    print(f"  Encontrada palabra válida: '{subcadena}' en posición {j}-{i}")
                    existencia_parcial[i] = True
                    path[i] = (j, subcadena)
                    break


        if not existencia_parcial[n]:
            print("No se encontró una segmentación válida para la oración")
            return []

        return reconstruir_segmentacion(path, n)

    def reconstruir_segmentacion(path, n):
        """
        Reconstruye la segmentación de una oración a partir del camino dado.
        :param path: Lista de tuplas que representan el camino de segmentación.
        :param n: Longitud de la oración original.
        :return: Lista de palabras segmentadas.
        """
        print("\nReconstruyendo segmentación:")
        resultado = []
        idx = n
        while idx > 0:
            j, palabra = path[idx]
            print(f"  Agregando palabra: '{palabra}'")
            resultado.append(palabra)
            idx = j

        return resultado[::-1]

    return procesar_texto(oraciones, diccionario)

def test_procesar_texto():
    print("\n=== INICIANDO TEST DE PROCESAMIENTO DE TEXTO ===")
    gen = Generador(1000)
    diccionario = gen.diccionario
    oraciones = gen.generar_oraciones(randint(1, 1), randint(1, 4))

    print("\nOraciones generadas:")
    for oracion in oraciones:
        print(f"- {oracion}")
    print("\nResultados del procesamiento:")
    resultados = procesar_texto_explicativo(oraciones, diccionario)
    for oracion, resultado in zip(oraciones, resultados):
        print(f"Oración: {oracion} -> Resultado: {resultado}")
