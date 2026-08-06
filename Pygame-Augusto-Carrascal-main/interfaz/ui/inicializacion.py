"""
Módulo de inicialización del juego.
Controla el arranque del sistema, la carga inicial de recursos y la configuración del usuario.
"""

import pygame
import json
from configuracion.constantes import ANCHO, ALTO
from interfaz import RAIZ_PROYECTO
from interfaz.recursos import cargar_recursos, reproducir_musica
from datos.data import inicializar_estadisticas, cargar_datos, cargar_preguntas

def inicializar_sistema():
    """
    Arranca los motores de Pygame y crea la ventana.
    
    Espera:
        Nada.
        
    Hace:
        1. Inicializa los módulos de video y audio de Pygame.
        2. Crea la ventana física de 800x600.
        3. Define el título de la ventana.
        
    Retorna:
        tuple: (pantalla, reloj_de_fps).
    """
    pygame.init()
    pygame.font.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        print("Aviso: no se pudo inicializar el mixer de audio.")
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Preguntados - Trabajo Final")
    reloj = pygame.time.Clock()
    return pantalla, reloj

def obtener_recursos_sistema():
    """
    Carga todas las imágenes y fuentes y las guarda en un diccionario organizado.
    
    Espera:
        Nada.
        
    Hace:
        Llama a cargar_recursos() y mete los resultados en un diccionario con llaves fáciles de recordar.
        
    Retorna:
        dict: Diccionario con todos los recursos cargados.
    """
    fondo_menu, fondo_juego, f_titulo, f_pregunta, f_normal = cargar_recursos()
    return {
        "fondo_menu": fondo_menu,
        "fondo_juego": fondo_juego,
        "fuente_titulo": f_titulo,
        "fuente_pregunta": f_pregunta,
        "fuente_normal": f_normal
    }

def inicializar_control_juego(recursos):
    """
    Crea el diccionario principal de control que viajará por todo el código.
    
    Espera:
        recursos (dict): El diccionario de imágenes y fuentes.
        
    Hace:
        Define la fase inicial ('INICIO'), el volumen (0.5) y prepara el espacio para los datos del usuario.
        
    Retorna:
        dict: El diccionario de estado global ('control').
    """
    return {
        "volumen_actual": 0.5,
        "fase_actual": "INICIO",
        "usuario_nombre": "",
        "datos_usuario_actual": {},
        "juego_dict": "",
        "imagen_fondo_actual": recursos["fondo_menu"]
    }

def obtener_rectangulos():
    """
    Transforma la configuración de los botones (coordenadas) del JSON a objetos Rect de Pygame.
    
    Espera:
        Nada (lee el archivo 'configuracion_botones.json' internamente).
        
    Hace:
        1. Abre el JSON.
        2. Recorre cada fase y cada botón.
        3. Crea un objeto pygame.Rect(x, y, ancho, alto) para cada botón.
        
    Retorna:
        dict: Diccionario donde la llave es el ID del botón y el valor es su rectángulo físico.
    """
    with open(RAIZ_PROYECTO / "datos" / "configuracion_botones.json", "r", encoding="utf-8") as archivo:
        config = json.load(archivo)
    
    rectangulos = {}
    for fase in config:
        lista_botones = config[fase]
        for b in lista_botones:
            rectangulos[b["id"]] = pygame.Rect(b["rect"][0], b["rect"][1], b["rect"][2], b["rect"][3])
            
    return rectangulos

def preparar_sesion_usuario(nombre, volumen):
    """
    Configura todo lo necesario para empezar a jugar con un perfil específico.
    
    Espera:
        nombre (str): Nombre del perfil ('Usuario 1' o 'Usuario 2').
        volumen (float): Volumen musical actual.
        
    Hace:
        1. Cambia la música a la de juego.
        2. Carga las estadísticas del usuario desde su JSON.
        3. Carga las preguntas del mazo CSV.
        4. Crea el 'juego_dict' con puntos, vidas y racha en cero.
        
    Retorna:
        tuple: (nuevo_diccionario_de_juego, datos_historicos_del_usuario).
    """
    reproducir_musica("sonidos_y_fondos/musica_juego.mp3", volumen, -1)
    ruta = inicializar_estadisticas(nombre)
    datos = cargar_datos(ruta)
    preguntas = cargar_preguntas(RAIZ_PROYECTO / "datos" / "preguntas.csv")
    
    nuevo_juego = {
        "lista": preguntas, "puntos": 0, "vidas": 3, "racha_aciertos": 0,
        "usuario_dict": datos, "nombre_archivo_usuario": ruta,
        "categorias_usadas": [], "categoria_comodin_actual": "", "modo_tdah": False,
        "feedback_mensaje": "", "feedback_timer": 0
    }
    return nuevo_juego, datos
