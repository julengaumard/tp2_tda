

# palabras = ['hambre', 'tengo', 'yo', 'increible']
# frase = "yotengohambreyoquierocomer"

# def obtener_palabras(palabras, frase):

#     matriz = [[0 for _ in range(len(palabras))] for _ in range(len(frase))]

#     for p in range(1,len(frase)):
#         # contador = 0
#         # largo = len(palabras[p])

#         letra = frase[p]

#         for w in range(0,len(palabras)):

            

#             if frase[p] == palabras[w][matriz[p-1][w]]:
#                 matriz[p][w] = matriz[p-1][w] + 1
                
                

#             # if contador < largo and frase[w-1] == palabras[p][contador]:
#             #     matriz[p][w] = max(matriz[p][w-1] + 1, matriz[p-1][-1] + 1)
#             #     contador += 1
 
#             # else:
#             #     matriz[p][w] = max(matriz[p][w-1], matriz[p-1][-1])
#             #     contador = 0
            


#     return matriz








# re = obtener_palabras(palabras, frase)
# for l in range(len(re)):
#     print(frase[l], re[l])
  
# for l in re:
#     print(l)
 
# print(list(frase))







# def obtener_palabras(palabras, frase):

#     matriz = [[0 for _ in range(len(frase))] for _ in range(len(palabras))]

#     for p in range(len(palabras)):
#         contador = 0
#         largo = len(palabras[p])


#         for w in range(1,len(frase)):
#             if contador < largo and frase[w-1] == palabras[p][contador]:
#                 matriz[p][w] = max(matriz[p][w-1] + 1, matriz[p-1][-1] + 1)
#                 contador += 1
 
#             else:
#                 matriz[p][w] = max(matriz[p][w-1], matriz[p-1][-1])
#                 contador = 0

#     return matriz


# def segmentar_oracion(oracion, diccionario):
#     n = len(oracion)
#     dp = [(None,0)] * (n + 1)
#     dp[0] = (None,0)

#     print(dp)

#     for i in range(1, n + 1):

#         ultima = dp[i-1][1]
 
        

#         palabra = oracion[ultima:i]

#         print(palabra)
        
#         if palabra in diccionario:

#             lista_encontrada = [palabra]
#             if dp[i-1][0] != None:
#                 lista_encontrada += dp[i-1][0]

#             dp[i] = (lista_encontrada, dp[i-1][1] + len(palabra))
             
#         print(dp[i])


#     return dp[n]

 
# Ejemplo de uso:
 

# diccionario = [ "es", "una", "prueba", "de", "segmentacion", "esto", "este", 'robot']
# oracion = "estoesunapruebadeessegmentacion"

# print(diccionario)
# print(oraciones[1]) 

# print(segmentar_oracion("estoesunapruebadeessegmentacion", [ "es", "una", "prueba", "de", "segmentacion", "esto", "este", 'robot']))

# tenemos que guardar, todos, no podemos hacer optimizacion, ya que no sabemos, al obtener una nueva letra que palabra vamos a poder generar y a que iteracion tenemos que retroceder para combinarlo.

