"""
Punto de acceso principal al videojuego Preguntados.
Su única responsabilidad es iniciar el sistema gráfico.
"""

import os
from interfaz.ui.interfaz_grafica import iniciar_juego

if __name__ == "__main__":
    """
    Este bloque asegura que el juego solo arranque si ejecutamos este archivo directamente.
    
    Espera:
        Nada.
        
    Hace:
        Cambia el directorio de trabajo a la carpeta del script y llama a iniciar_juego().
        
    Retorna:
        None.
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    iniciar_juego()


