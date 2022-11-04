import soko
import gamelib

ANCHO_VENTANA = 300
ALTO_VENTANA = 300

def cargar_niveles(archivo):
    level = {}
    dimension = {}
    with open (archivo, 'r') as archivo:
        lector = csv.reader(archivo)
        for linea in lector:

            if not linea:
                continue
            
            for valor in linea:
                if not valor[:1] in CARACTERES:
                    nivel = valor
                    level[nivel] = level.get(valor,[])
                    dimension[nivel] = dimension.get(valor,0)
                else:
                    level[nivel].append(valor)
                    
                    if len(valor) >= dimension[nivel]:
                        dimension[nivel] = len(valor)
    
    return level, dimension

def perfeccionar_grilla(dic_niveles, dimension):
    
    niveles_perfeccionados = {}
    for clave in dic_niveles:

        niveles_perfeccionados[clave]=[]
            
        for cadena_de_caracteres in dic_niveles[clave]:

            if len(cadena_de_caracteres) < dimension[clave]:

                print(dimension[clave])
                agregar = dimension[clave] - len(cadena_de_caracteres)
                fila_new = cadena_de_caracteres + agregar * ' '
                niveles_perfeccionados[clave].append(fila_new)

            else:
                niveles_perfeccionados[clave].append(cadena_de_caracteres)
    
    return niveles_perfeccionados               

def niveles_del_juego(archivo):
    level, dimension = cargar_niveles(archivo)
    level = perfeccionar_grilla(level,dimension)
    return level
    
def juego_mostrar(niveles):

    #for nivel in niveles:
    grilla = soko.crear_grilla(niveles[nivel])
    print(perfeccionar_grilla)    

def main():
    # Inicializar el estado del juego

    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)

    while gamelib.is_alive():
        gamelib.draw_begin()
        # Dibujar la pantalla
        gamelib.draw_end()

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key
        # Actualizar el estado del juego, según la `tecla` presionada

gamelib.init(main)