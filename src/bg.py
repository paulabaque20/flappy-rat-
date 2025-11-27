import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Rat')

# -----------------------
# VARIABLES DEL JUEGO
# -----------------------
ground_scroll = 0
scroll_speed = 4

# -----------------------
# CARGAR IMÁGENES
# -----------------------
bg = pygame.image.load('assets/bg.png')
ground_img = pygame.image.load('assets/ground.png')


# ===============================
# 💗 MENÚ DE INICIO (AQUÍ MISMO)
# ===============================
menu = True
titulo_fuente = pygame.font.SysFont('Bauhaus 93', 90)
texto_fuente = pygame.font.SysFont('Bauhaus 93', 50)

while menu:
    # fondo
    screen.blit(bg, (0, 0))

    # Título bonito
    titulo = titulo_fuente.render("FLAPPY RAT", True, (255, 150, 200))
    screen.blit(titulo, (screen_width//2 - titulo.get_width()//2, 250))

    # Texto inicio
    iniciar = texto_fuente.render("CLICK PARA INICIAR", True, (255, 255, 255))
    screen.blit(iniciar, (screen_width//2 - iniciar.get_width()//2, 450))

    # Eventos del menú
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Salta al juego
            menu = False

    pygame.display.update()
    clock.tick(60)



# ===============================
# 🚀 LOOP PRINCIPAL DEL JUEGO
# ===============================
run = True
while run:

    clock.tick(fps)

    # ----- Fondo -----
    screen.blit(bg, (0, 0))

    # ----- Suelo animado -----
    screen.blit(ground_img, (ground_scroll, 768))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    # ----- Eventos -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
