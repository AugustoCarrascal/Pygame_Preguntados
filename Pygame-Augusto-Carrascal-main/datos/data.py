"""
Módulo de gestión de datos persistentes.
Maneja la lectura/escritura de archivos JSON de usuario y la carga de preguntas desde CSV.
"""

import json
import random
from pathlib import Path
from logica.logica_juego import obtener_puntos
from interfaz import RAIZ_PROYECTO

def _ruta_proyecto(ruta_archivo):
    ruta = Path(ruta_archivo)
    if not ruta.is_absolute():
        ruta = RAIZ_PROYECTO / ruta_archivo
    return ruta

def inicializar_estadisticas(nombre_usuario):
    """
    Crea el archivo de estadísticas para un nuevo usuario si no existe.
    
    Espera:
        nombre_usuario (str): El nombre del perfil elegido por el usuario.
        
    Hace:
        1. Limpia el nombre reemplazando espacios por guiones bajos manualmente.
        2. Crea un archivo .json vacío si no existe usando el modo 'a'.
        3. Si el archivo está vacío, le escribe la estructura inicial de datos.
        
    Retorna:
        str: La ruta (nombre) del archivo JSON del usuario.
    """
    nombre_archivo_limpio = ""
    for caracter in nombre_usuario:
        if caracter == " ":
            nombre_archivo_limpio += "_"
        else:
            nombre_archivo_limpio += caracter
    
    nombre_archivo_limpio = nombre_archivo_limpio.lower()
    ruta_archivo = _ruta_proyecto("datos/" + nombre_archivo_limpio + ".json")
    
    archivo_creador = open(ruta_archivo, 'a', encoding='utf-8')
    archivo_creador.close()
    
    archivo_lector = open(ruta_archivo, 'r', encoding='utf-8')
    contenido = archivo_lector.read()
    archivo_lector.close()

    if contenido == "":
        datos_iniciales = {
            "usuario": nombre_usuario, 
            "puntaje_maximo": 0, 
            "partidas_jugadas": 0,
            "correctas": 0, 
            "incorrectas": 0
        }
        guardar_datos(ruta_archivo, datos_iniciales)
        
    return ruta_archivo

def cargar_datos(ruta_archivo):
    """
    Lee un archivo JSON y lo convierte en un diccionario.
    
    Espera:
        ruta_archivo (str): Ruta al archivo JSON que se quiere leer.
        
    Hace:
        Abre el archivo indicado y usa json.load para transformar el texto en un objeto de Python.
        
    Retorna:
        dict: Los datos cargados del archivo.
    """
    ruta = _ruta_proyecto(ruta_archivo)
    with open(ruta, 'r', encoding='utf-8') as archivo:
        datos_cargados = json.load(archivo)
    return datos_cargados

def guardar_datos(ruta_archivo, datos_a_guardar):
    """
    Guarda un diccionario en un archivo JSON.
    
    Espera:
        ruta_archivo (str): Ruta donde se guardarán los datos.
        datos_a_guardar (dict): El diccionario que se quiere persistir.
        
    Hace:
        Escribe el diccionario en el archivo físico con una sangría de 4 espacios para que sea legible.
        
    Retorna:
        None.
    """
    ruta = _ruta_proyecto(ruta_archivo)
    with open(ruta, 'w', encoding='utf-8') as archivo:
        json.dump(datos_a_guardar, archivo, indent=4, ensure_ascii=False)

def cargar_preguntas(ruta_archivo_csv):
    """
    Lee el archivo CSV de preguntas y devuelve una lista de diccionarios mezclada.
    
    Espera:
        ruta_archivo_csv (str): Ruta al archivo .csv con las preguntas.
        
    Hace:
        1. Lee todas las líneas del archivo.
        2. Saltea la primera línea (cabecera).
        3. Usa .strip() y .split(';') para separar cada dato.
        4. Mezcla el orden de las preguntas al azar.
        
    Retorna:
        list: Lista de diccionarios, donde cada uno es una pregunta.
    """
    ruta = _ruta_proyecto(ruta_archivo_csv)
    with open(ruta, mode='r', encoding='utf-8') as archivo:
        todas_las_lineas = archivo.readlines()
    
    lista_de_preguntas_final = []

    for linea in todas_las_lineas[1:]:
        linea_limpia = linea.strip()
        
        if linea_limpia != "":
            datos = linea_limpia.split(';')
            
            diccionario_pregunta = {
                "pregunta": datos[0],
                "opcion_a": datos[1],
                "opcion_b": datos[2],
                "opcion_c": datos[3],
                "opcion_d": datos[4],
                "correcta": datos[5],
                "categoria": datos[6],
                "dificultad": datos[7],
                "puntaje": int(datos[8])
            }
            lista_de_preguntas_final.append(diccionario_pregunta)
    
    random.shuffle(lista_de_preguntas_final)
    return lista_de_preguntas_final

def verificar_respuesta(datos_juegos, respuesta_del_usuario):
    """
    Verifica si la respuesta elegida es correcta y actualiza el estado del juego.
    
    Espera:
        datos_juegos (dict): Estado global del juego actual.
        respuesta_del_usuario (str): La letra ('a', 'b', 'c', 'd') que presionó el jugador.
        
    Hace:
        1. Compara la respuesta con la correcta.
        2. Suma puntos y racha si acierta; resta vida y resetea racha si falla.
        3. Activa un temporizador de feedback (cartel de correcto/incorrecto).
        4. Elimina la pregunta de la lista con .pop(0).
        
    Retorna:
        bool: True si acertó, False si falló.
    """
    if not datos_juegos["lista"]:
        datos_juegos["feedback_mensaje"] = "NO HAY PREGUNTAS"
        datos_juegos["feedback_timer"] = 60
        return False

    pregunta_actual = datos_juegos["lista"][0]
    
    if respuesta_del_usuario == pregunta_actual["correcta"]:
        puntos_ganados = obtener_puntos(pregunta_actual["dificultad"])
        datos_juegos["puntos"] += puntos_ganados 
        datos_juegos["racha_aciertos"] += 1
        datos_juegos["usuario_dict"]["correctas"] += 1
        resultado_final = True
        datos_juegos["feedback_mensaje"] = "¡CORRECTO!"
    else:
        datos_juegos["vidas"] -= 1
        datos_juegos["racha_aciertos"] = 0
        datos_juegos["usuario_dict"]["incorrectas"] += 1
        resultado_final = False
        datos_juegos["feedback_mensaje"] = "INCORRECTO"

    if datos_juegos["modo_tdah"] == True:
        datos_juegos["feedback_timer"] = 180 
    else:
        datos_juegos["feedback_timer"] = 60

    if len(datos_juegos["lista"]) > 0:
        datos_juegos["lista"].pop(0)

    return resultado_final
    
def finalizar_partida(datos_juego):
    """
    Actualiza el récord y las estadísticas totales al terminar un juego.
    
    Espera:
        datos_juego (dict): El estado del juego que acaba de terminar.
        
    Hace:
        1. Aumenta el contador de partidas jugadas.
        2. Compara el puntaje actual con el máximo histórico y actualiza si es mayor.
        3. Guarda los cambios en el archivo JSON del usuario.
        
    Retorna:
        None.
    """
    datos_juego["usuario_dict"]["partidas_jugadas"] += 1
    puntaje_actual = datos_juego["puntos"]
    record_actual = datos_juego["usuario_dict"]["puntaje_maximo"]
    if puntaje_actual > record_actual:
        datos_juego["usuario_dict"]["puntaje_maximo"] = puntaje_actual
    guardar_datos(datos_juego["nombre_archivo_usuario"], datos_juego["usuario_dict"])

def reiniciar_estadisticas_usuario(datos_juego):
    """
    Pone todas las estadísticas del usuario en cero.
    
    Espera:
        datos_juego (dict): El estado del juego actual.
        
    Hace:
        Modifica el diccionario del usuario poniendo puntaje, partidas y aciertos en 0 y guarda el archivo.
        
    Retorna:
        None.
    """
    datos_juego["usuario_dict"]["puntaje_maximo"] = 0
    datos_juego["usuario_dict"]["partidas_jugadas"] = 0
    datos_juego["usuario_dict"]["correctas"] = 0
    datos_juego["usuario_dict"]["incorrectas"] = 0
    datos_juego["puntos"] = 0
    guardar_datos(datos_juego["nombre_archivo_usuario"], datos_juego["usuario_dict"])