import csv
import soko
import gamelib

IMAGENES = {
    '#': 'img/wall.gif',
    '$': 'img/box.gif',
    '@': 'img/player.gif',
    '.': 'img/goal.gif',
    ' ': 'img/ground.gif'
}
PIXELES = 64
COMILLA = "'"

def cargar_niveles(archivo):
    '''
        Se cargan los niveles y se arreglan los anchos para devolver el diccionario de los niveles.
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
    niveles_archivo = {}
    dimension = {}
    try:
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
                        niveles_archivo[nivel] = []
                        dimension[nivel] = 0
                    else:
                        niveles_archivo[nivel].append(valor)
                        
                        if len(valor) >= dimension[nivel]:
                            dimension[nivel] = len(valor)
        
            levels = perfeccionar_grilla(niveles_archivo,dimension)
        return levels
    except IOError as err:
        print(f'IO error: {err}')


def perfeccionar_grilla(niveles, dimension):
    '''
        Recibe 2 diccionarios:
            1ro contiene los niveles del archivo
            2do contiene el ancho maximo de cada nivel
        Si las cadena de caracteres no tienen el ancho maximo, se rellena con ' ' 
    '''
    levels = {}
    for clave in niveles:

        levels[clave]=[]
            
        for cadena in niveles[clave]:

            if len(cadena) < dimension[clave]:

                agregar = dimension[clave] - len(cadena)
                nueva_cadena = cadena + agregar * ' '
                levels[clave].append(nueva_cadena)

            else:
                levels[clave].append(cadena)
    
    return levels

print(cargar_niveles('niveles.txt'))

def cargar_teclas(archivo):
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
    click = {}
    try:
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
    except IOError as err:
        print(f'IO error: {err}')
    except IndexError as err_2:
        print(f'IndexError: {err_2} - El archivo puede estar mal redactado')



def amoldar_ventana(grilla):
    '''
        Se calcula la dimension de la ventana, segun la grilla a jugar:
        Las imgs son de 64 px
        ancho_ventana = Cantidad de columnas por 64 
        Idem para el Alto de la pantalla
    '''
    ancho_ventana, alto_ventana =  soko.dimensiones(grilla)
    return ancho_ventana*64, alto_ventana*64

def detectar_movimiento(tecla, click):
    '''
        Se devuelve la direccion en la que se movera segun la tecla.
        Si la letra no pertenece a las mias del movimiento. Retorna None
    '''

    if tecla in click:
        return click[tecla]
    return

def juego_crear(archivo_niveles, archivo_teclas):
    '''
        Inicializamos el juego:
            - Cargamos los niveles
            - Las teclas
            - E inicializamos el primer nivel
        retornamos un diccionario
    '''

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
        'nivel_nro' : 1,
    }

    return juego


def juego_actualizar(grilla, juego, tecla):
    '''
        El jugador se mueve en la grilla
        Cuando se gana cambiamos de grilla
        Si reiniciamos la grilla vuelve a su estado inicial
        Si nos movemos y seguimos jugando retorna un clon de la grilla (modificada)
    '''
    
    indicacion = detectar_movimiento(tecla,juego['teclas'])
    
    grilla = soko.mover(grilla, indicacion)

    if soko.juego_ganado(grilla):
        return cambiar_de_nivel(grilla,juego)
    
    if indicacion == 'REINICIAR':
        return reiniciar(grilla,juego)
    
    return grilla

def cambiar_de_nivel(grilla,juego):
    '''
        Si el nivel esta ganado:
            - incrementa un nivel
            - devuelve la grilla del nuevo nivel
            - modifica y reasigna las medidas de la ventana
            - si no se gano, devuelve la misma grilla
    '''
    
    if soko.juego_ganado(grilla):
        juego['nivel_nro'] = juego.get('nivel_nro',0) + 1
        nro = juego['nivel_nro']
        levels = juego ['levels']
        grilla = levels[f'Level {nro}']
        juego['ANCHO'], juego['ALTO'] = amoldar_ventana(grilla)
    return grilla


def mostrar(grilla):
    '''
        Mostramos la grilla
    '''
    columnas, filas = soko.dimensiones(grilla)
    
    for f in range(filas):
        for c in range(columnas):
            caracter = grilla[f][c]
            gamelib.draw_image(IMAGENES[' '], c*PIXELES, f*PIXELES)

            if caracter in IMAGENES:
                gamelib.draw_image(IMAGENES[caracter], c*PIXELES, f*PIXELES)
                
            if soko.hay_objetivo(grilla,c,f) and soko.hay_jugador(grilla,c,f):
                gamelib.draw_image(IMAGENES['@'], c*PIXELES, f*PIXELES)
                gamelib.draw_image(IMAGENES['.'], c*PIXELES, f*PIXELES)

            if soko.hay_objetivo(grilla,c,f) and soko.hay_caja(grilla,c,f):
                gamelib.draw_image(IMAGENES['$'], c*PIXELES, f*PIXELES)
                gamelib.draw_image(IMAGENES['.'], c*PIXELES, f*PIXELES)


'''
    Reinicia el nivel, vuelve a la grilla inicial del nivel
'''
def reiniciar(grilla,juego):

    nro = juego['nivel_nro']
    levels = juego ['levels']
    grilla = levels[f'Level {nro}']

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