from imaplib import ParseFlags
from unittest import TestCase
from utils import parsear_resultados, wrapper_leer_archivo
from algoritmo import procesar_texto


class TestCasos(TestCase):
    def setUp(self):
        self.respuestas = parsear_resultados("casos/Resultados Esperados.txt")

    def test_assert(self):
        self.assertEqual(1, 1)

    def test_casos(self):

        for i, respuesta in enumerate(self.respuestas):
            with self.subTest(i=i, msg="Archivo de entrada: " + respuesta["entrada"] + " y palabras: " + respuesta["palabras"]):
                palabras = respuesta["palabras"]
                entrada = respuesta["entrada"]
                mensajes = respuesta["mensajes"]

                print(f"Entrada: {entrada}")
                print(f"Diccionario: {palabras}")

                oraciones, diccionario = wrapper_leer_archivo(entrada, palabras)

                resultado = procesar_texto(oraciones, diccionario)

                for index, mensaje in enumerate(mensajes):
                    if mensaje == "No es un mensaje":
                        self.assertEqual(mensaje, resultado[index])
                    else:
                        self.assertNotEqual(resultado[index], "No es un mensaje")
