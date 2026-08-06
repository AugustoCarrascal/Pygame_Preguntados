"""
Módulo de gestión de recursos.
Se encarga de la carga de imágenes, fuentes y la reproducción de música.
"""

import pygame
from pathlib import Path
from configuracion.constantes import ANCHO, ALTO
from interfaz import RAIZ_PROYECTO

def cargar_recursos():
    """
    Carga todos los elementos visuales y fuentes necesarios para el juego.
    
    Espera:
        Nada.
        
    Hace:
        1. Carga los archivos .jpg de fondo.
        2. Los escala al tamaño de la ventana (800x600).
        3. Inicializa las fuentes (Arial) con diferentes tamaños.
        
    Retorna:
        tuple: (fondo_menu, fondo_juego, fuente_titulo, fuente_pregunta, fuente_normal).
    """
    archivo_fondo_menu = pygame.image.load(RAIZ_PROYECTO / "sonidos_y_fondos" / "menu_fondo.jpg")
    imagen_fondo_menu = pygame.transform.scale(archivo_fondo_menu, (ANCHO, ALTO))
    
    archivo_fondo_juego = pygame.image.load(RAIZ_PROYECTO / "sonidos_y_fondos" / "juego_fondo.jpg")
    imagen_fondo_juego = pygame.transform.scale(archivo_fondo_juego, (ANCHO, ALTO))
    
    fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
    fuente_pregunta = pygame.font.SysFont("Arial", 30, bold=True)
    fuente_normal = pygame.font.SysFont("Arial", 26)
    
    return imagen_fondo_menu, imagen_fondo_juego, fuente_titulo, fuente_pregunta, fuente_normal

def reproducir_musica(archivo_musica, volumen, bucle=0):
    """
    Inicializa y reproduce un archivo de audio como música de fondo.
    
    Espera:
        archivo_musica (str): Ruta al archivo .mp3.
        volumen (float): Nivel de sonido entre 0.0 y 1.0.
        bucle (int): -1 para infinito, 0 para una sola vez.
        
    Hace:
        Carga el archivo en el mixer de Pygame, ajusta el volumen y le da al play.
        
    Retorna:
        None.
    """
    ruta_musica = Path(archivo_musica)
    if not ruta_musica.is_absolute():
        ruta_musica = RAIZ_PROYECTO / archivo_musica

    try:
        pygame.mixer.music.load(str(ruta_musica))
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(bucle)
    except pygame.error:
        print(f"Aviso: no se pudo reproducir la música: {ruta_musica}")