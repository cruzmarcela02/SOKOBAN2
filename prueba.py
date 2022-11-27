import csv
import soko
import gamelib


def cargar_niveles(archivo):
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
    niveles_archivo = {}
    dimension = {}
    with open (archivo, 'r') as archivo:
        lector = csv.reader(archivo)
        for linea in lector:

            if not linea:
                continue
            
            for valor in linea:
                if valor[:1] == "'":
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

def perfeccionar_grilla(dic_niveles, dimension):
    '''
        Recibe 2 diccionarios:
            1ro contiene los niveles del archivo
            2do contiene el ancho maximo de cada nivel
        Si las cadena de caracteres no tienen el ancho maximo, se rellena con ' ' 
    '''
    
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

#print(cargar_niveles('prueba.txt'))

def cargar_teclas(archivo):
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

#print(cargar_teclas('teclas.txt'))

def amoldar_pantalla(grilla):
    '''
        CALCULAR DIMENSION DE LA VENTANA, SEGUN LA GRILLA QUE SE JUEGE
        ANCHO_VENTANA = Cantidad de columnas por 64 
        ALTO_VENTANA = Cantidad de filas por 64
    '''
    ancho_ventana, alto_ventana =  soko.dimensiones(grilla)
    return ancho_ventana*64, alto_ventana*64

def detectar_movimiento(tecla_m, click):
    '''
        Quiero devolver que tipo de movimiento se hace al apretar cierta tecla
        Si la letra no pertenece a las mias del movimiento. Retorna None
    '''

    if tecla_m in click:
        return click[tecla_m]
    return

def juego_crear(archivo_niveles, archivo_teclas):
    '''
        Aca todo empieza a fallar
    '''

    levels = cargar_niveles(archivo_niveles)
    teclas = cargar_teclas(archivo_teclas)
    grilla = soko.crear_grilla(levels['Level 1'])
    ancho, alto = amoldar_pantalla(grilla)
    juego = {
        'levels': levels,
        'teclas' : teclas,
        'grilla': grilla,
        'inicio': True,
        'nivel' : 1,
        'ANCHO' : ancho,
        'ALTO' : alto
    }

    return juego

def juego_actualizar(grilla, juego, movimiento):
    '''
        El jugador se mueve en el tablero todo se ve bien, ahora veamos como avanzar entre los niveles
    '''
    
    direccion = detectar_movimiento(movimiento,juego['teclas'])
    print(direccion)

    if juego['inicio']:
        juego['inicio'] = False
    
    grilla = soko.mover(grilla, direccion)


    if soko.juego_ganado(grilla):
        return cambiar_de_nivel(grilla,juego)
    
    if direccion == 'REINICIAR':
        return reiniciar(grilla,juego)
    
    

    return grilla #soko.mover(grilla, direccion)

def mostrar(grilla):
    '''
        Mostramos el primer nivel por pantalla. Despues ver que onda
    '''

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

def cambiar_de_nivel(grilla,juego):
    '''
        Podemos cambiar del nivel1 al nivel 2
    '''
    
    if soko.juego_ganado(grilla):
        juego['nivel'] = juego.get('nivel',0) + 1
        nivel = juego['nivel']
        levels = juego ['levels']
        grilla = levels[f'Level {nivel}']
        ancho, alto = amoldar_pantalla(grilla)
        #print(ancho)
        #print(alto)
        juego['ANCHO'] = ancho
        juego['ALTO'] = alto
    return grilla

def reiniciar(grilla,juego):
    '''
        Reiniciar el nivel volver a la grilla inicial del nivel
    '''

    nivel = juego['nivel']
    levels = juego ['levels']
    grilla = levels[f'Level {nivel}']
    ancho, alto = amoldar_pantalla(grilla)
    juego['ANCHO'] = ancho
    juego['ALTO'] = alto
    return grilla

















def main():
    # Inicializar el estado del juego
    juego = juego_crear('prueba.txt','teclas.txt')
    gamelib.resize(juego['ANCHO'], juego['ALTO'])
    grilla = juego['grilla']
    for linea in grilla:
        print(linea)

    while gamelib.is_alive():
        gamelib.resize(juego['ANCHO'], juego['ALTO'])
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
        if tecla == 'Escape':
            break
        grilla = juego_actualizar(grilla,juego,tecla)

        # Actualizar el estado del juego, según la `tecla` presionada

gamelib.init(main)