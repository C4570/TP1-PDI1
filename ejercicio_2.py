import cv2
import numpy as np
import matplotlib.pyplot as plt

#Funcion Principal
def deteccion(form):
    
    img = cv2.imread(f"{form}.png",cv2.IMREAD_GRAYSCALE) 
    img.shape
    #Binarizamos la imagen con un Threshold de 128 <-- porque de 128 y no otro numero?
    th = 128 # 128 esta por encima de los dos valores por eso detecta ambos y por consiguiente se crean la row 497 y 498
    img_th = img<th # Porque menor a 128 y no mayor a 128?
    # "Visualizamos el formulario Binarizado"
    #plt.imshow(img_th, cmap='gray'), plt.show()

    #Sumarizamos los pixeles que son 1 en el eje x para detectar las columnas
    img_cols = np.sum(img_th,axis=0)
    # print(img_cols)

    #Sumarizamos los pixeles que son 1 en el eje y para detectar las filas
    img_rows = np.sum(img_th,axis=1)

    #Definimos un threshold del 80% para detectar filas y columnas <-- porque del 80% y no otro porcentaje?
    th_rows = img_rows.max() * 0.8 # Si subis a 90% o bajas a 70% o 60% sigue funcionando
    th_cols = img_cols.max() * 0.6 # Esto es 60% no 80% porque?

    #Los usamos para detectar filas y columnas respectivamente
    rows_detected = np.where(img_rows > th_rows)[0]

    cols_detected = np.where(img_cols > th_cols)[0]

    # Visualizamos la imagen y las filas y columnas detectadas
    plt.imshow(img_th, cmap='gray')

    # Dibujar líneas horizontales en rojo para las filas
    for row in rows_detected: # Si hacemos print(len(rows_detected)) no dice que tiene 12 pero cuando se muestra 
                              # la imagen solo hay 11 linea rojas? Si hacemos print(rows_detected) nos devuelve 
                              # [ 21  61 101 141 181 221 261 301 341 381 497 498], hay un espacio de mas entre el 21 y 61 eso podria ser el causante 
        plt.axhline(y=row, color='r', linestyle='-')
        
    # Dibujar líneas verticales en azul para las columnas
    for col in cols_detected:
        plt.axvline(x=col, color='b', linestyle='-')
    plt.show()

    renglones = []
    for i in range(len(rows_detected) - 1): # Esta va de 0 a 11 en vez de 0 a 10 porque rows_detected tiene 12 elementos en vez de tener 11. 
                                            # Deberiamos o poner - 2 o arrglar lo de rows_detected
        start_row = rows_detected[i]        # Si el obejtivo es buscar un par de casillas para definir un inicio y un final y se quiere excluir
                                            # la ultima row_detected deveria ser:
        end_row = rows_detected[i + 1]      #               - 1 para recorrer de 0 hasta la ultima para evitar un error de índice fuera de rango en la línea
                                            #               - 2 para evitar llegar a la ultima 

        for j in range(len(cols_detected) - 1):
            start_col = cols_detected[j]
            end_col = cols_detected[j + 1]

            # Extraer la subimagen (casilla)
            casilla = img_th[start_row:end_row, start_col:end_col]
            renglones.append(casilla)


    # Armamos un diccionario con las "subimagenes", categorizandolas en "Encabezados", "Categoria", "respuesta de la categoria"
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
        plt.title(key, fontsize=12)
        plt.subplots_adjust(wspace=0.1, hspace=1.5)
    plt.tight_layout()
    plt.show()

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

    # Crear una figura y un eje en matplotlib
    fig, ax = plt.subplots()

    # Convertir el diccionario a una cadena y mostrarla en el eje
    textstr = '\n'.join([f'{k}: {v}' for k, v in letras_por_renglon.items()])
    ax.text(0.5, 0.5, textstr, fontsize=12, ha='center', va='center')

    # Ocultar los ejes
    ax.axis('off')

    # Mostrar la figura
    plt.show()
    return letras_por_renglon

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

#Evalua las respuestas y devuelve "OK" o "MAL"
def devolucion(respuestas, form):
    informe = {}
    diccionario_respuestas = {
    'Nombre y apellido': 'Respuesta nombre y apellido',
    'Edad': 'Respuesta edad',
    'Mail': 'Respuesta mail',
    'Legajo': 'Respuesta legajo',
    'Pregunta 1': 'Respuesta 1',
    'Pregunta 2': 'Respuesta 2',
    'Pregunta 3': 'Respuesta 3',
    'Comentarios': 'Respuesta Comentario'}
    for key, value in diccionario_respuestas.items():
        if cumple_reglas(respuestas, value):
            informe[key] = "OK"
        else:
            informe[key] = "MAL"
    print(f"Resultado {form}")    
    for key, value in informe.items():
        print(f"'{key}' : {value}")


#--------------------- PROGRAMA -------------------
def main():
    formularios = ['formulario_01', 'formulario_02','formulario_03','formulario_04','formulario_05', 'formulario_vacio']
    for form in formularios:
        respuestas = deteccion(form)
        devolucion(respuestas, form)
    input()
    
main()