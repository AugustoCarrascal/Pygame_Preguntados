"""
Módulo de reglas de negocio y lógica pura del juego.
No contiene elementos visuales, solo manipulación de datos.
"""

def obtener_puntos(dificultad):
    """
    Calcula cuántos puntos otorga una pregunta según su dificultad.
    
    Espera:
        dificultad (str): 'facil', 'media' o 'dificil'.
        
    Hace:
        Retorna un valor entero (10, 20 o 30) basado en la cadena recibida.
        
    Retorna:
        int: El puntaje correspondiente.
    """
    puntos = 10
    if dificultad == "media":
        puntos = 20
    elif dificultad == "dificil":
        puntos = 30
    return puntos

def buscar_categoria_usada(lista_usadas, categoria_a_buscar):
    """
    Verifica si una categoría ya fue completada por el usuario.
    
    Espera:
        lista_usadas (list): Lista con los nombres de las categorías ya ganadas.
        categoria_a_buscar (str): El nombre de la categoría que queremos chequear.
        
    Hace:
        Recorre la lista con un bucle for y compara cada elemento con el buscado.
        
    Retorna:
        bool: True si la encontró (está usada), False si no.
    """
    esta_usada = False
    for cat in lista_usadas:
        if cat == categoria_a_buscar:
            esta_usada = True
            break
    return esta_usada

def activar_comodin_por_categoria(diccionario_juego, categoria_elegida):
    """
    Busca una pregunta de una categoría específica y la pone al principio para que sea la próxima.
    
    Espera:
        diccionario_juego (dict): El estado actual del juego.
        categoria_elegida (str): El nombre de la categoría que el usuario eligió con el comodín.
        
    Hace:
        1. Recorre la lista de preguntas buscando la primera que coincida con la categoría.
        2. La extrae de su posición original con .pop().
        3. La inserta en la posición 0 de la lista.
        
    Retorna:
        bool: True si encontró una pregunta de esa categoría, False si no quedaba ninguna.
    """
    indice_encontrado = -1
    for i in range(len(diccionario_juego["lista"])):
        if diccionario_juego["lista"][i]["categoria"] == categoria_elegida:
            indice_encontrado = i
            break
    
    if indice_encontrado != -1:
        pregunta_especial = diccionario_juego["lista"].pop(indice_encontrado)
        diccionario_juego["lista"].insert(0, pregunta_especial)
        return True
    
    return False

def eliminar_preguntas_de_categoria(diccionario_juego, categoria_ganada):
    """
    Borra todas las preguntas de una categoría específica del mazo actual.
    
    Espera:
        diccionario_juego (dict): El estado actual del juego.
        categoria_ganada (str): El nombre de la categoría que se quiere eliminar.
        
    Hace:
        Crea una lista nueva filtrada que excluye a las preguntas de la categoría indicada y reemplaza la vieja.
        
    Retorna:
        None.
    """
    lista_nueva = []
    for pregunta in diccionario_juego["lista"]:
        if pregunta["categoria"] != categoria_ganada:
            lista_nueva.append(pregunta)
    diccionario_juego["lista"] = lista_nueva