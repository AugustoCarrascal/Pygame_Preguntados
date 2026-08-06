"""
Módulo de dibujo de componentes visuales.
Se encarga de pintar botones, textos y sombreados en la pantalla física.
"""

import pygame
from configuracion.constantes import BLANCO, NEGRO

def dibujar_texto(pantalla, texto, posicion, fuente, color):
    """
    Dibuja un texto en pantalla con una sombra negra por detrás para legibilidad.
    
    Espera:
        pantalla: Superficie de Pygame donde dibujar.
        texto (str): El mensaje a escribir.
        posicion (tuple): Coordenadas (x, y).
        fuente: Objeto fuente de Pygame.
        color (tuple): Color RGB del texto principal.
        
    Hace:
        1. Genera la superficie del texto en negro (sombra) y la dibuja desplazada 2 píxeles.
        2. Genera la superficie en el color original y la dibuja sobre la sombra.
        
    Retorna:
        None.
    """
    sombra = fuente.render(texto, True, NEGRO)
    pantalla.blit(sombra, (posicion[0] + 2, posicion[1] + 2))
    superficie = fuente.render(texto, True, color)
    pantalla.blit(superficie, posicion)

def dibujar_boton(pantalla, texto, rectangulo, color_base, fuente, color_texto=BLANCO):
    """
    Dibuja un botón rectangular con bordes redondeados y efecto de brillo al pasar el mouse.
    
    Espera:
        pantalla: Superficie de dibujo.
        texto (str): Lo que dirá el botón.
        rectangulo (pygame.Rect): Dimensiones y posición.
        color_base (tuple): Color del botón.
        fuente: Objeto fuente.
        color_texto (tuple): Color de la letra (por defecto blanco).
        
    Hace:
        1. Detecta si el mouse está sobre el botón para aclarar el color (hover).
        2. Dibuja el fondo, un borde blanco y el texto centrado.
        
    Retorna:
        None.
    """
    mouse_pos = pygame.mouse.get_pos()
    color_final = color_base
    
    if rectangulo.collidepoint(mouse_pos):
        # Efecto Hover: Aclara el color un poco
        rojo = min(color_base[0] + 40, 255)
        verde = min(color_base[1] + 40, 255)
        azul = min(color_base[2] + 40, 255)
        color_final = (rojo, verde, azul)
    
    # Creación del botón físico
    pygame.draw.rect(pantalla, color_final, rectangulo, border_radius=12)
    pygame.draw.rect(pantalla, BLANCO, rectangulo, 3, border_radius=12)
    
    # Centrar el texto dentro del botón
    txt_surf = fuente.render(texto, True, color_texto)
    txt_rect = txt_surf.get_rect(center=rectangulo.center)
    pantalla.blit(txt_surf, txt_rect)

def dibujar_boton_multilinea(pantalla, texto, rectangulo, color_base, fuente, color_texto=BLANCO):
    """
    Similar a dibujar_boton, pero corta el texto en varias líneas si es muy largo.
    Ideal para los enunciados de las preguntas.
    
    Espera:
        Mismos parámetros que dibujar_boton.
        
    Hace:
        1. Corta el texto por palabras usando .split(' ').
        2. Va sumando palabras a una línea hasta que el ancho supera el del botón.
        3. Dibuja cada línea por separado centrada verticalmente.
        
    Retorna:
        None.
    """
    pygame.draw.rect(pantalla, color_base, rectangulo, border_radius=12)
    pygame.draw.rect(pantalla, BLANCO, rectangulo, 3, border_radius=12)

    palabras = texto.split(' ')
    lineas = []
    linea_actual = ""
    ancho_maximo = rectangulo.width - 20 

    for palabra in palabras:
        test_linea = linea_actual + palabra + " "
        if fuente.size(test_linea)[0] < ancho_maximo:
            linea_actual = test_linea
        else:
            lineas.append(linea_actual)
            linea_actual = palabra + " "
    lineas.append(linea_actual)

    # Cálculo de la altura total del bloque de texto para centrarlo
    alto_total = len(lineas) * fuente.get_linesize()
    y_inicial = rectangulo.centery - (alto_total // 2)

    for i in range(len(lineas)):
        txt_surf = fuente.render(lineas[i], True, color_texto)
        txt_rect = txt_surf.get_rect(centerx=rectangulo.centerx, y=y_inicial + (i * fuente.get_linesize()))
        pantalla.blit(txt_surf, txt_rect)