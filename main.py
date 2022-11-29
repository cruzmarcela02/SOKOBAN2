import csv
import soko
import gamelib
import pila
import cola

IMAGENES = {
    '#': 'img/wall.gif',
    '$': 'img/box.gif',
    '@': 'img/player.gif',
    '.': 'img/goal.gif',
    ' ': 'img/ground.gif'
}
PX = 64
COMILLA = "'"

REHACER = 'REHACER'
DESHACER = 'DESHACER'
REINICIAR = 'REINICIAR'
SALIR = 'SALIR'
PISTA = 'HELP'
DIRECCIONES = [soko.ESTE, soko.OESTE, soko.NORTE, soko.SUR]


def perfeccionar_grilla(niveles, dimension):
    '''
        Recibe el diccionario de niveles y el de dimension:
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
                if accion == REINICIAR or accion == SALIR or accion == DESHACER or accion == REHACER or accion == PISTA:
                    click[tecla] = accion
        return click
    except IOError as err:
        print(f'IO error: {err}')
    except IndexError as err_2:
        print(f'IndexError: {err_2} - El archivo puede estar mal redactado')

def amoldar_ventana(grilla):
    '''
        Se calcula la dimension de la ventana, segun la grilla a jugar:
        ancho_ventana = Cantidad de columnas por 64 (Idem para el Alto de la pantalla)
    '''
    ancho_ventana, alto_ventana =  soko.dimensiones(grilla)
    return ancho_ventana*PX, alto_ventana*PX

def detectar_accion(tecla, click):
    '''
        Devuelve la accion a realizar segun la tecla.
        Si la letra no esta en el diccionario retorna None
    '''
    if tecla in click:
        return click[tecla]
    return

def deshacer(grilla_actual, juego):
    p_deshacer = juego['deshacer']
    
    if p_deshacer.esta_vacia():
        return grilla_actual

    p_rehacer = juego ['rehacer']
    p_rehacer.apilar(grilla_actual)
    return p_deshacer.desapilar()

def rehacer(grilla_actual,juego):
    p_rehacer = juego['rehacer']

    if p_rehacer.esta_vacia():
        return grilla_actual

    p_deshacer = juego['deshacer']
    p_deshacer.apilar(grilla_actual)
    return p_rehacer.desapilar()

def guardar_movimiento(grilla, juego):
    juego['deshacer'].apilar(grilla)
    if not juego['rehacer'].esta_vacia():
        juego['rehacer'] = pila.Pila()

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

    p_rehacer = pila.Pila()
    p_deshacer = pila.Pila()

    juego = {
        'levels': levels,
        'teclas' : teclas,
        'grilla': grilla,
        'ANCHO' : ancho,
        'ALTO' : alto,
        'lvl_nro' : 1,
        'rehacer': p_rehacer,
        'deshacer': p_deshacer,
        'hay_pistas': False,
        'cola_pistas': cola.Cola()
    }

    return juego

def cargar_pistas(lista_pistas,juego):
    print(lista_pistas)
    for pista in lista_pistas:
        juego['cola_pistas'].encolar(pista)
    return juego['cola_pistas']

def juego_actualizar(grilla, juego, tecla):
    '''
        Obtenemos la indicacion, puede:
            Moverse o Reiniciar el nivel 
        Si gana el nivel avanza al siguiente, si no se actualiza la grilla en forma de clon
    '''
    indicacion = detectar_accion(tecla,juego['teclas'])

    if indicacion == PISTA:
        if not juego['hay_pistas']:
            juego['hay_pistas'], pistas = buscar_solucion(grilla)
            print("termine de buscar")
            print(juego['hay_pistas'])
            print(pistas)
            if juego['hay_pistas']:
                juego['cola_pistas'] = cargar_pistas(pistas, juego)
            return grilla
        
        else:
            indicacion = juego['cola_pistas'].desencolar()
            guardar_movimiento(grilla,juego)
            grilla = soko.mover(grilla, indicacion)
            if soko.juego_ganado(grilla):
                return cambiar_de_nivel(grilla,juego)
            return grilla

    
    if indicacion == REINICIAR:
        return reiniciar(grilla,juego)
    
    if indicacion == DESHACER:
        #apilar en ESTADO actual en REAHACER
        grilla = deshacer(grilla,juego)
        return grilla
    
    if indicacion == REHACER:
        grilla = rehacer(grilla,juego)
        return grilla

    #Reiniciamos el Rehacer
    

    #apilas el estado anterior en DESHACER
    guardar_movimiento(grilla,juego)

    grilla = soko.mover(grilla, indicacion)

    juego['cola_pistas'] = cola.Cola()
    juego['hay_pistas'] = False
    
    if soko.juego_ganado(grilla):
        return cambiar_de_nivel(grilla,juego)
    

    return grilla

def reiniciar(grilla,juego):
    '''
        Reinicia el nivel, vuelve a la grilla inicial del nivel
    '''
    nro = juego['lvl_nro']
    levels = juego ['levels']
    grilla = levels[f'Level {nro}']
    juego['rehacer'] = pila.Pila()
    juego['deshacer'] = pila.Pila()
    juego['cola_pista'] = cola.Cola()
    juego['hay_pistas'] = False
    return grilla

def cambiar_de_nivel(grilla,juego):
    '''
        Si el nivel esta ganado:
            - incrementa un nro de nivel
            - devuelve la grilla del nuevo nivel
            - modifica y reasigna las medidas de la ventana
            - si no se gano, devuelve la misma grilla
    '''
    if soko.juego_ganado(grilla):
        juego['lvl_nro'] = juego.get('lvl_nro',0) + 1
        nro = juego['lvl_nro']
        levels = juego ['levels']
        grilla = levels[f'Level {nro}']
        juego['rehacer'] = pila.Pila()
        juego['deshacer'] = pila.Pila()
        juego['cola_pista'] = cola.Cola()
        juego['hay_pistas'] = False
        juego['ANCHO'], juego['ALTO'] = amoldar_ventana(grilla)

    return grilla

def buscar_solucion(estado_inicial):
    visitados = set()
    return backtrack(estado_inicial, visitados)

def backtrack(estado,visitados):
    print("buscando...")
    agregar(visitados, estado)
    if soko.juego_ganado(estado):
        # ¡encontramos la solución!
        return True, []
    
    for movimiento in DIRECCIONES:
        nuevo_estado = soko.mover(estado, movimiento)
        nuevo_estado_transformado = tranformar_a_cadena(nuevo_estado)
        if nuevo_estado_transformado in visitados:
            continue
        solucion_encontrada, acciones = backtrack(nuevo_estado,visitados)
        if solucion_encontrada:
            return True, [movimiento] + acciones
    return False, None

def agregar(visitados, estado):
    cadena_estado = tranformar_a_cadena(estado)
    visitados.add(cadena_estado)

def tranformar_a_cadena(estado):
    columnas, filas = soko.dimensiones(estado)
    cadena = ''
    for f in range(filas):
        for c in range(columnas):
            caracter = estado[f][c]
            cadena += caracter
        cadena = cadena + '\n'
    return cadena

def mostrar(grilla):
    '''
        Mostramos la grilla
    '''
    columnas, filas = soko.dimensiones(grilla)
    
    for f in range(filas):
        for c in range(columnas):
            caracter = grilla[f][c]
            gamelib.draw_image(IMAGENES[soko.VACIO], c*PX, f*PX)

            if caracter in IMAGENES:
                gamelib.draw_image(IMAGENES[caracter], c*PX, f*PX)
                
            if soko.hay_objetivo(grilla,c,f) and soko.hay_jugador(grilla,c,f):
                gamelib.draw_image(IMAGENES[soko.JUGADOR], c*PX, f*PX)
                gamelib.draw_image(IMAGENES[soko.OBJETIVO], c*PX, f*PX)

            if soko.hay_objetivo(grilla,c,f) and soko.hay_caja(grilla,c,f):
                gamelib.draw_image(IMAGENES[soko.CAJA], c*PX, f*PX)
                gamelib.draw_image(IMAGENES[soko.OBJETIVO], c*PX, f*PX)

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