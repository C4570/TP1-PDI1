import cv2
import numpy as np
import matplotlib.pyplot as plt

"""Hacer una funcion para todos los formularios, por tema de ir debugeando y testeando la dejamos para lo ultimo"""
# formularios = ['formulario_01.png', 'formulario_02.png','formulario_03.png','formulario_04.png','formulario_05.png', 'formulario_vacio.png']
# for form in formularios

form = 'formulario_01'
img = cv2.imread(f"{form}.png",cv2.IMREAD_GRAYSCALE) 
img.shape
#Binarizamos la imagen con un Threshold de 128
th = 128
img_th = img<th
plt.imshow(img_th, cmap='gray'), plt.show()

#Sumarizamos los pixeles que son 1 en el eje x para detectar las columnas
img_cols = np.sum(img_th,axis=0)
print(img_cols)

#Sumarizamos los pixeles que son 1 en el eje y para detectar las filas
img_rows = np.sum(img_th,axis=1)

#Definimos un threshold del 80% para detectar filas y columnas
th_rows = img_rows.max() * 0.8
th_cols = img_cols.max() * 0.6

#Definimos nuestros arrays boolenos para detectar filas y columnas
img_rows_th = img_rows>th_rows
img_cols_th = img_rows>th_cols

#Los usamos para detectar filas y columnas respectivamente
rows_detected = np.where(img_rows > th_rows)[0]

cols_detected = np.where(img_cols > th_cols)[0]

# Visualizamos la imagen y las filas y columnas detectadas
plt.imshow(img_th, cmap='gray')

# Dibujar líneas horizontales en rojo para las filas
for row in rows_detected:
    plt.axhline(y=row, color='r', linestyle='-')

# Dibujar líneas verticales en azul para las columnas
for col in cols_detected:
    plt.axvline(x=col, color='b', linestyle='-')
plt.show()

renglones = []
for i in range(len(rows_detected) - 1):
    start_row = rows_detected[i]
    end_row = rows_detected[i + 1]

    for j in range(len(cols_detected) - 1):
        start_col = cols_detected[j]
        end_col = cols_detected[j + 1]

        # Extraer la subimagen (casilla)
        casilla = img_th[start_row:end_row, start_col:end_col]
        renglones.append(casilla)

len(renglones)

#Me armo un diccionario con las "subimagenes", categorizandolas en "Encabezados", "Categoria", "respuesta de la categoria"
diccionario_formulario = {}
diccionario_formulario["Encabezado"] = renglones[1]
diccionario_formulario["Encabezadoo"] = renglones[0]
for i in range(2, len(renglones), 2):
    categoria = renglones[i]
    respuesta = renglones[i + 1]
    
    
    if i == 2:
        diccionario_formulario["Nombre y apellido"] = categoria
        diccionario_formulario["Respuesta nombre y apellido"] = respuesta
    elif i == 4:
        diccionario_formulario["Edad"] = categoria
        diccionario_formulario["Respuesta edad"] = respuesta
    elif i == 6:
        diccionario_formulario["Mail"] = categoria
        diccionario_formulario["Respuesta mail"] = respuesta
    elif i == 8:
        diccionario_formulario["Legajo"] = categoria
        diccionario_formulario["Respuesta legajo"] = respuesta
    elif i == 12:
        diccionario_formulario["Pregunta 1"] = categoria
        diccionario_formulario["Respuesta 1"] = respuesta
    elif i == 14:
        diccionario_formulario["Pregunta 2"] = categoria
        diccionario_formulario["Respuesta 2"] = respuesta
    elif i == 16:
        diccionario_formulario["Pregunta 3"] = categoria
        diccionario_formulario["Respuesta 3"] = respuesta
    elif i == 18:
        diccionario_formulario["Comentarios"] = categoria
        diccionario_formulario["Respuesta Comentario"] = respuesta


for i, (key, casilla) in enumerate(diccionario_formulario.items()):
    plt.subplot(10,2,i+1)
    plt.imshow(casilla, cmap='gray')    
    plt.title(key)
plt.tight_layout()
plt.show()
"""Esto es lo mismo que esta abajo pero es para visualizar las letras que va detectando. Recomiendo probarlo"""
# letras = []
# for ir, renglon in enumerate(renglones):
#     # Aplicar umbralización en el renglón
#     reng_uint8 = np.uint8(renglon)

#     _, renglon_binary = cv2.threshold(reng_uint8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#     # Detección de componentes conectadas en el renglón binarizado
#     num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(renglon_binary, 8, cv2.CV_32S)

#     # Filtrar componentes conectadas por tamaño (ajusta th_area según tus necesidades)
#     th_area = 50
#     filtered_stats = stats[stats[:, -1] > th_area]

#     # Mostrar componentes conectadas detectadas en el renglón
#     for i, stat in enumerate(filtered_stats):
        
#         x, y, w, h, area = stat
#         letra = renglon[y:y+h, x:x+w]  # Recorta la letra
#         letras.append(letra)

#     # Visualizar la letra individual (puedes ajustar el tamaño de la figura)
#     plt.figure(figsize=(2, 2))
#     plt.imshow(letra, cmap='gray')
#             # Dibujar un rectángulo alrededor de la letra
#     plt.title(f"Renglón {ir+1}, Letra {i+1}")
#     plt.show()

letras_por_renglon = {}  # Diccionario para almacenar la cantidad de letras por renglón
letras = []
for i, (key, casilla) in enumerate(diccionario_formulario.items()):
    # Aplicar umbralización en el renglón
    reng_uint8 = np.uint8(casilla)
    _, renglon_binary = cv2.threshold(reng_uint8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Detección de componentes conectadas en el renglón binarizado
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(renglon_binary, 8, cv2.CV_32S)

    # Filtrar componentes conectadas por tamaño (ajusta th_area según tus necesidades)
    th_area = 50
    filtered_stats = stats[stats[:, -1] > th_area]

    # Almacenar la cantidad de letras detectadas en el renglón actual
    
    for i, stat in enumerate(filtered_stats):
        
        x, y, w, h, area = stat
        letra = renglon_binary[y:y+h, x:x+w]  # Recorta la letra
        letras.append(letra) 
    letras_por_renglon[f"{key}"] = len(filtered_stats)

print(letras_por_renglon)

#Funcion que chequea si las casillas cumplen las reglas

def cumple_reglas(letras_por_renglon, respuesta):
    longitud = int(letras_por_renglon[respuesta])
    if respuesta == "Respuesta nombre y apellido":
        return 1 <= longitud <= 25
    elif respuesta == "Respuesta edad":
        return 4 >= longitud > 1 #falta verificar que sean 2 palabras
    elif respuesta == "Respuesta mail":
        return longitud < 29 #Falta chequear que sea 1 palabra
    elif respuesta == "Respuesta legajo":
        return longitud < 11 #Falta chequear que sea 1 palabra
    elif respuesta in ['Respuesta 1', 'Respuesta 2', 'Respuesta 3']:
        return longitud == 3
    elif respuesta == "Respuesta Comentario":
        return 3 <= longitud <= 27

diccionario_respuestas = {
    'Nombre y apellido': 'Respuesta nombre y apellido',
    'Edad': 'Respuesta edad',
    'Mail': 'Respuesta mail',
    'Legajo': 'Respuesta legajo',
    'Pregunta 1': 'Respuesta 1',
    'Pregunta 2': 'Respuesta 2',
    'Pregunta 3': 'Respuesta 3',
    'Comentarios': 'Respuesta Comentario'
}

def devolucion(diccionario_respuestas):
    informe = {}
    for key, value in diccionario_respuestas.items():
        if cumple_reglas(letras_por_renglon, value):
            informe[key] = "OK"
        else:
            informe[key] = "MAL"
    print(f"Resultado {form}")    
    for key, value in informe.items():
        print(f"'{key}' : {value}")



devolucion(diccionario_respuestas)



















def imshow(img, new_fig=True, title=None, color_img=False, blocking=False, colorbar=True, ticks=False):
    if new_fig:
        plt.figure()
    if color_img:
        plt.imshow(img)
    else:
        plt.imshow(img, cmap='gray')
    plt.title(title)
    if not ticks:
        plt.xticks([]), plt.yticks([])
    if colorbar:
        plt.colorbar()
    if new_fig:        
        plt.show(block=blocking)














connectivity = 8
# Itera a través del diccionario y procesa las respuestas (elementos impares).
for i, (key, casilla) in enumerate(diccionario_formulario.items()):
    if i % 2 != 0:  # Verifica si el índice es impar (respuesta
        casilla_uint8 = np.uint8(casilla)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(casilla_uint8, connectivity, cv2.CV_32S)

        # Filtra las estadísticas para eliminar componentes conectadas con áreas pequeñas
        th_area = 10  # Ajusta este valor según tus necesidades
        ix_area = stats[:, -1] > th_area
        stats_filtradas = stats[ix_area, :]

        # Verifica requisitos específicos (al menos 2 palabras y no más de 25 caracteres)
        for stat in stats_filtradas:
            left, top, width, height, area = stat  # Extraer información de la componente conectada
            componente_conectada = casilla[top:top + height, left:left + width]

            # Realiza el procesamiento y verificación de requisitos aquí
            # Por ejemplo, contar palabras y verificar la longitud
            print(componente_conectada)  # Reemplaza con tu lógica de procesamiento
            imshow(img=labels)
            break
            # Verificar requisitos
            palabras = texto.split()
            if len(palabras) >= 2 and len(texto) <= 25:
                print(f"Respuesta válida en {key}: {texto}")
            else:
                print(f"Respuesta no válida en {key}: {texto}")

            # Puedes resaltar la región de texto válida en la imagen si lo deseas.
            if len(palabras) >= 2 and len(texto) <= 25:
                x, y, w, h = left, top, width, height
                casilla = cv2.rectangle(casilla, (x, y), (x + w, y + h), (0, 255, 0), 2)

        imshow(casilla, title=f'Respuesta: {key}')
        
input()