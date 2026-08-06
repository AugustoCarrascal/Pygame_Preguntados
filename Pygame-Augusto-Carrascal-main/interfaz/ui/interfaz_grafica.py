"""
Módulo de Interfaz Gráfica - Preguntados.
Orquestador principal del bucle de juego y renderizado.
"""

import pygame
import sys
from configuracion.constantes import FPS
from interfaz.recursos import reproducir_musica
from .inicializacion import inicializar_sistema, obtener_recursos_sistema, inicializar_control_juego, obtener_rectangulos
from logica.manejadores import DICCIONARIO_FASES_CLIC, gestionar_volumen
from interfaz.vistas import (
    renderizar_inicio, renderizar_seleccion_usuario, renderizar_pantalla_menu,
    renderizar_pantalla_estadisticas, renderizar_pantalla_juego, 
    renderizar_pantalla_configuracion, renderizar_pantalla_comodin, 
    renderizar_pantalla_victoria, dibujar_botones_fase
)

# Diccionario de despacho de vistas: Asocia el nombre de la fase con su función de dibujo.
DICCIONARIO_VISTAS = {
    "INICIO": renderizar_inicio,
    "SELECCION_USUARIO": renderizar_seleccion_usuario,
    "MENU": renderizar_pantalla_menu,
    "ESTADISTICAS": renderizar_pantalla_estadisticas,
    "JUEGO": renderizar_pantalla_juego,
    "CONFIGURACION": renderizar_pantalla_configuracion,
    "COMODIN": renderizar_pantalla_comodin,
    "VICTORIA": renderizar_pantalla_victoria
}

def dibujar_pantallas(pantalla, control, recursos, rects):
    """
    Decide qué pantalla dibujar y añade los botones comunes del sistema (volumen).
    
    Espera:
        pantalla: Superficie de dibujo.
        control (dict): Estado global del juego.
        recursos (dict): Diccionario de imágenes/fuentes.
        rects (dict): Diccionario de rectángulos de botones.
        
    Hace:
        Busca en el DICCIONARIO_VISTAS la función correspondiente a control["fase_actual"] y la ejecuta.
        Luego dibuja los botones de volumen (fase "SISTEMA").
        
    Retorna:
        None.
    """
    fase = control["fase_actual"]
    if fase in DICCIONARIO_VISTAS:
        DICCIONARIO_VISTAS[fase](pantalla, control, recursos, rects)
    
    dibujar_botones_fase(pantalla, "SISTEMA", rects, recursos["fuente_normal"], control)

def iniciar_juego():
    """
    Motor central del juego. Contiene el bucle infinito que procesa todo.
    
    Espera:
        Nada.
        
    Hace:
        1. Llama a todas las funciones de inicialización.
        2. Maneja el paso del tiempo (frames y timers de feedback).
        3. Captura eventos de mouse y cierre de ventana.
        4. Orquesta el despacho de clics y dibujo de pantallas.
        
    Retorna:
        None (el juego termina al cerrar la ventana).
    """
    pantalla, reloj = inicializar_sistema()
    recursos = obtener_recursos_sistema()
    rectangulos = obtener_rectangulos()
    control = inicializar_control_juego(recursos)
    
    reproducir_musica("sonidos_y_fondos/musica_menu.mp3", control["volumen_actual"], -1)

    while True:
        # Dibujamos primero para que la pantalla no se vea negra
        dibujar_pantallas(pantalla, control, recursos, rectangulos)
        
        # Procesamiento de feedback y transiciones automáticas después del cartel
        if control.get("juego_dict") and control["juego_dict"].get("feedback_timer", 0) > 0:
            control["juego_dict"]["feedback_timer"] -= 1
            if control["juego_dict"]["feedback_timer"] == 0:
                if control["juego_dict"]["vidas"] <= 0:
                    control["fase_actual"] = "MENU"
                elif len(control["juego_dict"]["categorias_usadas"]) >= 4:
                    control["fase_actual"] = "VICTORIA"

        # Captura de eventos de Pygame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if control.get("juego_dict") and control["juego_dict"].get("feedback_timer", 0) > 0:
                    continue

                click_pos = evento.pos
                gestionar_volumen(control, rectangulos, click_pos)
                
                # Despacho de clics por fase
                fase = control["fase_actual"]
                if fase in DICCIONARIO_FASES_CLIC:
                    DICCIONARIO_FASES_CLIC[fase](control, rectangulos, click_pos, recursos)

        pygame.display.flip() # Actualiza el monitor con lo dibujado
        reloj.tick(FPS) # Mantiene la velocidad constante (60 fps)