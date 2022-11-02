import re


Caracteres = ['#','$','@','.','*','+']

PARED = '#'
JUGADOR = '@'
CAJA = '$'
OBJETIVO = '.'
OBJETIVO_CAJA = '*'
OBJETIVO_JUGADOR = "+"
VACIO = ' '


OESTE = (-1,0)
ESTE = (1,0)
NORTE = (0,-1)
SUR = (0,1)



def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Ejemplo:

    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''

    '''
    grilla: es una matriz (una lista de listas de strings)

    grilla vacia: [[]]
    grilla 1 x 1: [["#"]]
    grilla 2 x 2: [["#","#"], ["#","#"]]

    '''

    '''
        
    '''

    '''Desicion de diseno'''
    if desc == None:
        return None

    grilla=[]

    for fila in desc:    
        nueva_fila = []

        for caracter in fila:
            nueva_fila.append(caracter)

        grilla.append(nueva_fila)


    return grilla


def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    filas = len(grilla)
    columnas = len(grilla[0])
    return (columnas,filas)
    
def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    
    return grilla[f][c] == PARED


def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return grilla[f][c] == OBJETIVO or grilla[f][c] == OBJETIVO_CAJA or grilla[f][c] == OBJETIVO_JUGADOR

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    return grilla[f][c] == CAJA or grilla[f][c] == OBJETIVO_CAJA

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    return grilla[f][c] == JUGADOR or grilla[f][c] == OBJETIVO_JUGADOR


def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for fila in grilla:
        for c in fila:
            if c == CAJA:
                return False
            
    return True

def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''
    if direccion == ESTE or direccion == OESTE or direccion == NORTE or direccion == SUR:
        grilla_movida = mover_todo(grilla,direccion)
    else:
        return grilla
    return grilla_movida


def encontrar_jugador(grilla):
    for f, fila in enumerate(grilla):
        for c, caracter in enumerate(fila):
            if caracter == JUGADOR or caracter == OBJETIVO_JUGADOR:
                return c,f

def mover_todo(grilla, direccion):#(1,0) / (0,1)
    lat, long = direccion
    c,f = encontrar_jugador(grilla)
    if hay_pared(grilla,c+lat,f+long):# c+lat, f / c,f+long
        return grilla
    if hay_caja(grilla,c+lat,f+long) and hay_caja(grilla,c+lat*2,f+long*2):#c+lat,f and c+lat*2, f / c, f+long and c, f + long*2
        return grilla
    if hay_caja(grilla,c+lat,f+long) and hay_pared(grilla,c+lat*2,f+long*2):#c+lat,f and c+lat*2,f / c, f+long and c, f + long*2
        return grilla

    grilla_clon = clonar_grilla(grilla)
    
    '''
    Si tenemos una caja al lado y al lado de la caja hay un objetivo, obtenemos OBJETIVO_CAJA
    si no, si hay una caja al lado, y no hay objetivo al lado de la caja, obtenemos CAJA  
    En cualquier otro caso no se modifica la celda
    '''
    if hay_caja(grilla,c+lat,f+long) and hay_objetivo(grilla,c+lat*2,f+long*2):# c+lat,f and c+lat*2, f / c,f+long and c,f+long*2
        grilla_clon[f+long*2][c+lat*2] = OBJETIVO_CAJA # f, c+lat*2 / f+long*2 , c
    elif hay_caja(grilla,c+lat,f+long) and not hay_objetivo(grilla,c+lat*2,f+long*2):# c+lat, f and c+lat*2,f / c, f+long and c, f+long*2
        grilla_clon[f+long*2][c+lat*2] = CAJA # f, c+lat*2 / f+long*2 , c

    '''
    Si hay un objetivo en la siguiente casilla, estare sobre el objetivo
    De no haber objetivo solo estare parado sobre nada    
    '''
    if hay_objetivo(grilla,c+lat,f+long):
        grilla_clon[f+long][c+lat] = OBJETIVO_JUGADOR
    else:
        grilla_clon[f+long][c+lat] = JUGADOR

    '''
    Lo que voy a dejar atras cuando me mueva
    '''
    if hay_objetivo(grilla,c,f): 
        grilla_clon[f][c] = OBJETIVO
    else:
        grilla_clon[f][c] = VACIO

    return grilla_clon

def clonar_grilla(grilla):
    
    grilla_clon = []
    for fila in grilla:
        fila_clon = []
        for caracter in fila:
            fila_clon.append(caracter)
        grilla_clon.append(fila_clon)
    return grilla_clon

    
