from algoritmo import segmentar_oracion
from utils import wrapper_leer_archivo

if __name__ == "__main__":
    oraciones, diccionario = wrapper_leer_archivo("200", "gigante")
    print(segmentar_oracion(oraciones[1], diccionario))