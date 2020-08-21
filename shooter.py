import pygame, random

width = 800
height = 600
black = (0,0,0)
green = (0, 255,0)
white = (255,255,255)

pygame.init()
pygame.mixer.init()  #para el sonido
screen = pygame.display.set_mode([width,height]) # crear la ventana
pygame.display.set_caption("Shooter") #titulo de la ventana
clock = pygame.time.Clock()  #reloj para controlar los frames por segundo

#para dibujar el texto en la pantalla
def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("serif",size) #para la fuente
	text_surface = font.render(text, True, white)  #donde se va a dibujar el texto
	text_rect = text_surface.get_rect()  #rext del texto
	text_rect.midtop = (x,y)  #las coordenadas donde aparecera el texto
	surface.blit(text_surface, text_rect) #pintarlo en pantalla

#barra de salud
def draw_shield_bar(surface, x, y, percentage):
	bar_lenght = 100
	bar_height = 10
	fill = (percentage/100) * bar_lenght
	border = pygame.Rect(x, y, bar_lenght, bar_height)
	fill = pygame.Rect(x, y, fill, bar_height)
	pygame.draw.rect(surface, green, fill)
	pygame.draw.rect(surface, white,border,2)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert() #cargar la imagen
		self.image.set_colorkey(black)  #remover el fodo negro
		self.rect = self.image.get_rect()   #obtener el cuadro del sprite de la imagen
		self.rect.centerx = width // 2
		self.rect.bottom = height - 10
		self.speed_x = 0
		self.shield = 100

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed() #para versi se presiono una tecla
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5  #velocidad disminuye e 5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5  # aumenta en 5
		self.rect.x += self.speed_x

		if self.rect.right >width:
			self.rect.right = width
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		laser_sound.play()


class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image =  random.choice(meteor_images)
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(width- self.rect.width)
		self.rect.y = random.randrange(-140, -100) #efecto de que esta bajando
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)

	def update(self):
		self.rect.y += self.speedy  #movimiento en y
		self.rect.x += self.speedx  #movimiento en deagonal x

		if self.rect.top > height + 10 or self.rect.left < -40 or self.rect.right > width+25:
			self.rect.x = random.randrange(width- self.rect.width)
			self.rect.y = random.randrange(-100, -40) #efecto de que esta bajando
			self.speedy = random.randrange(1, 10)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/laser1.png").convert()
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x  #el centro del objeto
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()  #pausando las imagenes para ver que sucede
		self.frame_rate = 50   #velocidad de la explosion

	def update(self):
		now = pygame.time.get_ticks() #para saber cuanto tiempo ha transcurrido
		if now - self.last_update > self.frame_rate:
			self.last_update =  now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill()
			else:
				center =  self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

def show_go_screen():
	screen.blit(background,[0,0])
	draw_text(screen, "SHOOTER", 65, width//2,height//4)
	draw_text(screen, "Intrucciones van aqui", 27, width//2, height//2)
	draw_text(screen, "press key", 20, width//2,height*3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			if event.type == pygame.KEYUP:
				waiting = False


#meteor imagenes
meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in meteor_list:
	meteor_images.append(pygame.image.load(img).convert())

####--------explosion inagenes--------
explosion_anim = []
for i in range(8):
	file = "assets/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(black)
	img_scale = pygame.transform.scale(img, (70,70))
	explosion_anim.append(img_scale)

#cargar imagen de fondo
background = pygame.image.load("assets/orion2.jpg").convert()

#cargar sonidos
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)


pygame.mixer.music.play(loops=-1) #activar la musica y decirle que sea infinito

## game over
game_over = True


running = True

while running:
	if game_over:

		show_go_screen()

		game_over = False
		all_sprites = pygame.sprite.Group() #lista de sprites
		meteor_list = pygame.sprite.Group()
		bullets = pygame.sprite.Group()

		player = Player()
		all_sprites.add(player) #agregar el jugador a la lista

		for i in range(8):
			meteor = Meteor()
			all_sprites.add(meteor)
			meteor_list.add(meteor)

		score = 0

	clock.tick(60) #frames por segundo FPS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()

	all_sprites.update()  

	#colisiones meteoro laser
	hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
	for hit in hits:
		score += 10
		explosion_sound.play()
		#agregando las explosiones
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)

		#agregando los meteoros
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)

	#checar colisiones jugador - meteoro
	hits = pygame.sprite.spritecollide(player, meteor_list, True)
	for hit in hits:
		player.shield -= 25
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)
		if player.shield <= 0:
			game_over = True

	screen.blit(background,[0,0])

	all_sprites.draw(screen)

	#marcador
	draw_text(screen, str(score), 25, width // 2, 10)

	#escudo
	draw_shield_bar(screen,5,5,player.shield)

	pygame.display.flip()

pygame.quit()


