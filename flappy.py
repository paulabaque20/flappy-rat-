import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
# Título actualizado
pygame.display.set_caption('Flappy Rat') 

# Definir fuente
fuente = pygame.font.SysFont('Bauhaus 93', 60)

# Definir colores
blanco = (255, 255, 255)

# Definir variables del juego
scroll_suelo = 0 # Cambiado de 'ground_scroll'
velocidad_scroll = 4 # Cambiado de 'scroll_speed'
volando = False # Cambiado de 'flying'
juego_terminado = False # Cambiado de 'game_over'
tubo_gap = 150 # Cambiado de 'pipe_gap'
frecuencia_tubo = 1500 # milisegundos, cambiado de 'pipe_frequency'
ultimo_tubo = pygame.time.get_ticks() - frecuencia_tubo # Cambiado de 'last_pipe'
puntuacion = 0 # Cambiado de 'score'
paso_tubo = False # Cambiado de 'pass_pipe'


# Cargar imágenes (rutas ajustadas a 'assets/')
bg = pygame.image.load('assets/bg.png')
img_suelo = pygame.image.load('assets/ground.png')
img_boton = pygame.image.load('assets/restart.png') # Cambiado de 'button_img'


# Función para mostrar texto en pantalla
def dibujar_texto(texto, fuente, color_texto, x, y):
	img = fuente.render(texto, True, color_texto)
	screen.blit(img, (x, y))

# Función para reiniciar el juego
def reiniciar_juego():
	grupo_tubo.empty() # Vaciar el grupo de tubos
	flappy_rat.rect.x = 100 # Resetear posición X del Ratón
	flappy_rat.rect.y = int(screen_height / 2) # Resetear posición Y del Ratón
	puntuacion = 0 # Resetear la puntuación
	return puntuacion


# CLASE DEL PERSONAJE: Rat
class Rat(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.contador = 0 # Cambiado de 'counter'
		# Cargar imágenes del Ratón (rat1.png, rat2.png, rat3.png)
		for num in range (1, 4):
			img = pygame.image.load(f"assets/rat{num}.png") # Ruta corregida
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.cliqueado = False # Cambiado de 'clicked'

	def update(self):

		if volando == True:
			# Aplicar gravedad
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)

		if juego_terminado == False:
			# Salto
			if pygame.mouse.get_pressed()[0] == 1 and self.cliqueado == False:
				self.cliqueado = True
				self.vel = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.cliqueado = False

			# Manejar la animación
			enfriamiento_aleteo = 5 # Cambiado de 'flap_cooldown'
			self.contador += 1
			
			if self.contador > enfriamiento_aleteo:
				self.contador = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
				self.image = self.images[self.index]


			# Rotar el Ratón
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			# Orientar el Ratón hacia el suelo (caída)
			self.image = pygame.transform.rotate(self.images[self.index], -90)


# CLASE DEL OBSTÁCULO: Tubo
class Tubo(pygame.sprite.Sprite): # Cambiado de 'Pipe'

	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("assets/tubos.png") # Ruta corregida a 'tubos.png'
		self.rect = self.image.get_rect()
		# La variable 'position' determina si el tubo viene de abajo o arriba
		# La posición 1 es desde arriba, -1 es desde abajo
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(tubo_gap / 2)] # Usando tubo_gap
		elif position == -1:
			self.rect.topleft = [x, y + int(tubo_gap / 2)] # Usando tubo_gap


	def update(self):
		self.rect.x -= velocidad_scroll # Usando velocidad_scroll
		if self.rect.right < 0:
			self.kill() # Eliminar tubo fuera de pantalla


# CLASE DEL BOTÓN: Button
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):
		accion = False # Cambiado de 'action'

		# Obtener posición del ratón
		pos = pygame.mouse.get_pos()

		# Verificar si el ratón está sobre el botón y si fue clickeado
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				accion = True

		# Dibujar botón
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return accion


# Creación de grupos
grupo_tubo = pygame.sprite.Group() # Cambiado de 'pipe_group'
grupo_rat = pygame.sprite.Group() # Cambiado de 'bird_group'

# Creación de la instancia del Ratón
flappy_rat = Rat(100, int(screen_height / 2)) # Cambiado de 'flappy'

grupo_rat.add(flappy_rat)

# Crear instancia del botón de reinicio
boton_reinicio = Button(screen_width // 2 - 50, screen_height // 2 - 100, img_boton) # Cambiado de 'button'


run = True
# Bucle principal del juego
while run:

	clock.tick(fps)

	# Dibujar el fondo
	screen.blit(bg, (0,0))

	# Dibujar y actualizar Tubos y Ratón
	grupo_tubo.draw(screen)
	grupo_rat.draw(screen)
	grupo_rat.update()

	# Dibujar y desplazar el suelo
	screen.blit(img_suelo, (scroll_suelo, 768))

	# Verificar la puntuación
	if len(grupo_tubo) > 0:
		if grupo_rat.sprites()[0].rect.left > grupo_tubo.sprites()[0].rect.left\
			and grupo_rat.sprites()[0].rect.right < grupo_tubo.sprites()[0].rect.right\
			and paso_tubo == False:
			paso_tubo = True
		if paso_tubo == True:
			if grupo_rat.sprites()[0].rect.left > grupo_tubo.sprites()[0].rect.right:
				puntuacion += 1
				paso_tubo = False
	dibujar_texto(str(puntuacion), fuente, blanco, int(screen_width / 2), 20)


	# Buscar colisiones
	if pygame.sprite.groupcollide(grupo_rat, grupo_tubo, False, False) or flappy_rat.rect.top < 0:
		juego_terminado = True
	# Una vez que el Ratón golpea el suelo, es fin del juego y deja de volar
	if flappy_rat.rect.bottom >= 768:
		juego_terminado = True
		volando = False


	if volando == True and juego_terminado == False:
		# Generar nuevos tubos
		tiempo_actual = pygame.time.get_ticks()
		if tiempo_actual - ultimo_tubo > frecuencia_tubo:
			altura_tubo = random.randint(-100, 100)
			tubo_inferior = Tubo(screen_width, int(screen_height / 2) + altura_tubo, -1)
			tubo_superior = Tubo(screen_width, int(screen_height / 2) + altura_tubo, 1)
			grupo_tubo.add(tubo_inferior)
			grupo_tubo.add(tubo_superior)
			ultimo_tubo = tiempo_actual

		# Actualizar movimiento de tubos
		grupo_tubo.update()

		# Desplazar el suelo
		scroll_suelo -= velocidad_scroll
		if abs(scroll_suelo) > 35:
			scroll_suelo = 0
	

	# Verificar fin del juego y reinicio
	if juego_terminado == True:
		if boton_reinicio.draw(): # Dibujar botón y verificar si fue clickeado
			juego_terminado = False
			puntuacion = reiniciar_juego()
			# Resetear temporizador de tubos y bandera de paso
			ultimo_tubo = pygame.time.get_ticks() - frecuencia_tubo
			paso_tubo = False


	# Manejar eventos
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		# Iniciar el vuelo
		if event.type == pygame.MOUSEBUTTONDOWN and volando == False and juego_terminado == False:
			volando = True

	pygame.display.update()

pygame.quit()