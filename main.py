import csv
import soko
import gamelib

ANCHO_VENTANA = 384
ALTO_VENTANA = 448

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
                if not valor[:1] in soko.Caracteres:
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
            
        for cadena_de_caracteres in dic_niveles[clave]:

            if len(cadena_de_caracteres) < dimension[clave]:

                agregar = dimension[clave] - len(cadena_de_caracteres)
                fila_new = cadena_de_caracteres + agregar * ' '
                levels[clave].append(fila_new)

            else:
                levels[clave].append(cadena_de_caracteres)
    
    return levels               

'''
    Cargamos las teclas en un diccionario. Del tipo:
    click = {
            'w': 'NORTE',
            'a': 'OESTE',
            's': 'SUR',
            'd': 'ESTE',
            'r': 'REINICIAR',
            'Escape':
            'SALIR'}
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

    return click

'''
    CALCULAR DIMENSION DE LA VENTANA, SEGUN LA GRILLA QUE SE JUEGE
    ANCHO_VENTANA = Cantidad de columnas por 64 
    ALTO_VENTANA = Cantidad de filas por 64
'''
def amoldar_pantalla(grilla):
    ancho_ventana, alto_ventana =  soko.dimensiones(grilla)
    return ancho_ventana*64, alto_ventana*64

'''
    Quiero devolver que tipo de movimiento se hace al apretar cierta tecla
    Si la letra no pertenece a las mias del movimiento. Retorna None
'''
def detectar_movimiento(tecla_m, click):

    if tecla_m in click:
        return click[tecla_m]
    return

'''
    Aca todo empieza a fallar
'''

def juego_crear(archivo_niveles, archivo_teclas):

    levels = cargar_niveles(archivo_niveles)
    teclas = cargar_teclas(archivo_teclas)
    grilla = soko.crear_grilla(levels['Level 1'])
    juego = {
        'levels': levels,
        'teclas' : teclas,
        'grilla': grilla,
        'inicio': True
    }

    return juego
    

def juego_actualizar(grilla, juego, movimiento):
    
    direccion = detectar_movimiento(movimiento,juego['teclas'])

    if juego['inicio']:
        juego['inicio'] = False
    
    return soko.mover(grilla, direccion)

'''
    Mostramos el primer nivel por pantalla. Despues ver que onda
'''

def mostrar(grilla):

    c = 0
    for fila in grilla:
        
        f = 0
        for elemento in fila:
        
            if elemento == soko.PARED:
                gamelib.draw_image('img/ground.gif', f, c)
                gamelib.draw_image('img/wall.gif', f, c)
        
        
            if elemento == soko.CAJA:
                gamelib.draw_image('img/ground.gif', f, c)
                gamelib.draw_image('img/box.gif', f, c)
        

            if elemento == soko.JUGADOR:
                gamelib.draw_image('img/ground.gif', f, c)
                gamelib.draw_image('img/player.gif', f, c)

    
            if elemento == soko.OBJETIVO:
                gamelib.draw_image('img/ground.gif', f, c)
                gamelib.draw_image('img/goal.gif', f, c)


            if elemento == soko.OBJETIVO_CAJA:
                gamelib.draw_image('img/ground.gif', f, c)
                gamelib.draw_image('img/box.gif', f, c)
                gamelib.draw_image('img/goal.gif', f, c)
        

            if elemento == soko.OBJETIVO_JUGADOR:
                gamelib.draw_image('img/ground.gif', f, c)
                gamelib.draw_image('img/player.gif', f, c)
                gamelib.draw_image('img/goal.gif', f, c)
        
    
            if elemento == soko.VACIO:
                gamelib.draw_image('img/ground.gif', f, c)
        
            f += 64
        c += 64



def main():
    # Inicializar el estado del juego
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    juego = juego_crear('prueba.txt','teclas.txt')
    grilla = juego['grilla']
    click = juego['teclas']
    for linea in grilla:
        print(linea)

    while gamelib.is_alive():
        gamelib.draw_begin()

        '''
            Poner el piso abajo de las otras cosas por las uniones
        '''

        mostrar(grilla)

        # Dibujar la pantalla
        gamelib.draw_end()

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key
        grilla = juego_actualizar(grilla,juego,tecla)

        # Actualizar el estado del juego, según la `tecla` presionada

gamelib.init(main)