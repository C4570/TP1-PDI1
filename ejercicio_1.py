import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('Imagen_con_detalles_escondidos.tif', cv2.IMREAD_GRAYSCALE)

def ecualizacion_local_hist(imagen, ventana_tamaño):
    ancho, largo = imagen.shape
    resultado_img = np.zeros_like(imagen)

    # Agregar un borde a la imagen para manejar las ventanas cerca de los bordes
    borde = ventana_tamaño // 2
    imagen_con_borde = cv2.copyMakeBorder(imagen, borde, borde, borde, borde, cv2.BORDER_REPLICATE)

    for y in range(ancho):
        for x in range(largo):
            # Calculamos la coordenada horizontal mínima para la ventana, si es menor a 0 toma 0.
            x_min = max(0, x - ventana_tamaño // 2) 
            # Calculamos la coordenada horizontal máxima de la ventana, si es mayor al ancho establece el ancho de la imagen.
            x_max = min(largo, x + ventana_tamaño // 2 + 1)
            # Calculamos la coordenada vertical mínima para la ventana, si es menor a 0 toma 0.
            y_min = max(0, y - ventana_tamaño // 2)
            # Calculamos la coordenada vertical máxima de la ventana, si es mayor al alto establece el alto de la imagen.
            y_max = min(ancho, y + ventana_tamaño // 2 + 1)

            ventana = imagen_con_borde[y_min + borde:y_max + borde, x_min + borde:x_max + borde] #extrae la ventana usando las coordenadas
            hist = cv2.calcHist([ventana], [0], None, [256], [0, 256]) #calcula el histograma de la ventana
            hist_equalizado = cv2.equalizeHist(ventana) #aplica la ecualizacion, ajusta las intensidades para mejorar el contraste

            resultado_img[y, x] = hist_equalizado[y - y_min, x - x_min] #asigna el valor ecualizado al pixel, ajusta las coordenadas con la posicion de la ventana

    return resultado_img

# Elegimos algunas vemtanas para probar cual es mejor
ventana_tamaño1 = 30
ventana_tamaño2 = 10
ventana_tamaño3 = 20
ventana_tamaño4 = 50

# Ejecutamos la función con las ventanas elegidas y la imagen original
resultado30 = ecualizacion_local_hist(img, ventana_tamaño1)
resultado10 = ecualizacion_local_hist(img, ventana_tamaño2)
resultado20 = ecualizacion_local_hist(img, ventana_tamaño3)
resultado50 = ecualizacion_local_hist(img, ventana_tamaño4)

# Mostramos las diferentes imagenes generadas con las ventanas
plt.subplot(221)
h = plt.imshow(resultado10, cmap='gray')
plt.colorbar(h)
plt.title('Imagen ventana 10')
plt.subplot(222)
h = plt.imshow(resultado20, cmap='gray')
plt.colorbar(h)
plt.title('Imagen ventana 20')
plt.subplot(223)
h = plt.imshow(resultado30, cmap='gray')
plt.colorbar(h)
plt.title('Imagen ventana 30')
plt.subplot(224)
h = plt.imshow(resultado50, cmap='gray')
plt.colorbar(h)
plt.title('Imagen ventana 50')
plt.show()


# Mostramos la imagen original y la procesada
plt.subplot(121)
h = plt.imshow(img, cmap='gray')
plt.colorbar(h)
plt.title('Imagen original')
plt.subplot(122)
h = plt.imshow(resultado20, cmap='gray')
plt.colorbar(h)
plt.title('Imagen procesada')
plt.show()
