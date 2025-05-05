import random
import requests

MAX_LENGTH = 15

class Generador:
    def __init__(self, cantidad):
        self.todas_las_palabras = self.obtener_palabras_desde_url()
        self.diccionario = self.generar_diccionario_aleatorio(self.todas_las_palabras, cantidad)

    def obtener_palabras_desde_url(self):
        try:
            response = requests.get("https://raw.githubusercontent.com/JorgeDuenasLerin/diccionario-espanol-txt/refs/heads/master/0_palabras_todas.txt")
            response.raise_for_status()
            palabras = response.text.splitlines()
            return palabras

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener las palabras desde la URL: {e}")
            return []

    def generar_diccionario_aleatorio(self, url, cantidad):
        todas_las_palabras = Generador.obtener_palabras_desde_url(url)
        if not todas_las_palabras:
            return []
        return random.sample(todas_las_palabras, min(cantidad, len(todas_las_palabras)))

    def generar_oracion_valida(self, cantidad_palabras):
        if not self.diccionario:
            return ""
        palabras = [palabra for palabra in self.diccionario if len(palabra) <= MAX_LENGTH]
        oracion = [random.choice(palabras) for _ in range(cantidad_palabras)]
        return "".join(oracion)

    def generar_oracion_invalida(self):
        caracteres = "abcdefghijklmnopqrstuvwxyz"
        longitud = random.randint(5, 15)
        return "".join(random.choice(caracteres) for _ in range(longitud))

    def generar_oraciones(self, cantidad_oraciones, cantidad_palabras):
        oraciones = []
        for _ in range(cantidad_oraciones):
            if random.choice([True, False]):
                oracion = self.generar_oracion_valida(cantidad_palabras)
            else:
                oracion = self.generar_oracion_invalida()
            oraciones.append(oracion)
        return oraciones
