# Importa la librería Pygame para el desarrollo del juego.
import pygame
# Importa todas las constantes de Pygame (como QUIT, K_SPACE) para usarlas directamente.
from pygame.locals import *

# Inicializa todos los módulos de Pygame necesarios para el entorno.
pygame.init()

# Crea un objeto Clock para ayudar a controlar la tasa de frames.
clock = pygame.time.Clock()
# Define la cantidad de cuadros por segundo (Frames Per Second) deseada.
fps = 60

# Define el ancho de la ventana del juego en píxeles.
screen_width = 864
# Define la altura de la ventana del juego en píxeles.
screen_height = 936

# Crea la superficie de dibujo principal (la ventana) con las dimensiones definidas.
screen = pygame.display.set_mode((screen_width, screen_height))
# 1. Título 
# Asigna el texto 'Flappy Rat' a la barra de título de la ventana.
pygame.display.set_caption('Flappy Rat') 


#define game variables
# Inicializa una variable para rastrear la posición horizontal de desplazamiento del suelo.
ground_scroll = 0
# Define la velocidad constante a la que se desplazarán los elementos del juego (scroll).
scroll_speed = 4

#load images
# 2. Rutas corregidas a 'assets/'
# Carga la imagen de fondo (background) desde el archivo especificado.
bg = pygame.image.load('assets/bg.png')
# Carga la imagen del suelo (ground) desde el archivo especificado.
ground_img = pygame.image.load('assets/ground.png')

# Variable booleana que controla si el bucle principal debe continuar.
run = True
# Bucle principal del juego
while run:

    # Limita la velocidad del bucle a los 60 FPS definidos.
    clock.tick(fps)

    #draw background
    # Dibuja la imagen de fondo (bg) en la posición (0,0).
    screen.blit(bg, (0,0))

    #draw and scroll the ground
    # Dibuja la imagen del suelo, usando 'ground_scroll' para el movimiento horizontal.
    screen.blit(ground_img, (ground_scroll, 768))
    # Mueve la posición del scroll del suelo hacia la izquierda.
    ground_scroll -= scroll_speed
    # Comprueba si el desplazamiento horizontal ha superado el límite del patrón.
    if abs(ground_scroll) > 35:
        # Si se cumple, reinicia la posición del scroll a 0 para crear un bucle visual continuo.
        ground_scroll = 0


    # Itera sobre todos los eventos que han ocurrido.
    for event in pygame.event.get():
        # Comprueba si el evento es el de cerrar la ventana (QUIT).
        if event.type == pygame.QUIT:
            # Si el evento es QUIT, establece 'run' en False para finalizar el bucle.
            run = False

    # Actualizar la pantalla
    # Muestra en pantalla todo lo que se ha dibujado en el ciclo actual.
    pygame.display.update()

# Finaliza Pygame y cierra la ventana del juego una vez que el bucle termina.
pygame.quit()