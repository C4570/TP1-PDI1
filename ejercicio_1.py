import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('Imagen_con_detalles_escondidos.tif', cv2.IMREAD_GRAYSCALE)

def ecualizacion_local_hist(imagen, ventana_tamaño):
    ancho, largo = imagen.shape
    resultado_img = np.zeros_like(imagen)

    for y in range(ancho):
        for x in range(largo):
            x_min = max(0, x - ventana_tamaño // 2) #calcula la coordenada horizontal minima para la ventana, si es menor  a 0 toma 0
            x_max = min(largo, x + ventana_tamaño // 2 + 1) # calcula la coordenada horizontal maxima de la ventana, si es mayor al ancho establece el ancho de la imagen.
            y_min = max(0, y - ventana_tamaño // 2)
            y_max = min(ancho, y + ventana_tamaño // 2 + 1)

            ventana = imagen[y_min:y_max, x_min:x_max] #extrae la ventana usando las coordenadas
            hist = cv2.calcHist([ventana], [0], None, [256], [0, 256]) #calcula el histograma de la ventana
            hist_equalizado = cv2.equalizeHist(ventana) #aplica la ecualizacion, ajusta las intensidades para mejorar el contraste

            resultado_img[y, x] = hist_equalizado[y - y_min, x - x_min] #asigna el valor ecualizado al pixel, ajusta las coordenadas con la posicion de la ventana

    return resultado_img


ventana_tamaño = 35

# Aplicamos la ecualización local del histograma
resultado = ecualizacion_local_hist(img, ventana_tamaño)

# Mostramos la imagen original y la procesada
plt.subplot(121)
h = plt.imshow(img, cmap='gray')
plt.colorbar(h)
plt.title('Imagen original')
plt.subplot(122)
h = plt.imshow(resultado, cmap='gray')
plt.colorbar(h)
plt.title('Imagen procesada')
plt.show()
