import unittest
from algoritmo import procesar_texto
from utils import wrapper_leer_archivo
from casos import test_procesar_texto


def main(argc, argv):
    """
    Función principal que ejecuta el programa.
    :param argc: Número de argumentos de la línea de comandos.
    :param argv: Lista de argumentos de la línea de comandos.
    """
    if argc == 2:
        if argv[1] == "test":
            loader = unittest.TestLoader()
            tests = loader.discover('./tests', pattern='test_*.py')
            test_runner = unittest.TextTestRunner()
            test_runner.run(tests)
            sys.exit(0)

        if argv[1] == "ejemplo":
            test_procesar_texto()
            sys.exit(0)

        print("Uso: python tp2.py test")
        print("Uso: python tp2.py <archivo_oraciones> <archivo_diccionario>")
        return

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
