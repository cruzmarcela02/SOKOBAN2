import csv
import soko
CARACTERES = ['#','$','@','.','*','+'," "]

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

#n, d = cargar_niveles('prueba.txt')
#print(n)
#print(d)

def perfeccionar_grilla(dic_niveles, dimension):
    
    niveles_perfeccionados = {}
    for clave in dic_niveles:

        niveles_perfeccionados[clave]=[]
            
        for cadena_de_caracteres in dic_niveles[clave]:

            if len(cadena_de_caracteres) < dimension[clave]:

                agregar = dimension[clave] - len(cadena_de_caracteres)
                fila_new = cadena_de_caracteres + agregar * ' '
                niveles_perfeccionados[clave].append(fila_new)

            else:
                niveles_perfeccionados[clave].append(cadena_de_caracteres)
    
    return niveles_perfeccionados               

#niveles = perfeccionar_grilla(n,d)
#print(niveles)

def niveles_del_juego(archivo):
    level, dimension = cargar_niveles(archivo)
    level = perfeccionar_grilla(level,dimension)
    return level

#print(niveles_del_juego('prueba.txt'))


def juego_mostrar(archivo):

    levels = niveles_del_juego(archivo)
    for nivel in levels:
        grilla = soko.crear_grilla(levels['Level 1'])
        print(grilla)

juego_mostrar('prueba.txt')

def cargar(archivo):
    n_nivel = 0
    level = {}
    dimension = 0
    with open (archivo,'r') as niveles: # Abrimos el archivo como - niveles
        for linea in niveles: # Recorremos cada linea de -niveles-
            linea = linea.rstrip('\n') # Le sacamos la \n de cada fin de linea
            
            for caracter in linea[:1]:



                if not caracter in CARACTERES:
                    n_nivel += 1
                else:    
                    level[n_nivel] = level.get(n_nivel,[])
                    level[n_nivel].append(linea)
                    if len(linea) >= dimension:
                        dimension = len(linea)

        print(f'la linea mas larga mide {dimension}' )

    print(level, dimension)
#cargar('prueba.txt')