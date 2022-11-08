import csv
import soko
import gamelib

PIXELES = 64
COMILLA = "'"

'''
    Se cargan los niveles tan cual estan en el archivo.
    Se arreglan los anchos, y devuelve el diccionario de los niveles.
    Con la estructura:
        levels:{
            'Level 1' : ['####  ',
                         '# .#  ',
                         '#  ###',
                         '#*@  #',
                         '#  $ #',
                         '#  ###',
                         '####  ']
        }
    Se omiten los titulos de los niveles como del 147 en adelante
'''
def cargar_niveles(archivo):
    niveles_archivo = {}
    dimension = {}
    with open (archivo, 'r') as archivo:
        lector = csv.reader(archivo)
        for linea in lector:

            if not linea:
                continue
            
            for valor in linea:
                if valor[:1] == COMILLA:
                    continue

                if valor[:1] == 'L':
                    nivel = valor
                    niveles_archivo[nivel] = niveles_archivo.get(valor,[])
                    dimension[nivel] = dimension.get(valor,0)
                else:
                    niveles_archivo[nivel].append(valor)
                    
                    if len(valor) >= dimension[nivel]:
                        dimension[nivel] = len(valor)
    
        levels = perfeccionar_grilla(niveles_archivo,dimension)
    return levels

'''
    Recibe 2 diccionarios:
        1ro contiene los niveles del archivo
        2do contiene el ancho maximo de cada nivel
    Si las cadena de caracteres no tienen el ancho maximo, se rellena con ' ' 
'''

def perfeccionar_grilla(dic_niveles, dimension):
    
    levels = {}
    for clave in dic_niveles:

        levels[clave]=[]
            
        for cadena in dic_niveles[clave]:

            if len(cadena) < dimension[clave]:

                agregar = dimension[clave] - len(cadena)
                nueva_cadena = cadena + agregar * ' '
                levels[clave].append(nueva_cadena)

            else:
                levels[clave].append(cadena)
    
    return levels

#print(cargar_niveles('prueba.txt'))

'''
    Cargamos las teclas en un diccionario. Del tipo:
    click = {
            'w': (0,-1), 
            'a': (-1,0),
            's': (0,1),
            'd': (1,0),
            'r': 'REINICIAR',
            'Escape':'SALIR'
            }
'''
def cargar_teclas(archivo):
    click = {}
    with open (archivo, 'r') as teclas:
        for linea in teclas:

            linea = linea.rstrip('\n')
            tecla_accion = linea.split(' = ')

            if not tecla_accion[0] or not tecla_accion[1]:
                continue
            else:
                tecla = tecla_accion[0]
                accion = tecla_accion[1]
            
            if accion == 'NORTE':
                click[tecla] = soko.NORTE
            if accion == 'OESTE':
                click[tecla] = soko.OESTE
            if accion == 'ESTE':
                click[tecla] = soko.ESTE
            if accion == 'SUR':
                click[tecla] = soko.SUR
            if accion == 'REINICIAR' or accion == 'SALIR':
                click[tecla] = accion

    return click

print(cargar_teclas('teclas.txt'))

'''
    Se calcula la dimension de la ventana, segun la grilla a jugar:
    Las imgs son de 64 px
    ancho_ventana = Cantidad de columnas por 64 
    Idem para el Alto de la pantalla
'''
def amoldar_ventana(grilla):
    ancho_ventana, alto_ventana =  soko.dimensiones(grilla)
    return ancho_ventana*64, alto_ventana*64

'''
    Se devuelve la direccion en la que se movera segun la tecla.
    Si la letra no pertenece a las mias del movimiento. Retorna None
'''
def detectar_movimiento(tecla, click):

    if tecla in click:
        return click[tecla]
    return

'''
    Inicializamos el juego:
        - Cargamos los niveles
        - Las teclas
        - E inicializamos el primer nivel
    retornamos un diccionario
'''
def juego_crear(archivo_niveles, archivo_teclas):

    levels = cargar_niveles(archivo_niveles)
    teclas = cargar_teclas(archivo_teclas)

    grilla = soko.crear_grilla(levels['Level 1'])
    ancho, alto = amoldar_ventana(grilla)
    juego = {
        'levels': levels,
        'teclas' : teclas,
        'grilla': grilla,
        'ANCHO' : ancho,
        'ALTO' : alto,
        'nivel' : 1,
        'inicio': True,
    }

    return juego

'''
    El jugador se mueve en la grilla
    Cuando se gana cambiamos de grilla
    Si reiniciamos la grilla vuelve a su estado inicial
    Si nos movemos y seguimos jugando retorna un clon de la grilla (modificada)
'''

def juego_actualizar(grilla, juego, movimiento):
    
    direccion = detectar_movimiento(movimiento,juego['teclas'])

    if juego['inicio']:
        juego['inicio'] = False
    
    grilla = soko.mover(grilla, direccion)

    if soko.juego_ganado(grilla):
        return cambiar_de_nivel(grilla,juego)
    
    if direccion == 'REINICIAR':
        return reiniciar(grilla,juego)
    
    return grilla

'''
    Si el nivel esta ganado:
        - incrementa un nivel
        - devuelve la grilla del nuevo nivel
        - modifica y reasigna las medidas de la ventana
        - si no se gano, devuelve la misma grilla
'''
def cambiar_de_nivel(grilla,juego):
    
    if soko.juego_ganado(grilla):
        juego['nivel'] = juego.get('nivel',0) + 1
        nivel = juego['nivel']
        levels = juego ['levels']
        grilla = levels[f'Level {nivel}']
        juego['ANCHO'], juego['ALTO'] = amoldar_ventana(grilla)
    return grilla

'''
    Mostramos la grilla
'''

def mostrar(grilla):

    c = 0
    for fila in grilla:
        
        f = 0
        for elemento in fila:

            gamelib.draw_image('img/ground.gif', f, c)
            if elemento == soko.PARED:
                gamelib.draw_image('img/wall.gif', f, c)
        
            if elemento == soko.CAJA:
                gamelib.draw_image('img/box.gif', f, c)
        
            if elemento == soko.JUGADOR:
                gamelib.draw_image('img/player.gif', f, c)

            if elemento == soko.OBJETIVO:
                gamelib.draw_image('img/goal.gif', f, c)

            if elemento == soko.OBJETIVO_CAJA:
                gamelib.draw_image('img/box.gif', f, c)
                gamelib.draw_image('img/goal.gif', f, c)

            if elemento == soko.OBJETIVO_JUGADOR:
                gamelib.draw_image('img/player.gif', f, c)
                gamelib.draw_image('img/goal.gif', f, c)
        
            f += PIXELES
        c += PIXELES

'''
    Reinicia el nivel, vuelve a la grilla inicial del nivel
'''
def reiniciar(grilla,juego):

    nivel = juego['nivel']
    levels = juego ['levels']
    grilla = levels[f'Level {nivel}']

    return grilla

def main():
    # Inicializar el estado del juego
    gamelib.title('SOKOBAN 2: LA VENGANZA')
    juego = juego_crear('niveles.txt','teclas.txt')
    gamelib.resize(juego['ANCHO'], juego['ALTO'])
    grilla = juego['grilla']

    while gamelib.is_alive():

        gamelib.resize(juego['ANCHO'], juego['ALTO'])
        
        gamelib.draw_begin()

        mostrar(grilla)

        gamelib.draw_end()

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key

        if tecla == 'Escape':
            break

        grilla = juego_actualizar(grilla,juego,tecla)

        # Actualizar el estado del juego, según la `tecla` presionada

gamelib.init(main)