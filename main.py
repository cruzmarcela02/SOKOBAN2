import soko
import gamelib

ANCHO_VENTANA = 300
ALTO_VENTANA = 300

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