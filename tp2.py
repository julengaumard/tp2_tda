from algoritmo import procesar_texto
from utils import wrapper_leer_archivo


def main(argc, argv):
    """
    Función principal que ejecuta el programa.
    :param argc: Número de argumentos de la línea de comandos.
    :param argv: Lista de argumentos de la línea de comandos.
    """
    if argc != 3:
        print("Uso: python tp2.py <archivo_oraciones> <archivo_diccionario>")
        return

    path_oraciones = argv[1]
    path_diccionario = argv[2]

    oraciones, diccionario = wrapper_leer_archivo(path_oraciones, path_diccionario)

    resultado = procesar_texto(oraciones, diccionario)

    for i, oracion in enumerate(resultado):
        print(f"Oración {i + 1}: {oracion}")


if __name__ == "__main__":
    import sys
    main(len(sys.argv), sys.argv)
