"""
Módulo de visualización y renderizado.
Organiza el dibujo de cada pantalla basándose en el estado del controlador.
"""

import pygame
import json
from configuracion.constantes import *
from interfaz import RAIZ_PROYECTO
from interfaz.ui.componentes import dibujar_texto, dibujar_boton, dibujar_boton_multilinea
from logica.logica_juego import buscar_categoria_usada

# Cargamos la configuración de botones globalmente para las vistas
with open(RAIZ_PROYECTO / "datos" / "configuracion_botones.json", "r", encoding="utf-8") as f:
    CONFIG_BOTONES = json.load(f)

def dibujar_botones_fase(pantalla, fase, rects, fuente, estado):
    """
    Dibuja automáticamente todos los botones configurados en el JSON para una fase específica.
    
    Espera:
        pantalla: Superficie de dibujo.
        fase (str): El nombre de la pantalla actual (ej: 'INICIO').
        rects (dict): Diccionario que asocia IDs con objetos pygame.Rect.
        fuente: Fuente normal.
        estado (dict): El diccionario de control del juego.
        
    Hace:
        1. Busca en el JSON los botones de esa fase.
        2. Si el texto es 'DINAMICO', busca la opción de la pregunta actual.
        3. Dibuja el botón con su color y posición.
        
    Retorna:
        None.
    """
    if fase in CONFIG_BOTONES:
        for btn in CONFIG_BOTONES[fase]:
            rect = rects[btn["id"]]
            color = btn["color"]
            texto = btn["texto"]

            if texto == "DINAMICO":
                juego = estado["juego_dict"]
                if len(juego["lista"]) > 0:
                    pregunta = juego["lista"][0]
                    if btn["id"] == "opcion_a": texto = pregunta["opcion_a"]
                    elif btn["id"] == "opcion_b": texto = pregunta["opcion_b"]
                    elif btn["id"] == "opcion_c": texto = pregunta["opcion_c"]
                    elif btn["id"] == "opcion_d": texto = pregunta["opcion_d"]
                    elif btn["id"] == "enunciado": 
                        dibujar_boton_multilinea(pantalla, pregunta["pregunta"], rect, AMARILLO, fuente, color_texto=NEGRO)
                        continue 
                else:
                    continue

            # Ajuste visual de colores para modo TDA/H
            if estado["juego_dict"] != "":
                if estado["juego_dict"]["modo_tdah"] == True:
                    if fase == "JUEGO":
                        color = (70, 70, 80)

            dibujar_boton(pantalla, texto, rect, color, fuente)

def renderizar_inicio(pantalla, estado, recursos, rects):
    """Renderiza la pantalla de bienvenida con el título gigante."""
    pantalla.blit(recursos["fondo_menu"], (0, 0))
    dibujar_texto(pantalla, "PREGUNTADOS", (215, 100), recursos["fuente_titulo"], AMARILLO)
    dibujar_botones_fase(pantalla, "INICIO", rects, recursos["fuente_normal"], estado)

def renderizar_seleccion_usuario(pantalla, estado, recursos, rects):
    """Renderiza la pantalla para elegir el perfil del jugador."""
    pantalla.blit(recursos["fondo_menu"], (0, 0))
    dibujar_texto(pantalla, "ELIJA SU PERFIL", (310, 170), recursos["fuente_normal"], AMARILLO)
    dibujar_botones_fase(pantalla, "SELECCION_USUARIO", rects, recursos["fuente_normal"], estado)

def renderizar_pantalla_menu(pantalla, estado, recursos, rects):
    """Renderiza el menú principal después de loguearse."""
    pantalla.blit(estado["imagen_fondo_actual"], (0, 0))
    dibujar_botones_fase(pantalla, "MENU", rects, recursos["fuente_normal"], estado)

def renderizar_pantalla_estadisticas(pantalla, estado, recursos, rects):
    """Renderiza la tabla de récords y aciertos históricos del usuario."""
    pantalla.blit(recursos["fondo_juego"], (0, 0))
    nombre = estado["usuario_nombre"]
    datos = estado["datos_usuario_actual"]
    dibujar_texto(pantalla, f"ESTADISTICAS: {nombre}", (200, 50), recursos["fuente_normal"], BLANCO)
    
    pos_y = 150
    for clave, valor in datos.items():
        clave_limpia = ""
        for c in clave:
            if c == "_": clave_limpia += " "
            else: clave_limpia += c
        
        txt = f"{clave_limpia.capitalize()}: {valor}"
        dibujar_boton(pantalla, txt, pygame.Rect(250, pos_y, 300, 40), AZUL_FUERTE, recursos["fuente_normal"])
        pos_y += 60
    dibujar_botones_fase(pantalla, "ESTADISTICAS", rects, recursos["fuente_normal"], estado)

def renderizar_pantalla_juego(pantalla, estado, recursos, rects):
    """
    Controla el dibujo de la pantalla de trivia.
    Dibuja puntos, vidas, dificultad y el cartel de feedback.
    """
    juego = estado["juego_dict"]
    if juego["modo_tdah"] == True:
        pantalla.fill((20, 20, 30))
    else:
        pantalla.blit(estado["imagen_fondo_actual"], (0, 0))
    
    dibujar_botones_fase(pantalla, "JUEGO", rects, recursos["fuente_normal"], estado)
    
    dibujar_texto(pantalla, f"PUNTOS: {juego['puntos']}", (620, 500), recursos["fuente_normal"], VERDE)
    dibujar_texto(pantalla, f"VIDAS: {juego['vidas']}", (620, 540), recursos["fuente_normal"], ROJO)
    
    if len(juego["lista"]) > 0:
        texto_dif = f"Dificultad: {juego['lista'][0]['dificultad'].capitalize()}"
        dibujar_texto(pantalla, texto_dif, (20, 20), recursos["fuente_normal"], BLANCO)

    # Cartel de feedback de respuesta
    if juego["feedback_timer"] > 0:
        texto_feedback = juego["feedback_mensaje"]
        color_feedback = VERDE if (texto_feedback == "¡CORRECTO!" or "VICTORIA" in texto_feedback) else ROJO
        
        rect_f = pygame.Rect((ANCHO//2)-250, (ALTO//2)-60, 500, 120)
        pygame.draw.rect(pantalla, NEGRO, rect_f)
        pygame.draw.rect(pantalla, color_feedback, rect_f, 4)
        
        fuente_f = recursos["fuente_titulo"]
        ancho_t, alto_t = fuente_f.size(texto_feedback)
        dibujar_texto(pantalla, texto_feedback, (rect_f.centerx-ancho_t//2, rect_f.centery-alto_t//2), fuente_f, color_feedback)

def renderizar_pantalla_configuracion(pantalla, estado, recursos, rects):
    """Muestra los botones para resetear estadísticas y activar modo TDA/H."""
    pantalla.blit(recursos["fondo_menu"], (0, 0))
    dibujar_texto(pantalla, "CONFIGURACIÓN", (250, 50), recursos["fuente_titulo"], BLANCO)
    
    modo = estado["juego_dict"]["modo_tdah"]
    for btn in CONFIG_BOTONES["CONFIGURACION"]:
        if btn["id"] == "tdah":
            if modo == True:
                btn["texto"] = "MODO DE JUEGO NORMAL"; btn["color"] = VERDE
            else:
                btn["texto"] = "MODO TDA/H"; btn["color"] = AZUL_FUERTE
            
    dibujar_botones_fase(pantalla, "CONFIGURACION", rects, recursos["fuente_normal"], estado)

def renderizar_pantalla_victoria(pantalla, estado, recursos, rects):
    """Muestra el mensaje de triunfo total al completar las 4 categorías."""
    juego = estado["juego_dict"]
    if juego["modo_tdah"] == True:
        pantalla.fill((20, 20, 30))
        fuente_v = pygame.font.SysFont("Arial", 80, bold=True)
        pos_v = (100, 200)
    else:
        pantalla.blit(estado["imagen_fondo_actual"], (0, 0))
        fuente_v = recursos["fuente_titulo"]
        pos_v = (230, 200)

    dibujar_texto(pantalla, "¡GANASTE!", pos_v, fuente_v, AMARILLO)
    dibujar_texto(pantalla, f"Puntaje Final: {juego['puntos']}", (300, 320), recursos["fuente_normal"], BLANCO)
    dibujar_botones_fase(pantalla, "VICTORIA", rects, recursos["fuente_normal"], estado)

def renderizar_pantalla_comodin(pantalla, estado, recursos, rects):
    """Muestra los 4 botones de categorías para que el usuario elija su comodín."""
    pantalla.blit(estado["imagen_fondo_actual"], (0, 0))
    dibujar_texto(pantalla, "¡RACHA DE 3! ELEGÍ CATEGORÍA", (130, 60), recursos["fuente_normal"], BLANCO)
    
    usadas = estado["juego_dict"]["categorias_usadas"]
    for btn in CONFIG_BOTONES["COMODIN"]:
        if buscar_categoria_usada(usadas, btn["texto"]) == False:
            dibujar_boton(pantalla, btn["texto"], rects[btn["id"]], btn["color"], recursos["fuente_normal"])