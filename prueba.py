import csv
import soko
import gamelib

ANCHO_VENTANA = 300
ALTO_VENTANA = 300
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
    Quiero leer las teclas
'''
def leer_teclas(archivo):
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
            #if not tecla in click:
            #    click[tecla] = accion
    
    return click
#print(leer_teclas('teclas.txt')) 
