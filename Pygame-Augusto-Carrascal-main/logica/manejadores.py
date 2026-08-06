"""
Módulo de manejadores de eventos.
Contiene la lógica que decide qué sucede cuando el usuario hace clic.
"""

import pygame
import sys
from logica.logica_juego import buscar_categoria_usada, activar_comodin_por_categoria, eliminar_preguntas_de_categoria
from datos.data import verificar_respuesta, finalizar_partida, reiniciar_estadisticas_usuario
from interfaz.ui.inicializacion import preparar_sesion_usuario

def manejar_clic_inicio(estado, rects, pos, recursos):
    """Maneja los clics en la pantalla de bienvenida."""
    if rects["comenzar"].collidepoint(pos):
        estado["fase_actual"] = "SELECCION_USUARIO"
    elif rects["salir_inicio"].collidepoint(pos):
        pygame.quit()
        sys.exit()

def manejar_clic_seleccion(estado, rects, pos, recursos):
    """Maneja la elección del perfil de usuario."""
    if rects["usuario_1"].collidepoint(pos):
        vincular_usuario(estado, "Usuario 1", recursos)
    elif rects["usuario_2"].collidepoint(pos):
        vincular_usuario(estado, "Usuario 2", recursos)

def vincular_usuario(estado, nombre, recursos):
    """
    Establece la conexión entre el perfil elegido y el sistema de juego.
    
    Espera:
        estado (dict): El control global.
        nombre (str): 'Usuario 1' o 'Usuario 2'.
        recursos (dict): Las imágenes cargadas.
        
    Hace:
        Carga los datos del usuario, las preguntas y cambia la pantalla al Menú.
        
    Retorna:
        None.
    """
    estado["usuario_nombre"] = nombre
    estado["fase_actual"] = "MENU"
    estado["imagen_fondo_actual"] = recursos["fondo_juego"]
    estado["juego_dict"], estado["datos_usuario_actual"] = preparar_sesion_usuario(nombre, estado["volumen_actual"])

def manejar_clic_menu(estado, rects, pos, recursos):
    """Maneja los botones del Menú principal."""
    if rects["jugar"].collidepoint(pos):
        if len(estado["juego_dict"]["lista"]) > 0:
            estado["juego_dict"]["vidas"] = 3
            estado["juego_dict"]["puntos"] = 0
            estado["juego_dict"]["racha_aciertos"] = 0
            estado["juego_dict"]["categorias_usadas"] = []
            estado["fase_actual"] = "JUEGO"
    elif rects["estadisticas"].collidepoint(pos):
        estado["fase_actual"] = "ESTADISTICAS"
    elif rects["configuracion"].collidepoint(pos):
        estado["fase_actual"] = "CONFIGURACION"
    elif rects["salir_menu"].collidepoint(pos):
        estado["fase_actual"] = "INICIO"

def manejar_clic_estadisticas(estado, rects, pos, recursos):
    """Maneja el botón de volver de la pantalla de récords."""
    if rects["volver"].collidepoint(pos):
        estado["fase_actual"] = "MENU"

def manejar_clic_configuracion(estado, rects, pos, recursos):
    """Maneja el reseteo de puntos y el cambio de modo TDA/H."""
    if rects["reiniciar_config"].collidepoint(pos):
        reiniciar_estadisticas_usuario(estado["juego_dict"])
        estado["datos_usuario_actual"] = estado["juego_dict"]["usuario_dict"]
    elif rects["volver"].collidepoint(pos):
        estado["fase_actual"] = "MENU"
    elif rects["tdah"].collidepoint(pos):
        if estado["juego_dict"]["modo_tdah"] == True:
            estado["juego_dict"]["modo_tdah"] = False
        else:
            estado["juego_dict"]["modo_tdah"] = True

def manejar_clic_juego_fase(estado, rects, pos, recursos):
    """Maneja los clics durante la ronda de preguntas."""
    if rects["volver_juego"].collidepoint(pos):
        estado["fase_actual"] = "MENU"
        return
    # Delega la lógica de respuesta a otra función específica
    estado["fase_actual"] = manejar_clic_juego_logica(estado["juego_dict"], pos, rects["opcion_a"], rects["opcion_b"], rects["opcion_c"], rects["opcion_d"])

def manejar_clic_comodin_fase(estado, rects, pos, recursos):
    """Maneja la elección de categoría del comodín."""
    estado["fase_actual"] = manejar_clic_comodin(estado["juego_dict"], pos, rects["cat_deportes"], rects["cat_informatica"], rects["cat_historia"], rects["cat_superheroes"])

def manejar_clic_victoria(estado, rects, pos, recursos):
    """Maneja el botón de salida después de ganar."""
    if rects["volver_desde_victoria"].collidepoint(pos):
        estado["fase_actual"] = "MENU"

def gestionar_volumen(estado, rects, pos):
    """Aumenta o disminuye el volumen del mixer musical."""
    if rects["volumen_subir"].collidepoint(pos):
        estado["volumen_actual"] = min(estado["volumen_actual"] + 0.1, 1.0)
        pygame.mixer.music.set_volume(estado["volumen_actual"])
    elif rects["volumen_bajar"].collidepoint(pos):
        estado["volumen_actual"] = max(estado["volumen_actual"] - 0.1, 0.0)
        pygame.mixer.music.set_volume(estado["volumen_actual"])

def manejar_clic_juego_logica(juego, click, rect_a, rect_b, rect_c, rect_d):
    """
    Procesa cuál opción (A, B, C o D) fue elegida y activa el verificador.
    
    Espera:
        juego (dict): Estado del juego actual.
        click (tuple): Coordenadas del mouse.
        rect_a..d: Rectángulos de las opciones.
        
    Hace:
        1. Detecta en qué opción hizo click.
        2. Llama a verificar_respuesta().
        3. Chequea si ganó el juego o perdió todas las vidas.
        
    Retorna:
        str: La nueva fase ('JUEGO', 'COMODIN', o el estado actual).
    """
    opcion = " "
    if rect_a.collidepoint(click): opcion = "a"
    elif rect_b.collidepoint(click): opcion = "b"
    elif rect_c.collidepoint(click): opcion = "c"
    elif rect_d.collidepoint(click): opcion = "d"

    if opcion != " ":
        acerto = verificar_respuesta(juego, opcion)
        cat_c = juego["categoria_comodin_actual"]
        
        if cat_c != "":
            if acerto == True:
                juego["categorias_usadas"].append(cat_c)
                eliminar_preguntas_de_categoria(juego, cat_c)
            juego["categoria_comodin_actual"] = ""

        # Verificación de condiciones de fin de juego
        if len(juego["categorias_usadas"]) >= 4:
            finalizar_partida(juego)
            juego["feedback_mensaje"] = "¡VICTORIA TOTAL!"
            juego["feedback_timer"] = 240 if juego["modo_tdah"] else 120
            return "JUEGO"
        
        if juego["vidas"] <= 0:
            finalizar_partida(juego)
            juego["feedback_mensaje"] = "GAME OVER - VIDAS: 0"
            juego["feedback_timer"] = 240 if juego["modo_tdah"] else 120
            return "JUEGO"
        
        elif juego["racha_aciertos"] == 3:
            return "COMODIN"
            
    return "JUEGO"

def manejar_clic_comodin(juego, click, rect_dep, rect_inf, rect_his, rect_sup):
    """
    Procesa la elección de categoría del comodín y la activa.
    
    Espera:
        juego (dict): Estado del juego.
        click: Posición mouse.
        rect_dep..sup: Rectángulos de las categorías.
        
    Hace:
        1. Identifica qué categoría eligió el usuario.
        2. Verifica que no sea una categoría ya ganada.
        3. Llama a activar_comodin_por_categoria().
        
    Retorna:
        str: Cambia a la fase 'JUEGO' si eligió bien, sino sigue en 'COMODIN'.
    """
    elegida = ""
    if rect_dep.collidepoint(click):
        if buscar_categoria_usada(juego["categorias_usadas"], "Deportes") == False:
            elegida = "Deportes"
    elif rect_inf.collidepoint(click):
        if buscar_categoria_usada(juego["categorias_usadas"], "Informática") == False:
            elegida = "Informática"
    elif rect_his.collidepoint(click):
        if buscar_categoria_usada(juego["categorias_usadas"], "Historia") == False:
            elegida = "Historia"
    elif rect_sup.collidepoint(click):
        if buscar_categoria_usada(juego["categorias_usadas"], "Superhéroes") == False:
            elegida = "Superhéroes"

    if elegida != "":
        juego["categoria_comodin_actual"] = elegida
        activar_comodin_por_categoria(juego, elegida)
        return "JUEGO"
    return "COMODIN"

# Diccionario de despacho de eventos
DICCIONARIO_FASES_CLIC = {
    "INICIO": manejar_clic_inicio,
    "SELECCION_USUARIO": manejar_clic_seleccion,
    "MENU": manejar_clic_menu,
    "ESTADISTICAS": manejar_clic_estadisticas,
    "CONFIGURACION": manejar_clic_configuracion,
    "JUEGO": manejar_clic_juego_fase,
    "COMODIN": manejar_clic_comodin_fase,
    "VICTORIA": manejar_clic_victoria
}
