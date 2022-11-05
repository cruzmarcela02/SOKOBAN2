import csv
import soko
import gamelib

ANCHO_VENTANA = 384
ALTO_VENTANA = 448
CARACTERES = ['#','$','@','.','*','+'," "]
ACCIONES = ['NORTE','SUR','ESTE',"OESTE",'REINICIAR','SALIR']

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
                if not valor[:1] in CARACTERES:
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

            click[tecla] = accion 
    return click

'''
    CALCULAR DIMENSION DE LA VENTANA
    ANCHO_VENTANA = ??
    ALTO_VENTANA = ??
'''
def juego_crear(archivo_niveles, archivo_teclas):

    levels = cargar_niveles(archivo_niveles)
    teclas = cargar_teclas(archivo_teclas)

    grilla = soko.crear_grilla(levels['Level 1'])

    return grilla

#print(juego_crear('prueba.txt','teclas.txt'))

def mostrar_juego(grilla):

    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0

    for elemento in grilla[0]:
        
        if elemento == '#':
            gamelib.draw_image('img/ground.gif', a, 0)
            gamelib.draw_image('img/wall.gif', a, 0)
        
        a += 64
        
    
    for elemento in grilla[0]:
        if elemento == '$':
            gamelib.draw_image('img/ground.gif', b, 0)
            gamelib.draw_image('img/box.gif', b, 0)
        
        b += 64

    for elemento in grilla[0]:
        if elemento == '@':
            gamelib.draw_image('img/ground.gif', c, 0)
            gamelib.draw_image('img/player.gif', c, 0)
        
        c += 64
    
    for elemento in grilla[0]:
        if elemento == '.':
            gamelib.draw_image('img/ground.gif', d, 0)
            gamelib.draw_image('img/goal.gif', d, 0)
        d += 64

    for elemento in grilla[0]:
        if elemento == '*':
            gamelib.draw_image('img/ground.gif', e, 0)
            gamelib.draw_image('img/goal.gif', e, 0)
            gamelib.draw_image('img/box.gif', e, 0)
        
        e += 64

    for elemento in grilla[0]:
        if elemento == '+':
            gamelib.draw_image('img/ground.gif', f, 0)
            gamelib.draw_image('img/goal.gif', f, 0)
            gamelib.draw_image('img/player.git',f,0)
        
        f += 64
    
    for elemento in grilla[0]:
        if elemento == soko.VACIO:
            gamelib.draw_image('img/ground.gif', g, 0)
        g += 64


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
                gamelib.draw_image('img/player.git', f, c)
                gamelib.draw_image('img/goal.gif', f, c)
        
    
            if elemento == soko.VACIO:
                gamelib.draw_image('img/ground.gif', f, c)
        
            f += 64
        c += 64



def main():
    # Inicializar el estado del juego

    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    grilla = juego_crear('prueba.txt','teclas.txt')
    print(grilla)

    while gamelib.is_alive():
        gamelib.draw_begin()

        '''
            Poner el piso abajo de las otras cosas por las uniones
        '''
        #mostrar_juego(grilla)

        mostrar(grilla)
        #gamelib.draw_image('img/ground.gif', 0, 0)
        #gamelib.draw_image('img/wall.gif', 0, 0)

        #gamelib.draw_image('img/ground.gif', 64, 0)
        #gamelib.draw_image('img/wall.gif', 64, 0)

        #gamelib.draw_image('img/ground.gif', 0, 64)
        #gamelib.draw_image('img/wall.gif', 0, 64)
        
        #gamelib.draw_image('img/ground.gif', 64, 64)
        #gamelib.draw_image('img/player.gif', 64, 64)

        # Dibujar la pantalla
        gamelib.draw_end()

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key
        # Actualizar el estado del juego, según la `tecla` presionada

gamelib.init(main)