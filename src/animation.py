# Importa la librería Pygame para el desarrollo del juego.
import pygame
# Importa todas las constantes de Pygame (como QUIT).
from pygame.locals import *

# Inicializa todos los módulos de Pygame.
pygame.init()

# Crea un objeto Clock para controlar la velocidad.
clock = pygame.time.Clock()
# --- AJUSTE DE VELOCIDAD 1: FLUJO ---
# Define la tasa de fotogramas (FPS). Un valor más alto (90) se siente más rápido y fluido que 60.
fps = 90

# --- CONFIGURACIÓN DE PANTALLA ---
screen_width = 864
screen_height = 936

# Crea la ventana principal.
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Rat') 

# --- VARIABLES DE JUEGO ---
scroll_suelo = 0
# --- AJUSTE DE VELOCIDAD 2: MOVIMIENTO HORIZONTAL ---
# Define la velocidad constante de desplazamiento (scroll). 
# Un valor de 8 mueve los objetos más rápido que el valor inicial de 4.
velocidad_scroll = 8 

# Cargar imágenes 
bg = pygame.image.load('assets/bg.png')
img_suelo = pygame.image.load('assets/ground.png')

# --- BUCLE PRINCIPAL DEL JUEGO ---
run = True
while run:

    # Limita la velocidad del bucle a los FPS definidos (90).
    clock.tick(fps)

    # Dibuja el fondo.
    screen.blit(bg, (0,0))

    # Dibuja el suelo en movimiento.
    screen.blit(img_suelo, (scroll_suelo, 768))
    
    # Mueve el suelo hacia la izquierda con la velocidad ajustada.
    scroll_suelo -= velocidad_scroll
    
    # Reinicia el scroll para el bucle continuo.
    if abs(scroll_suelo) > 35:
        scroll_suelo = 0

    # Manejar eventos.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Actualizar la pantalla para mostrar los cambios.
    pygame.display.update()

# Finaliza Pygame.
pygame.quit()