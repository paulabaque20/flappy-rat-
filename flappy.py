import pygame
from pygame.locals import *
import random
import os
import sys
import math

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Rat')

# -----------------------
# Fuentes y colores
# -----------------------
fuente = pygame.font.SysFont('Bauhaus 93', 60)
fuente_pequena = pygame.font.SysFont('Bauhaus 93', 30)
blanco = (255, 255, 255)
negro = (0, 0, 0)

# -----------------------
# VARIABLES DEL JUEGO
# -----------------------
scroll_suelo = 0
velocidad_scroll = 4
volando = False
juego_terminado = False
tubo_gap = 150
frecuencia_tubo = 1500
ultimo_tubo = pygame.time.get_ticks() - frecuencia_tubo
puntuacion = 0
paso_tubo = False

# Música (intenta cargar, si no imprime aviso)
MUSICA_FONDO_PATH = os.path.join("assets", "musica_fondo.mp3")
try:
    pygame.mixer.music.load(MUSICA_FONDO_PATH)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
except Exception:
    print("AVISO: No se pudo cargar la música.")

# -----------------------
# CARGAR IMÁGENES (optimizado)
# -----------------------
# background: convert() para acelerar el blit
try:
    bg = pygame.image.load('assets/bg.png').convert()
except Exception:
    bg = pygame.Surface((screen_width, screen_height)).convert()
    bg.fill((120, 200, 255))
    print("AVISO: No se pudo cargar 'assets/bg.png'")

try:
    img_suelo = pygame.image.load('assets/ground.png').convert_alpha()
except Exception:
    img_suelo = pygame.Surface((screen_width, 168), pygame.SRCALPHA).convert_alpha()
    pygame.draw.rect(img_suelo, (80, 50, 30), img_suelo.get_rect())
    print("AVISO: No se pudo cargar 'assets/ground.png'")

try:
    img_boton = pygame.image.load('assets/restart.png').convert_alpha()
except Exception:
    img_boton = pygame.Surface((100, 50), pygame.SRCALPHA).convert_alpha()
    pygame.draw.rect(img_boton, (200, 50, 80), img_boton.get_rect(), border_radius=8)
    print("AVISO: No se pudo cargar 'assets/restart.png'")

# -----------------------
# FUNCIONES UTILES
# -----------------------
def dibujar_texto(texto, fuente_local, color_texto, x, y):
    img = fuente_local.render(texto, True, color_texto)
    screen.blit(img, (x, y))


def reiniciar_juego():
    global puntuacion, ultimo_tubo, paso_tubo
    grupo_tubo.empty()
    flappy_rat.rect.x = 100
    flappy_rat.rect.y = int(screen_height / 2)
    puntuacion = 0
    ultimo_tubo = pygame.time.get_ticks() - frecuencia_tubo
    paso_tubo = False
    return puntuacion


# ------------------------------------
# CLASE DEL PERSONAJE: Rat
# ------------------------------------
class Rat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.contador = 0

        # Pre-cargar imágenes con convert_alpha para velocidad
        for num in range(1, 4):
            try:
                img_original = pygame.image.load(f"assets/rat{num}.png").convert_alpha()
            except Exception:
                # placeholder si falta
                img_original = pygame.Surface((48, 34), pygame.SRCALPHA).convert_alpha()
                pygame.draw.ellipse(img_original, (255, 160, 200), img_original.get_rect())
            width = img_original.get_width()
            height = img_original.get_height()
            img_reescalada = pygame.transform.scale(img_original, (int(width * 0.6), int(height * 0.6)))
            self.images.append(img_reescalada)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.cliqueado = False

    def update(self):
        global volando, juego_terminado

        if volando:
            # gravedad
            self.vel += 0.4
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if not juego_terminado:
            # salto
            if pygame.mouse.get_pressed()[0] == 1 and not self.cliqueado:
                self.cliqueado = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.cliqueado = False

            enfriamiento_aleteo = 5
            self.contador += 1

            if self.contador > enfriamiento_aleteo:
                self.contador = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]

            # rotar imagen (rotación por frame ya cargado)
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Tubo(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load("assets/tubos.png").convert_alpha()
        except Exception:
            self.image = pygame.Surface((80, 600), pygame.SRCALPHA).convert_alpha()
            pygame.draw.rect(self.image, (80, 180, 80), self.image.get_rect())
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(tubo_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(tubo_gap / 2)]

    def update(self):
        self.rect.x -= velocidad_scroll
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        accion = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                accion = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return accion


# Grupos y sprites
grupo_tubo = pygame.sprite.Group()
grupo_rat = pygame.sprite.Group()

flappy_rat = Rat(100, int(screen_height / 2))
grupo_rat.add(flappy_rat)

boton_reinicio = Button(screen_width // 2 - 50, screen_height // 2 - 100, img_boton)

# -------------------------
# MENÚ DE INICIO (FLAPPY-BIRD STYLE)
# -------------------------
en_menu = True

# Fuentes del menú
titulo_fuente = pygame.font.SysFont('Bauhaus 93', 96)
fuente_menu = pygame.font.SysFont('Bauhaus 93', 44)

# Colores para letras arcoíris
colores_titulo = [
    (255, 100, 200),
    (255, 180, 120),
    (255, 255, 120),
    (140, 220, 180),
    (140, 170, 255),
    (200, 150, 255)
]

t_menu = 0.0  # tiempo para animación del título

# -------------------------
# PRE-RENDER DEL TÍTULO Y TEXTOS (para mejorar performance)
# -------------------------
titulo = "FLAPPY RAT"
# render por letra (precalcular superficies)
title_surfaces = []
for i, letra in enumerate(titulo):
    surf = titulo_fuente.render(letra, True, colores_titulo[i % len(colores_titulo)])
    title_surfaces.append(surf)

texto_iniciar_surf = fuente_menu.render("Haz clic en JUGAR o pulsa Espacio", True, blanco)
txt_jugar = fuente_menu.render("JUGAR", True, blanco)
txt_salir = fuente_menu.render("SALIR", True, blanco)

# -------------------------
# MINI-IMAGEN DEL MENÚ (USAR "assets/menu_rat.png" si existe)
# -------------------------
mini_image = None
try:
    # si el usuario puso una imagen personalizada para el menú
    mini_image_raw = pygame.image.load('assets/menu_rat.png').convert_alpha()
    # escalar a tamaño apropiado una vez
    mini_image = pygame.transform.smoothscale(mini_image_raw, (int(mini_image_raw.get_width()*0.9),
                                                               int(mini_image_raw.get_height()*0.9)))
except Exception:
    # si no existe, usar el primer frame del flappy_rat ya cargado (pre-escalado)
    try:
        base = flappy_rat.images[0]
        mini_image = pygame.transform.smoothscale(base, (int(base.get_width()*0.9), int(base.get_height()*0.9)))
    except Exception:
        mini_image = None

# -------------------------
# BUCLE DEL MENÚ
# -------------------------
while en_menu:
    clock.tick(fps)
    t_menu += 0.06

    # dibujar fondo y suelo estático de menú
    screen.blit(bg, (0, 0))
    screen.blit(img_suelo, (0, 768))

    # animación y título multicolor (cada letra con color distinto)
    x_start = screen_width // 2 - (len(titulo) * 34) // 2
    bounce = int(math.sin(t_menu) * 8)

    # en lugar de renderizar en cada frame, usamos las surfaces precalculadas
    for i, surf in enumerate(title_surfaces):
        screen.blit(surf, (x_start + i * 46, 140 + bounce + (i % 2) * 4))

    # texto pequeño de ayuda (pre-rendered)
    screen.blit(texto_iniciar_surf, (screen_width // 2 - texto_iniciar_surf.get_width() // 2, 360 + bounce // 2))

    # dibujar botones simples (rectángulos) - visual y detección
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    jugar_rect = pygame.Rect(screen_width // 2 - 140, 420, 280, 80)
    salir_rect = pygame.Rect(screen_width // 2 - 140, 520, 280, 80)

    # efecto hover
    if jugar_rect.collidepoint(mouse):
        pygame.draw.rect(screen, (255, 120, 180), jugar_rect, border_radius=18)
    else:
        pygame.draw.rect(screen, (220, 80, 140), jugar_rect, border_radius=18)

    if salir_rect.collidepoint(mouse):
        pygame.draw.rect(screen, (180, 180, 180), salir_rect, border_radius=18)
    else:
        pygame.draw.rect(screen, (120, 120, 120), salir_rect, border_radius=18)

    # dibujar texto de botones (pre-rendered)
    screen.blit(txt_jugar, (jugar_rect.x + jugar_rect.width // 2 - txt_jugar.get_width() // 2,
                             jugar_rect.y + jugar_rect.height // 2 - txt_jugar.get_height() // 2))
    screen.blit(txt_salir, (salir_rect.x + salir_rect.width // 2 - txt_salir.get_width() // 2,
                             salir_rect.y + salir_rect.height // 2 - txt_salir.get_height() // 2))

    # dibujar una mini animación del flappy_rat en el menú (flotando) - solo mover la posición
    if mini_image:
        mini_x = screen_width // 2 - 260
        mini_y = 220 + int(math.cos(t_menu) * 8)
        screen.blit(mini_image, (mini_x, mini_y))

    # eventos del menú
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if jugar_rect.collidepoint(event.pos):
                en_menu = False
            if salir_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                en_menu = False

    pygame.display.update()

# -------------------------
# LOOP PRINCIPAL DEL JUEGO
# -------------------------
run = True
while run:

    clock.tick(fps)
    fps_actual = int(clock.get_fps())

    screen.blit(bg, (0, 0))

    grupo_tubo.draw(screen)
    grupo_rat.draw(screen)
    grupo_rat.update()

    screen.blit(img_suelo, (scroll_suelo, 768))

    # puntuación
    if len(grupo_tubo) > 0:
        if grupo_rat.sprites()[0].rect.left > grupo_tubo.sprites()[0].rect.left \
                and grupo_rat.sprites()[0].rect.right < grupo_tubo.sprites()[0].rect.right \
                and paso_tubo == False:
            paso_tubo = True
        if paso_tubo == True:
            if grupo_rat.sprites()[0].rect.left > grupo_tubo.sprites()[0].rect.right:
                puntuacion += 1
                paso_tubo = False

    dibujar_texto(str(puntuacion), fuente, blanco, int(screen_width / 2), 20)
    dibujar_texto(f"FPS: {fps_actual}", fuente_pequena, negro, 10, 10)

    if pygame.sprite.groupcollide(grupo_rat, grupo_tubo, False, False) or flappy_rat.rect.top < 0:
        juego_terminado = True

    if flappy_rat.rect.bottom >= 768:
        juego_terminado = True
        volando = False

    if volando == True and juego_terminado == False:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - ultimo_tubo > frecuencia_tubo:
            altura_tubo = random.randint(-100, 100)
            tubo_inferior = Tubo(screen_width, int(screen_height / 2) + altura_tubo, -1)
            tubo_superior = Tubo(screen_width, int(screen_height / 2) + altura_tubo, 1)
            grupo_tubo.add(tubo_inferior)
            grupo_tubo.add(tubo_superior)
            ultimo_tubo = tiempo_actual

        grupo_tubo.update()

        scroll_suelo -= velocidad_scroll
        if abs(scroll_suelo) > 35:
            scroll_suelo = 0

    if juego_terminado == True:
        if boton_reinicio.draw():
            juego_terminado = False
            puntuacion = reiniciar_juego()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and volando == False and juego_terminado == False:
            volando = True

    pygame.display.update()

pygame.quit()
sys.exit()
