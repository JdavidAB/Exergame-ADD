# @autor: Jonathan David Aguilar Betancourth.

# "Pathologhys": El juego presenta una temática de invasión que consiste en enfrentar y vencer al enemigo que
# ha desplegado una infección (virus) en el mundo, el objetivo del jugador es evitar ser golpeado por estos, 
# y para ello debe realizar sentadillas. El juego finaliza cuando el jugador culmine todas las etapas de éste 
# o pierda todas sus vidas.

#- Graficos de sprites, objetos, fondo e imagenes -#

# ejercicio (sentadilla) - autor:solar22 - https://www.shutterstock.com/es/image-vector/sport-women-doing-fitness-dumbbell-squat-1727481424
# background (escenario) - autor:rrcaseyr - http://opengameart.org/users/rrcaseyr
# avatar - autor:mikailain - https://sp.depositphotos.com/86045540/stock-illustration-blue-shirt-boy-game-sprites.html
# instructor - autor:irmirx - https://opengameart.org/content/golem-animations
# virus1 - autor:HBecker - https://opengameart.org/content/mad-corona
# virus2 - autor:ChiliGames - https://opengameart.org/content/random-germsamoeba-sprites
# mundo - autor:geekygnome - https://opengameart.org/content/low-poly-planet
# vidas - autor:Vander96 - https://opengameart.org/content/animated-lives
# explosion - https://opengameart.org/
# ejercicios de estiramiento dinamico - autor:Lio putra 
#                                     - https://www.shutterstock.com/es/image-vector/man-doing-bodyweight-side-steps-lateral-1841032051
#                                     - https://www.shutterstock.com/es/image-vector/woman-doing-arm-stretching-exercise-flat-2009895662
#                                     - https://www.shutterstock.com/es/image-vector/man-doing-hip-circles-exercise-flat-1991346707
#                                     - https://www.shutterstock.com/es/image-vector/woman-doing-balance-chop-exercise-flat-2055236477
# ejercicios de estiramiento estatico - autor:Lio putra 
#                                     - https://www.shutterstock.com/es/image-vector/man-doing-standing-cross-body-arm-2076359665
#                                     - https://www.shutterstock.com/es/image-vector/woman-doing-triceps-stretch-exercise-flat-1986214448
#                                     - https://www.shutterstock.com/es/image-vector/woman-doing-standing-side-bend-stretch-1986214445
#                                     - https://www.shutterstock.com/es/image-vector/man-doing-anjaneyasana-low-lunge-yoga-2102664823

#- Efectos de sonido -#
# https://opengameart.org/

### CODIGO JUEGO ###

# Librerias
import pygame, sys
import random
import os
from pygame import mouse
from pygame.constants import MOUSEBUTTONDOWN
import serial.tools.list_ports
import serial
import signal
import itertools
import threading
import time
import sqlite3

ANCHO = 800 # Ancho
ALTO = 600  # Altura

NEGRO = (0, 0, 0)
BLANCO = (248, 248, 248)
VERDE = (20, 248, 20)
ROJO = (200, 20, 10)
AMARILLO = (200, 192, 16)
AZULCLARO = (180, 226, 244)
FPS = 60   

# Busca el directorio donde esta el archivo (__file__) cargado
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# Funcion para cerrar la comunicacion (Arduino-Python) de forma segura
def signal_handler(signal, frame):
    print("HAS SALIDO - CTRL+C FUE PRESIONADO")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("PARA SALIR - PRESIONAR CTRL+C")

# Funciones para dibujar en ventana texto con diferentes caracteristicas
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, BLANCO)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_text1(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, BLANCO)
    text_shadow = font.render(text, True, ROJO)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    text_shadow_pos = [text_rect.x +2, text_rect.y +2]
    surface.blit(text_shadow, text_shadow_pos)
    surface.blit(text_surface, text_rect)

def draw_text2(surface, text, size, x, y):
    font = pygame.font.SysFont("segoe print", size)
    text_surface = font.render(text, True, BLANCO)
    text_shadow = font.render(text, True, NEGRO)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    text_shadow_pos = [text_rect.x +2, text_rect.y +2]
    surface.blit(text_shadow, text_shadow_pos)
    surface.blit(text_surface, text_rect)

# funcion para dibujar en ventana los valores de puntaje, puntaje mas alto y nivel del juego 
def dibujar_score_o_high_score_o_nivel(surf, text, size, pos): # pos referente a una tupla que contendra cordenadas de posicion (x, y)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLANCO)
    text_shadow = font.render(text, True, ROJO)
    text_rect = text_surface.get_rect()
    text_rect.midtop = pos                                     # midtop referente a la parte superior de la letra que se vaya a mostrar
    text_shadow_pos = [text_rect.x +2, text_rect.y +2]
    surf.blit(text_shadow, text_shadow_pos)
    surf.blit(text_surface, text_rect)

# Funciones para actualizar y dibujar automaticamente sprites
def asteroide_nuevo():
    a = Asteroides()
    all_sprites.add(a) # añadimos a(asteroide) a la lista de sprites para actualizar y dibujar automaticamente el sprite
    asteriodes.add(a)  # añadimos a(asteroide) a el grupo Asteroides

def mob_nuevo():
    m = Mob()
    all_sprites.add(m) # añadimos m(enemigo) a la lista de sprites para actualizar y dibujar automaticamente el sprite
    mobs.add(m)        # añadimos m(enemigo) a el grupo Mobs, que me permitira comprobar colisiones

# Funciones para dibujar en ventana barra de vida y tiempo, numero de vidas y objetos adicionales del juego
def dibujar_barra_vida(surf, x, y, valor):
    if valor < 0:
        valor = 0
    
    LONGITUD_BARRA = 300 # longitud
    ALTURA_BARRA = 10    # altura
    fill = (valor / 100)*LONGITUD_BARRA                          # total de la barra a dibujar
    fill_rect = pygame.Rect(x, y, fill, ALTURA_BARRA)
    outer_rect = pygame.Rect(x, y, LONGITUD_BARRA, ALTURA_BARRA) # muestra un marco (rectangulo) exterior en la barra de vida
    pygame.draw.rect(surf, ROJO, outer_rect)
    pygame.draw.rect(surf, VERDE, fill_rect)
    pygame.draw.rect(surf, BLANCO, outer_rect, 2)                # asignamos colo blanco al marco de la barra 

def dibujar_barra_tiempo(surf, x, y, valor):
    if valor < 0:
        valor = 0
    
    LONGITUD_BARRA = 10 # longitud
    ALTURA_BARRA = 300  # altura
    fill = (valor / 60)*ALTURA_BARRA                             # total de la barra a dibujar 
    fill_rect = pygame.Rect(x, y, LONGITUD_BARRA, fill)
    outer_rect = pygame.Rect(x, y, LONGITUD_BARRA, ALTURA_BARRA) # muestra un marco (rectangulo) exterior en la barra de tiempo
    pygame.draw.rect(surf, VERDE, outer_rect)
    pygame.draw.rect(surf, NEGRO, fill_rect)
    pygame.draw.rect(surf, BLANCO, outer_rect, 2)                # asignamos color blanco al marco de la barra 

def dibujar_numerovidas(surf, x, y, n_lives, img):
    for i in range(n_lives):
        img_rect = img.get_rect()
        img_rect.x = x + 20*i
        img_rect.y = y
        surf.blit(img, img_rect)

def dibujar_imagen(surf, x, y, img):
    img_rect = img.get_rect()
    img_rect.x = x 
    img_rect.y = y
    surf.blit(img, img_rect)

# Funciones para mostrar mensajes motivaciones en la escena mundo 1.
def dibujar_dialogo(surf, x ,y):
    DILG_LARGO = 300
    DILG_ANCHO = 150
    fill =  DILG_LARGO
    border = pygame.Rect(x, y, DILG_LARGO, DILG_ANCHO)
    fill = pygame.Rect(x, y, fill, DILG_ANCHO)
    pygame.draw.rect(surf, NEGRO, fill, 0)
    pygame.draw.rect(surf, AZULCLARO, border, 2)
    draw_text2(ventana, "'Recuerda'", 18, 470, 180)
    draw_text2(ventana, "Debes bajar lo mas que puedas", 18, 470, 220)
    draw_text2(ventana, "Vamos, Tu puedes", 18, 470, 260)

def dibujar_dialogo2(surf, x ,y):
    DILG_LARGO = 300
    DILG_ANCHO = 150
    fill =  DILG_LARGO
    border = pygame.Rect(x, y, DILG_LARGO, DILG_ANCHO)
    fill = pygame.Rect(x, y, fill, DILG_ANCHO)
    pygame.draw.rect(surf, NEGRO, fill, 0)
    pygame.draw.rect(surf, AZULCLARO, border, 2)
    draw_text2(ventana, "'Exelente'", 18, 470, 180)
    draw_text2(ventana, "Sigue asi, que", 18, 470, 220)
    draw_text2(ventana, "esto apenas comienza", 18, 470, 260)

def dibujar_dialogo3(surf, x ,y):
    DILG_LARGO = 300
    DILG_ANCHO = 150
    fill =  DILG_LARGO
    border = pygame.Rect(x, y, DILG_LARGO, DILG_ANCHO)
    fill = pygame.Rect(x, y, fill, DILG_ANCHO)
    pygame.draw.rect(surf, NEGRO, fill, 0)
    pygame.draw.rect(surf, AZULCLARO, border, 2)
    draw_text2(ventana, "No permitas", 18, 470, 180)
    draw_text2(ventana, "Que el virus te toque", 18, 470, 220)
    draw_text2(ventana, "¡ ANIMO !...", 18, 470, 260)

def dibujar_dialogo4(surf, x ,y):
    DILG_LARGO = 300
    DILG_ANCHO = 150
    fill =  DILG_LARGO
    border = pygame.Rect(x, y, DILG_LARGO, DILG_ANCHO)
    fill = pygame.Rect(x, y, fill, DILG_ANCHO)
    pygame.draw.rect(surf, NEGRO, fill, 0)
    pygame.draw.rect(surf, AZULCLARO, border, 2)
    draw_text2(ventana, "'Recuerda'", 18, 470, 180)
    draw_text2(ventana, "Debes bajar lo mas que puedas", 18, 470, 220)
    draw_text2(ventana, "¡ VAMOS !...", 18, 470, 260)

def dibujar_dialogo5(surf, x ,y):
    DILG_LARGO = 300
    DILG_ANCHO = 150
    fill =  DILG_LARGO
    border = pygame.Rect(x, y, DILG_LARGO, DILG_ANCHO)
    fill = pygame.Rect(x, y, fill, DILG_ANCHO)
    pygame.draw.rect(surf, NEGRO, fill, 0)
    pygame.draw.rect(surf, AZULCLARO, border, 2)
    draw_text2(ventana, "¡ VAMOS !", 18, 470, 180)
    draw_text2(ventana, "Falta poco", 18, 470, 220)
    draw_text2(ventana, "Lo estas haciendo muy bien...", 18, 470, 260)

def dibujar_dialogo6(surf, x ,y):
    DILG_LARGO = 300
    DILG_ANCHO = 150
    fill =  DILG_LARGO
    border = pygame.Rect(x, y, DILG_LARGO, DILG_ANCHO)
    fill = pygame.Rect(x, y, fill, DILG_ANCHO)
    pygame.draw.rect(surf, NEGRO, fill, 0)
    pygame.draw.rect(surf, AZULCLARO, border, 2)
    draw_text2(ventana, "¡ Lo haz logrado !", 18, 470, 180)
    draw_text2(ventana, "Ahora, debes subir tus brazos", 18, 470, 220)
    draw_text2(ventana, "para tomar los medicamentos", 18, 470, 260)

def dibujar_dialogo7(surf, x ,y):
    DILG_LARGO = 300
    DILG_ANCHO = 150
    fill =  DILG_LARGO
    border = pygame.Rect(x, y, DILG_LARGO, DILG_ANCHO)
    fill = pygame.Rect(x, y, fill, DILG_ANCHO)
    pygame.draw.rect(surf, NEGRO, fill, 0)
    pygame.draw.rect(surf, AZULCLARO, border, 2)
    draw_text2(ventana, "¡ ANIMO !...", 18, 470, 180)
    draw_text2(ventana, "Lo estas haciendo bien", 18, 470, 220)
    draw_text2(ventana, "...", 18, 470, 260)

def dibujar_dialogo8(surf, x ,y):
    DILG_LARGO = 300
    DILG_ANCHO = 150
    fill =  DILG_LARGO
    border = pygame.Rect(x, y, DILG_LARGO, DILG_ANCHO)
    fill = pygame.Rect(x, y, fill, DILG_ANCHO)
    pygame.draw.rect(surf, NEGRO, fill, 0)
    pygame.draw.rect(surf, AZULCLARO, border, 2)
    draw_text2(ventana, "Que no se te escapen", 18, 470, 180)
    draw_text2(ventana, "los medicamentos", 18, 470, 220)
    draw_text2(ventana, "¡ ANIMO !...", 18, 470, 260)

def dibujar_dialogo9(surf, x ,y):
    DILG_LARGO = 300
    DILG_ANCHO = 150
    fill =  DILG_LARGO
    border = pygame.Rect(x, y, DILG_LARGO, DILG_ANCHO)
    fill = pygame.Rect(x, y, fill, DILG_ANCHO)
    pygame.draw.rect(surf, NEGRO, fill, 0)
    pygame.draw.rect(surf, AZULCLARO, border, 2)
    draw_text2(ventana, "'Recuerda'", 18, 470, 180)
    draw_text2(ventana, "Levanta muy bien los brazos", 18, 470, 220)
    draw_text2(ventana, "¡ VAMOS !...", 18, 470, 260)

def dibujar_dialogo10(surf, x ,y):
    DILG_LARGO = 300
    DILG_ANCHO = 150
    fill =  DILG_LARGO
    border = pygame.Rect(x, y, DILG_LARGO, DILG_ANCHO)
    fill = pygame.Rect(x, y, fill, DILG_ANCHO)
    pygame.draw.rect(surf, NEGRO, fill, 0)
    pygame.draw.rect(surf, AZULCLARO, border, 2)
    draw_text2(ventana, "Ahora, sera un ejercicio", 18, 470, 180)
    draw_text2(ventana, "COMBINADO", 18, 470, 220)
    draw_text2(ventana, "¡ VAMOS, TU PUEDES !...", 18, 470, 260)  

def dibujar_dialogo11(surf, x ,y):
    DILG_LARGO = 300
    DILG_ANCHO = 150
    fill =  DILG_LARGO
    border = pygame.Rect(x, y, DILG_LARGO, DILG_ANCHO)
    fill = pygame.Rect(x, y, fill, DILG_ANCHO)
    pygame.draw.rect(surf, NEGRO, fill, 0)
    pygame.draw.rect(surf, AZULCLARO, border, 2)
    draw_text2(ventana, "'Recuerda'", 18, 470, 180)
    draw_text2(ventana, "Levanta muy bien los brazos", 18, 470, 220)
    draw_text2(ventana, "y baja lo mas que puedas...", 18, 470, 260)  

def dibujar_dialogo12(surf, x ,y):
    DILG_LARGO = 300
    DILG_ANCHO = 150
    fill =  DILG_LARGO
    border = pygame.Rect(x, y, DILG_LARGO, DILG_ANCHO)
    fill = pygame.Rect(x, y, fill, DILG_ANCHO)
    pygame.draw.rect(surf, NEGRO, fill, 0)
    pygame.draw.rect(surf, AZULCLARO, border, 2)
    draw_text2(ventana, "¡ Vamos !", 18, 470, 180)
    draw_text2(ventana, "Debes ser muy rapido", 18, 470, 220)
    draw_text2(ventana, "No te rindas...", 18, 470, 260) 

# Funcion - muestra la escena inicial del juego 
def show_go_ventana():
    draw_text(ventana, "PATHOLOGHYS", 65, ANCHO // 2, ALTO // 4)
    draw_text(ventana, "!Animo tu puedes!", 27, ANCHO // 2, ALTO // 2)
    draw_text(ventana, "Press 'x'", 20, ANCHO // 2, ALTO * 3/4)
    pygame.display.flip()
    running = True
    while running:
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keystate = pygame.key.get_pressed()
            if keystate [pygame.K_x]:
                running  = False

# Clase del jugador - propiedades y atributos 
class Player(pygame.sprite.Sprite):  # JUGADOR
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.sprites=[] 

        for i in range(3):
            filename1 = 'jugador' + str(i) + '.png'                                        # nombre de las imagenes 
            img1 = pygame.image.load(os.path.join(ASSETS_DIR, filename1)).convert_alpha()  # leemos y cargamos imagenes pequeñas
            img_big1 = pygame.transform.scale(img1, (90,340))                              # escalamos las imagenes pequeñas a imagenes grandes
            self.sprites.append(img_big1) 

        self.cambio = 0 
        self.image = self.sprites[self.cambio]
        self.rect = self.image.get_rect()                    # cuadrado que engloba (encierra) la imagen (sprite)
        self.radius = 130
        self.rect.centerx = ANCHO//3 
        self.rect.bottom = ALTO - 10
        self.speedx = 0
        self.vida = 100
        self.numerovidas = 3  
        self.hidden = False                                  # oculta al jugador cuando este cambian a True
        self.hide_timer = pygame.time.get_ticks()            # tiempo que va a estar oculto el jugador

    # Actualiza las dinamicas de esta clase
    def update(self):
        # Muestra la imagen de la clase Player despues de un determinado tiempo 
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.rect.centerx = ANCHO//3 
            self.rect.bottom = ALTO - 10
        
        # Animacion del jugador - depende de los valores del sensor final de carrera 
        self.speedx = dsp

        if mundo == 1:
            if self.speedx > 100: 
                self.cambio = 1
                self.image = self.sprites[self.cambio]
                
            else:
                self.cambio = 0
                self.image = self.sprites[self.cambio]

    # Oculta la imagen del jugador por un determinado tiempo, si este pierde una vida             
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.y = ALTO + 200

# Clase Asteroides - propiedades y atributos
class Asteroides(pygame.sprite.Sprite):  
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroide_img                                   # asigna la imagen a esta clase
        self.image.set_colorkey(NEGRO)                           
        self.rect = self.image.get_rect()                            # cuadrado que engloba (encierra) la imagen (sprite)
        self.radius = int(self.rect.width*0.3) 
        self.rect.x = random.randrange(-5, ANCHO+5)                                
        self.rect.y = random.randrange(-100, -40)                
        self.speedy = random.randrange(5, 10)                        # permite establecer la velocidad de los estaroides entre (5,10)
        self.speedx = random.randrange(-5, 5)                        # permite que algunos asteriodes se muevann de forma diagonal

    # Actualiza las dinamicas de esta clase  
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > ALTO + 10 or self.rect.left < -25 or self.rect.right > ANCHO + 25:
            self.rect.x = random.randrange(-5, ANCHO+5)                                
            self.rect.y = random.randrange(-100, -40)                 
            self.speedy = random.randrange(5, 10) 
            self.speedx = random.randrange(-5, 5)
            self.image.set_colorkey(NEGRO)

# Clase Enemigo - propiedades y atributos
class Mob(pygame.sprite.Sprite):  # ENEMIGOS
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(enemy['enemys'])                    # asigna la imagen a esta clase
        self.rect = self.image.get_rect()                              # cuadrado que engloba (encierra) la imagen (sprite)
        self.radius = int(self.rect.width*0.3) 
        self.rect.x = random.randint(-100, -40)                        # inicia el movimiento horizontalmente entre esos rangos establecidos 
        self.rect.y =  random.randint((ALTO//2)-45, (ALTO//2)-40)      # mantiene el movimiento verticalmete entre esos rangos establecidos 
        self.speedx = 0 

    # Actualiza las dinamicas de esta clase 
    def update(self):
        self.speedx = velocidad_enem_o_medic

        global score, high_score
        if mundo == 1:
            self.rect.x += self.speedx
            # rango establecido para la destrucion de esta clase y posterior creacion
            if self.rect.right > ANCHO//2.8:             
                score += 5
                    
                self.rect.y = random.randint((ALTO//2)-45, (ALTO//2)-40) 
                self.rect.x = random.randint(-100, -40)
                self.speedx = velocidad_enem_o_medic 

                if score > high_score:
                    high_score = score 

# Clase Explosion - propiedades y atributos                 
class Explosion(pygame.sprite.Sprite): # ANIMACION DE EXPLOSION
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]                # asignacion del primer frame de la animacion
        self.rect = self.image.get_rect()
        self.rect.center = center                                # la animacion se ubica en el centro de la imagen que se va a sustituir
        self.frame = 0                                           # para saber en que frame se esta inicialmente
        self.last_update = pygame.time.get_ticks()               # tiempo que a trancurrido desde que se inicio el juego
        self.frame_delay = 50                                    # tiempo en milisegundos entre frame y frame de la animacion

    # Actualiza las dinamicas de esta clase 
    def update(self):
        now = pygame.time.get_ticks()                            # cuenta del tiempo actual

        # Calculamos si toca cambiar de frame
        if now - self.last_update > self.frame_delay:
            self.last_update = now                               # actualizamos self.last_update
            self.frame +=1                                       # incrementamos el indice del frame
            
            # Comrpobamos si se llego al final de la animacion
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center                        # linea para que de una imagen de animacion a otra no se desubiquen de su posicion
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center =center

# Clase Instructor - propiedades y atributos
class Instructor(pygame.sprite.Sprite):
    def __init__(self, position, images, delay):
        super(Instructor, self).__init__()

        self.images = itertools.cycle(images)                    # asignacion del primer frame de la animacion
        self.image = next(self.images)
        self.image.set_colorkey(NEGRO)
        self.rect = pygame.Rect(position,  self.image.get_rect().size)
        self.animation_time = delay
        self.current_time = 0
    
    # Actualiza las dinamicas de esta clase 
    def comportamiento(self, r):
        self.current_time += r
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.image = next(self.images)
            self.image.set_colorkey(NEGRO)

# Carga la imagen del instructor
def load_images(path):
    images =  [pygame.image.load(path + os.sep + file_name).convert() for file_name in sorted(os.listdir(path))]
    return images
    
###################################################################################################################
###################################################################################################################
# Inicializa Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()

# Abrir la comunicacion (Arduino-Python), ingresando el nombre del puerto serial
ports = list(serial.tools.list_ports.comports())
for SerialPortName in ports:
    print(SerialPortName)

try:
    porta=input("INGRESE EL NOMBRE DEL PUERTO SERIE DONDE ESTA CONECTADO EL ARDUINO: ")
    ser = serial.Serial(str(porta))  # abre el puerto serie  
    print(ser.name)   

except serial.SerialException:
    print("PUERTO INEXISTENTE")  
    sys.exit(0)


###################################
#----- ESTRUCTURA BASE DATOS -----#
###################################
conexion = sqlite3.connect('datosjuego.db')

cursor = conexion.cursor()

cursor.execute("""create table IF NOT EXISTS datos (
                              N° integer primary key autoincrement,
                              mundo text,
                              nivel text,
                              vidasrestantes text,
                              porcentajevida text,
                              dificultadnivel text,
                              percepciondificultad text,
                              ppm text 
                        )""")

# Se establece el ancho y alto de la ventana de juego 
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('JUEGO PATHOLOGHYS')
reloj = pygame.time.Clock()

# Funcion para las colosiones del player vs enemigo
def colision():
    global game_over, death_explosion, score, high_score

    if player.speedx <= 100 and mundo == 1:   
        
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        
        for hit in hits:
            snd_explosions[1].play()
            expl = Explosion(hit.rect.center, 'small')
            all_sprites.add(expl)
            player.vida -= 20
            mob_nuevo()
            
            if player.vida <= 0:
                snd_player_explosion.play()
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.numerovidas -=1
                player.vida = 100
                player.hide()
            
        if player.numerovidas == 0 and not death_explosion.alive():
            game_over = True

# Funcion para ordenar los objetos del juego en la escena mundo 1 
def esenarios():
    global comentario2, comentario3, comentario6, comentario7, tiempo_actual1, tiempo_pulsar_botón1

    if mundo == 1:
        ventana.blit(background,background_rect)
        dibujar_imagen(ventana, ANCHO-180, -100, mundo_img)
        draw_text1(ventana, "World", 30, ANCHO-70, 20)
        draw_text1(ventana, "Legs", 30, ANCHO-70, 45)
        dibujar_barra_tiempo(ventana, 760, 260, tiempo_actual1-tiempo_pulsar_botón1)


#########################################
#---------- CARGA DE IMAGENES ----------#
#########################################
background =  pygame.image.load(os.path.join(ASSETS_DIR, 'paisaje1.png')).convert_alpha() 
background = pygame.transform.scale(background, (ANCHO,ALTO))
background_rect = background.get_rect()

asteroide_img = pygame.image.load(os.path.join(ASSETS_DIR, 'asteroide.png')).convert_alpha()
asteriode_img = pygame.transform.scale(asteroide_img, (1,1))

ejercicio_img = pygame.image.load(os.path.join(ASSETS_DIR, 'EEestiramientoDinamico.png')).convert_alpha()
ejercicio_img = pygame.transform.scale(ejercicio_img, (560,290)) 

ejercicio_img0 = pygame.image.load(os.path.join(ASSETS_DIR, 'EEestiramientoEstatico.png')).convert_alpha()
ejercicio_img0 = pygame.transform.scale(ejercicio_img0, (500,290)) 

ejercicio_img1 = pygame.image.load(os.path.join(ASSETS_DIR, 'ss.png')).convert_alpha()
ejercicio_img1 = pygame.transform.scale(ejercicio_img1, (260,200))

virus_img = pygame.image.load(os.path.join(ASSETS_DIR, 'virus.png')).convert_alpha()
virus_img = pygame.transform.scale(virus_img, (240,230))

intru_img = pygame.image.load(os.path.join(ASSETS_DIR, 'intru.png')).convert_alpha()
intru_img = pygame.transform.scale(intru_img, (350,350))

estrella1_img = pygame.image.load(os.path.join(ASSETS_DIR, 's1.png')).convert_alpha()
estrella1_img = pygame.transform.scale(estrella1_img, (390,160))

estrella2_img = pygame.image.load(os.path.join(ASSETS_DIR, 's2.png')).convert_alpha()
estrella2_img = pygame.transform.scale(estrella2_img, (390,160))

estrella3_img = pygame.image.load(os.path.join(ASSETS_DIR, 's3.png')).convert_alpha()
estrella3_img = pygame.transform.scale(estrella3_img, (390,160))

estrella4_img = pygame.image.load(os.path.join(ASSETS_DIR, 's4.png')).convert_alpha()
estrella4_img = pygame.transform.scale(estrella4_img, (390,160))

estrella5_img = pygame.image.load(os.path.join(ASSETS_DIR, 's5.png')).convert_alpha()
estrella5_img = pygame.transform.scale(estrella5_img, (390,160))

estrella6_img = pygame.image.load(os.path.join(ASSETS_DIR, 's6.png')).convert_alpha()
estrella6_img = pygame.transform.scale(estrella6_img, (390,160))

estrella7_img = pygame.image.load(os.path.join(ASSETS_DIR, 's7.png')).convert_alpha()
estrella7_img = pygame.transform.scale(estrella7_img, (390,160))

estrella8_img = pygame.image.load(os.path.join(ASSETS_DIR, 's8.png')).convert_alpha()
estrella8_img = pygame.transform.scale(estrella8_img, (390,160))

mundo_img = pygame.image.load(os.path.join(ASSETS_DIR, 'mundo1.png')).convert_alpha()
mundo_img = pygame.transform.scale(mundo_img, (250,250))

encuesta_img = pygame.image.load(os.path.join(ASSETS_DIR, 'encuesta.png')).convert_alpha()
encuesta_img = pygame.transform.scale(encuesta_img, (500,150))

# INSTRUCTOR
images = load_images(path='background_frames')

vidas_img = pygame.image.load(os.path.join(ASSETS_DIR, 'vidas.png')).convert_alpha()
vidas_img = pygame.transform.scale(vidas_img, (16,16))

# ENEMIGO
enemy={}
enemy['enemys'] = []
for i in range(2):
    filename2 = 'virus' + str(i) + '.png'                                         # nombre de las imagenes 
    img2 = pygame.image.load(os.path.join(ASSETS_DIR, filename2)).convert_alpha() # leemos y cargamos imagenes pequeñas
    img_big2 = pygame.transform.scale(img2, (45,55))                              # escalamos las imagenes pequeñas a imagenes grandes
    enemy['enemys'].append(img_big2)                                              # añadimos las imagenes grandes al diccionario que tiene clave 'enemys'

# DICCIONARIO DE ANIMACIONES EXPLOSION
explosion_anim = {}                # creacion de diccionario vacio
explosion_anim['big'] = []         # listas con clave 'big' con inicializacion vacia
explosion_anim['small'] = []       # listas con clave 'small' con inicializacion vacia

# Llenamos el contenio de este diccionario
for i in range(3):
    filename = 'explosion' + str(i) + '.png'                                     # nombre de las imagenes 
    img = pygame.image.load(os.path.join(ASSETS_DIR, filename)).convert_alpha()  # leemos y cargamos imagenes pequeñas
    img_big = pygame.transform.scale(img, (80,80))                               # escalamos las imagenes pequeñas a imagenes grandes
    explosion_anim['big'].append(img_big)                                        # añadimos las imagenes grandes al diccionario que tiene clave 'big'
    explosion_anim['small'].append(img)                                          # añadimos las imagenes pequeñas al diccionario que tiene clave 'small'

explosion_anim['player'] = explosion_anim['big'][0:3]
explosion_anim['player'].append(explosion_anim['big'][1])
explosion_anim['player'].append(explosion_anim['big'][0])


######################################
#--------- CARGA DE SONIDOS ---------#
######################################
snd_explosions = []
snd_files = ['explosion.wav', 'explosion2.wav', 'explosion3.wav']
for snd_file in snd_files:
    snd = pygame.mixer.Sound(os.path.join(ASSETS_DIR, snd_file))
    snd.set_volume(0.06)
    snd_explosions.append(snd)

snd_player_explosion = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'explosion_player.wav'))
snd_player_explosion.set_volume(0.06)

snd_encuesta = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'encuesta.wav'))
snd_encuesta.set_volume(0.2)

pygame.mixer.music.load(os.path.join(ASSETS_DIR, 'Fondo.wav'))
pygame.mixer.music.set_volume(0.09) 

# Reproducir musica para siempre
pygame.mixer.music.play(loops = -1)                 # el -1 hace que se reprodusca la musica de manera indefinida


###############################################
#------------ FUENTES DE LETRAS --------------#
###############################################
font_name = pygame.font.match_font('arial')         # nos aseguramos que cargue alguna fuente de letra para mostrar
fuente = pygame.font.SysFont("segoe print", 30)
fuente1 = pygame.font.SysFont("segoe print", 20) 


######################################
#--- FUNCIONES PARA LAS HISTORIAS ---#
######################################
# Funcion - Mision intruccion del ejercicio
def go_ventana():
    ventana.fill(NEGRO)
    historia = [
    "          MUNDO LEGS",
    "",
    "El objetivo es esquivar la infeccion", 
    "        Que 'PATHOLOGHYS'",
    "    Desplego sobre este mundo",
    "",
    "    ¡ Que el virus No te toque !",
    "",
    "                         Para ello, debes realizar el siguiente movimiento",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "                                         Press 'x' para continuar "
    ]
                    
    y = 30
    for frase in historia:
        texto = fuente1.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, 20, 245, intru_img)
        dibujar_imagen(ventana, 420, 320, ejercicio_img1)
        dibujar_imagen(ventana, 480, 15, mundo_img)
        y += 30
    pygame.display.flip()

    running = True
    while running:
        global tiempo_pulsar_botón, t
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keystate = pygame.key.get_pressed()
            if keystate [pygame.K_x]:

                t = True
                tiempo_pulsar_botón = pygame.time.get_ticks()
                running  = False

# Funcion - Ejercicios de estiramiento dinamico
def go_ventana1():
    ventana.fill(NEGRO)
    historia = [
    "      Antes de comenzar con la misión, debes prepararte",
    "",
    "  Realiza los siguientes ejercicios de estiramiento dinamico", 
    "",
    "                    12 repeticiones por ejercicio",
    "",
    "",
    "",
    "", 
    "",
    "",
    "",
    "",
    "",
    "",
    "                          ¡ Vamos no tardes !",
    "",
    "                       Press 'x' para continuar "
    ]
                    
    y = 30
    for frase in historia:
        texto = fuente1.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, ANCHO-680, 190, ejercicio_img)  
        y += 30
    pygame.display.flip()

    running = True
    while running:
        global tiempo_pulsar_botón, t
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                running  = False

# Funcion - Contextualizacion de la historia
def show_go_ventana1():
    ventana.fill(NEGRO)
    historia = [
    "    Se ha detectado un virus llamado",
    "",
    "             ''PATHOLOGHYS''",
    "",
    "    Su plan es destruir mundos con", 
    "         ''Poblacion Sendentaria''",
    "",
    "     Tú misión, detenerlo y vencerlo",
    "",
    "        Se dirige a ''Mundo Legs''", 
    "",
    "Tienes que ser muy rápido para lograrlo",
    "",
    "          ''ANIMO TU PUEDES''",
    "",
    "",
    "         Press 'x' para continuar "
    ]
                    
    y = 30
    for frase in historia:
        texto = fuente1.render(frase, True, BLANCO)
        ventana.blit(texto, (360, y))
        dibujar_imagen(ventana, 20, 100, intru_img)
        y += 30
    pygame.display.flip()

    running = True
    while running:
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                running  = False

# Funcion - Mensaje de motivacion
def show_go_ventana2():
    ventana.fill(NEGRO)
    historia = [
    "              Lograste detener a",
    "",
    "                PATHOLOGHYS",
    "",
    "        Haz salvado el Mundo ''Legs''",
    "",
    "  Los habitantes de este mundo estan",
    "",
    "               Muy agradecidos",
    "",
    " Si que eres una persona ''Muy activa''",   
    "",
    "                 Mantente asi",
    "",
    "",
    "          Press 'x' para continuar "
    ]   
                    
    y = 30
    for frase in historia:
        texto = fuente.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        y += 30
    pygame.display.flip()

    running = True
    while running:
        global tiempo_pulsar_botón, t
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                running  = False            

# Funcion - Mensaje final de motivacion
def show_go_ventana4():
    ventana.fill(NEGRO)
    historia = [
    "                ¡FELICIDADES!",
    "",
    "     Haz derrotado a PATHOLOGHYS",
    "",
    "",
    "          Lograste salvar a todos ",
    "",
    "",
    "",
    "",
    "",
    "",
    "",  
    "",
    "            ''¡ERES EL MEJOR!''",
    "",
    "",
    "         Press 'x' para continuar"
    ] 
                    
    y = 30
    for frase in historia:
        texto = fuente.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, 275, 230, virus_img)
        y += 30
    pygame.display.flip()

    running = True
    while running:
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keystate = pygame.key.get_pressed()
            if keystate [pygame.K_x]:
                running  = False

# Funcion - Ejercicios de estiramiento dinamico
def go_ventana5():
    ventana.fill(NEGRO)
    historia = [
    "           Antes de terminar, debes relajar tu cuerpo",
    "",
    "   Realiza los siguientes ejercicios de estiramiento estatico", 
    "",
    "                      10 segundos por ejercicio",
    "",
    "",
    "",
    "", 
    "",
    "",
    "",
    "",
    "",
    "",
    "                          ¡ Buen trabajo !",
    "",
    "                  Press 'x' para volver a jugar"
    ]
                    
    y = 30
    for frase in historia:
        texto = fuente1.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, ANCHO-650, 190, ejercicio_img0)  
        y += 30
    pygame.display.flip()

    running = True
    while running:
        global tiempo_pulsar_botón, t
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                running  = False

# Funcion encuesta - Percepcón de dificultad
def go_ventana4():
    aceptar1 = pygame.Rect(100, 400, 35 ,35)
    aceptar2 = pygame.Rect(230, 400, 35 ,35)
    aceptar3 = pygame.Rect(380, 400, 35 ,35)
    aceptar4 = pygame.Rect(530, 400, 35 ,35)
    aceptar5 = pygame.Rect(660, 400, 35 ,35)
    ventana.fill(NEGRO)
    historia = [
    "                               ¡MUY BIEN!",
    "",
    "     ¿Qué te pareció la dificultad de este nivel del juego?",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "Muy          Fácil           Ni fácil           Difícil          Muy",
    "fácil                          Ni difícil                           difícil ",  
    "",
    "",
    "",
    "                            ¡ NO TARDES !",
    "",
    "                Press 'x' para continuar en el juego"
    ]  
                   
    y = 30
    for frase in historia:
        texto = fuente1.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, 150, 150, encuesta_img)
        pygame.draw.rect(ventana, BLANCO, aceptar1, 0) 
        pygame.draw.rect(ventana, AZULCLARO, aceptar2, 0) 
        pygame.draw.rect(ventana, VERDE, aceptar3, 0)
        pygame.draw.rect(ventana, AZULCLARO, aceptar4, 0)
        pygame.draw.rect(ventana, ROJO, aceptar5, 0)
        y += 30
        draw_text1(ventana, "1", 35, 115, 395)
        draw_text1(ventana, "2", 35, 245, 395)
        draw_text1(ventana, "3", 35, 397, 395)
        draw_text1(ventana, "4", 35, 545, 395)
        draw_text1(ventana, "5", 35, 678, 395)
    pygame.display.flip()
    
    running = True
    while running:
        global tiempo_pulsar_botón, t, percepcion, puntaje
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            # Permite insertar las variables (parametros del juego, percepcion de dificultad, desempeño y pulso cardiaco del jugador)
            # en la base de datos, al pulsar clic en alguna opcion que se muestra en la encuesta 
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and mundo == 1:
                if aceptar1.collidepoint(mouse.get_pos()):
                    timer_interruptmundo1()
                    snd_encuesta.play()
                    percepcion = 1
                    basedatosmundo1()
                    print(percepcion)
                if aceptar2.collidepoint(mouse.get_pos()):
                    timer_interruptmundo1()
                    snd_encuesta.play()
                    percepcion = 2
                    basedatosmundo1()
                    print(percepcion)
                if aceptar3.collidepoint(mouse.get_pos()):
                    timer_interruptmundo1()
                    snd_encuesta.play()
                    percepcion = 3
                    basedatosmundo1()
                    print(percepcion)
                if aceptar4.collidepoint(mouse.get_pos()):
                    timer_interruptmundo1()
                    snd_encuesta.play()
                    percepcion = 4
                    basedatosmundo1()
                    print(percepcion)
                if aceptar5.collidepoint(mouse.get_pos()):
                    timer_interruptmundo1()
                    snd_encuesta.play()
                    percepcion = 5
                    basedatosmundo1()
                    print(percepcion)
                    
            keystate = pygame.key.get_pressed()
            if keystate [pygame.K_x]:
                t = True
                tiempo_pulsar_botón = pygame.time.get_ticks()
                running  = False

# Funciones escenas de bonificacion            
def show_go_nivel1():
    ventana.fill(NEGRO)
    historia = [
    "                ¡FELICIDADES!",
    "",
    "",
    "          Haz superado el 'Nivel 1'",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    " ",
    "",  
    "            Sigue asi, ¡No pares!",
    "",
    "",
    "         Press 'x' para continuar "
    ]   
                    
    y = 30
    for frase in historia:
        texto = fuente.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, 205, 215, estrella1_img)
        y += 30
    pygame.display.flip()

    running = True
    while running:
        global tiempo_pulsar_botón, t
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keystate = pygame.key.get_pressed()
            if keystate [pygame.K_x]:
                running  = False

def show_go_nivel2():
    ventana.fill(NEGRO)
    historia = [
    "                ¡FELICIDADES!",
    "",
    "",
    "          Haz superado el 'Nivel 2'",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    " ",
    "",  
    "            Sigue asi, ¡No pares!",
    "",
    "",
    "         Press 'x' para continuar "
    ]   
                    
    y = 30
    for frase in historia:
        texto = fuente.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, 205, 215, estrella2_img)
        y += 30
    pygame.display.flip()

    running = True
    while running:
        global tiempo_pulsar_botón, t
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keystate = pygame.key.get_pressed()
            if keystate [pygame.K_x]:
                running  = False


def show_go_nivel3():
    ventana.fill(NEGRO)
    historia = [
    "                ¡FELICIDADES!",
    "",
    "",
    "          Haz superado el 'Nivel 3'",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    " ",
    "",  
    "            Sigue asi, ¡No pares!",
    "",
    "",
    "         Press 'x' para continuar "
    ]   
                    
    y = 30
    for frase in historia:
        texto = fuente.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, 205, 215, estrella3_img)
        y += 30
    pygame.display.flip()

    running = True
    while running:
        global tiempo_pulsar_botón, t
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keystate = pygame.key.get_pressed()
            if keystate [pygame.K_x]:
                running  = False


def show_go_nivel4():
    ventana.fill(NEGRO)
    historia = [
    "                ¡FELICIDADES!",
    "",
    "",
    "          Haz superado el 'Nivel 4'",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    " ",
    "",  
    "            Sigue asi, ¡No pares!",
    "",
    "",
    "         Press 'x' para continuar "
    ]   
                    
    y = 30
    for frase in historia:
        texto = fuente.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, 205, 215, estrella4_img)
        y += 30
    pygame.display.flip()

    running = True
    while running:
        global tiempo_pulsar_botón, t
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keystate = pygame.key.get_pressed()
            if keystate [pygame.K_x]:
                running  = False

def show_go_nivel5():
    ventana.fill(NEGRO)
    historia = [
    "                ¡FELICIDADES!",
    "",
    "",
    "          Haz superado el 'Nivel 5'",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    " ",
    "",  
    "            Sigue asi, ¡No pares!",
    "",
    "",
    "         Press 'x' para continuar "
    ]   
                    
    y = 30
    for frase in historia:
        texto = fuente.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, 205, 215, estrella5_img)
        y += 30
    pygame.display.flip()

    running = True
    while running:
        global tiempo_pulsar_botón, t
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keystate = pygame.key.get_pressed()
            if keystate [pygame.K_x]:
                running  = False

def show_go_nivel6():
    ventana.fill(NEGRO)
    historia = [
    "                ¡FELICIDADES!",
    "",
    "",
    "          Haz superado el 'Nivel 6'",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    " ",
    "",  
    "            Sigue asi, ¡No pares!",
    "",
    "",
    "         Press 'x' para continuar "
    ]   
                    
    y = 30
    for frase in historia:
        texto = fuente.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, 205, 215, estrella6_img)
        y += 30
    pygame.display.flip()

    running = True
    while running:
        global tiempo_pulsar_botón, t
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keystate = pygame.key.get_pressed()
            if keystate [pygame.K_x]:
                running  = False

def show_go_nivel7():
    ventana.fill(NEGRO)
    historia = [
    "                ¡FELICIDADES!",
    "",
    "",
    "          Haz superado el 'Nivel 7'",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    " ",
    "",  
    "            Sigue asi, ¡No pares!",
    "",
    "",
    "         Press 'x' para continuar "
    ]   
                    
    y = 30
    for frase in historia:
        texto = fuente.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, 205, 215, estrella7_img)
        y += 30
    pygame.display.flip()

    running = True
    while running:
        global tiempo_pulsar_botón, t
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keystate = pygame.key.get_pressed()
            if keystate [pygame.K_x]:
                running  = False

def show_go_nivel8():
    ventana.fill(NEGRO)
    historia = [
    "                ¡FELICIDADES!",
    "",
    "",
    "          Haz superado el 'Nivel 8'",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    " ",
    "",  
    "            Sigue asi, ¡No pares!",
    "",
    "",
    "         Press 'x' para continuar "
    ]   
                    
    y = 30
    for frase in historia:
        texto = fuente.render(frase, True, BLANCO)
        ventana.blit(texto, (100, y))
        dibujar_imagen(ventana, 205, 215, estrella8_img)
        y += 30
    pygame.display.flip()

    running = True
    while running:
        global tiempo_pulsar_botón, t
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keystate = pygame.key.get_pressed()
            if keystate [pygame.K_x]:
                running  = False
                
                
#--- VARIABLE GLOBAL ---#
velocidad_enem_o_medic = 4

# puntuacion
score = 0
high_score = 0

nivel = 1
mundo = 1
percepcion = 0

#--- GAME OVER ---#
game_over = True

comentario = True
comentario1 = True
comentario2 = True
comentario3 = True
comentario4 = True
comentario5 = True
comentario6 = True
comentario7 = True
comentario8 = True
comentario9 = True

t = False

tiempo_actual = 0
tiempo_pulsar_botón = 0


###---- BUCLE DEL JUEGO ----#####
running = True   # En partida

# Funcion para insertar datos en la base de datos SQLite (parametros del juego, percepcion de dificultad, desempeño y pulso cardiaco del jugador)
def basedatosmundo1():
    
    global mundo, nivel, numvidas, porcentaje, velocidad_enem_o_medic, percepcion, dspc

    conexion.execute("insert into datos(mundo,nivel,vidasrestantes,porcentajevida,dificultadnivel,percepciondificultad,ppm) values (?,?,?,?,?,?,?)", (mundo,nivel,numvidas,porcentaje,velocidad_enem_o_medic,percepcion,dspc))
    conexion.commit()


#############################################
#------- DATOS DE SENSORES (SEÑALES) -------#
#############################################

# Funcion de interrupcion 
# Lectura de los sensores porvenientes de arduino por medio de puerto serial 
def timer_interrupt():
    
    global dsp, dspc
    datos = ser.readline()           # leer los datos de la variable "ser", y se almacena en la varobale datos
    datos1 = datos.decode('utf-8')   # decodifica una cadena codificada en formato UTF-8

    datos2 = datos1.split(',')       # divide una cadena en una lista, con una coma

    d1= datos2[0]  
    d11 = float(d1)
    dsp = int(d11)                   # dato sensor final de carrera

    d3=datos2[2]
    d33 = float(d3)
    dspc = int(d33)                  # dato sensor de frecuencia cardiaca
    print(dspc)

    # Genera una interrupcion cada determinado tiempo para actualizar los datos de los sensores
    threading.Timer(0.001,timer_interrupt).start()   

threading.Timer(0.001, timer_interrupt).start()

# Funcion - escalar variable frecuancia cardiaca
def timer_interruptmundo1():

    global pulso, dspc
    pulso = (dspc*100)/100
    

######################## RUNNING #############################
while running:

    time.sleep(0.0001)

    if game_over:
        show_go_ventana()
        game_over = False
        
        # Grupo de todos los sprites
        all_sprites = pygame.sprite.Group()

        # Grupo de sprites de solo enemigos 
        mobs = pygame.sprite.Group()
        asteriodes = pygame.sprite.Group()

        # Creaccion de una instacia de la clase Player e Instructor
        player = Player()
        
        instru = Instructor(position=((ANCHO - ANCHO//2.5), ALTO - ALTO//2), images=images, delay = 0.03)

        # Añadimos elementos al grupo de sprites
        all_sprites.add(player)
        all_sprites.add(instru)

        # Crea nuevos sprites 
        for i in range(8):
            asteroide_nuevo()

        for i in range(1):
                mob_nuevo()
       
        # Inicializacion de variables 
        score = 0
        nivel = 1
        mundo = 1
        cont = 0

        comentario = True
        comentario1 = True
        comentario2 = True
        comentario3 = True
        comentario4 = True
        comentario5 = True
        comentario6 = True
        comentario7 = True
        comentario8 = True

        velocidad_enem_o_medic = 5

    # Muestra en orden la historia inicial del juego 
    if running:
        if comentario1:
            show_go_ventana1()
            comentario1 = False
        
    if running:
        if comentario5:
            go_ventana1()
            comentario5 = False

    if running:
        if comentario:
            go_ventana()
            comentario = False

    # Tiempo establecido para cada etapa de ejercicio - se refleja en la barra de tiempo del juego 
    tiempo_actual1 = int(tiempo_actual/1000)
    tiempo_pulsar_botón1 = int(tiempo_pulsar_botón/1000)
    
    # Mantiene el bucle funcionando a la velocidad correcta
    reloj.tick(FPS)
    tiempoinstru = reloj.tick(FPS)/2000

    # Entrada de procesos (eventos)
    for evento in pygame.event.get():
        # Comprobar si se cierra la ventana
        if evento.type == pygame.QUIT:
            running = False
    
    # Condiciones - si el jugador pierde todas sus vidas  
    if player.numerovidas == 0:
        if comentario8:
            numvidas = player.numerovidas
            porcentaje = 0
            go_ventana4()
            comentario8 = False

    if mundo ==1 and t:
        tiempo_actual = pygame.time.get_ticks()

        # Condicion para la etapa 1 de ejercicio 
        if tiempo_actual - tiempo_pulsar_botón > 60000 and nivel == 1: 
            tiempo_pulsar_botón = tiempo_actual 
            t = False

            # Muestra la escena de bonificacion 1 y se guarda los valores "player.numerovidas" y "player.vida/100" 
            # en las variables "numvidas" y "porcentaje" para insertar estos valores en la base de datos SQLite
            show_go_nivel1()
            if comentario8:
                numvidas = player.numerovidas
                porcentaje = player.vida/100
                go_ventana4()
                comentario8 = False
            
            # Condiciones de ajuste automatico de parametros - Tomadas del Arbol de decision 
            if pulso < 98 and numvidas >= 3 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont += 1
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic < 6:
                velocidad_enem_o_medic += 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -=1
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            # Restrablece el valor de variables como numero de vidas y porcetanje de vida 
            player.vida = 100
            player.numerovidas = 3
            nivel += 1
            comentario8 = True

        # Condicion para la etapa 2 de ejercicio    
        if tiempo_actual - tiempo_pulsar_botón > 60000 and nivel == 2: 
            tiempo_pulsar_botón = tiempo_actual 
            t = False

            # Muestra la escena de bonificacion 2 y se guarda los valores "player.numerovidas" y "player.vida/100" 
            # en las variables "numvidas" y "porcentaje" para insertar estos valores en la base de datos SQLite
            show_go_nivel2()
            if comentario8:
                numvidas = player.numerovidas
                porcentaje = player.vida/100
                go_ventana4()
                comentario8 = False
            
            # Condiciones de ajuste automatico de parametros - Tomadas del Arbol de decision
            if pulso < 98 and numvidas >= 3 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont += 1
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic < 6:
                velocidad_enem_o_medic += 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -=1
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            # Restrablece el valor de variables como numero de vidas y porcetanje de vida 
            player.vida = 100
            player.numerovidas = 3
            nivel += 1
            comentario8 = True
        
        # Condicion para la etapa 3 de ejercicio
        if tiempo_actual - tiempo_pulsar_botón > 60000 and nivel == 3: 
            tiempo_pulsar_botón = tiempo_actual 
            t = False

            # Muestra la escena de bonificacion 3 y se guarda los valores "player.numerovidas" y "player.vida/100" 
            # en las variables "numvidas" y "porcentaje" para insertar estos valores en la base de datos SQLite
            show_go_nivel3()
            if comentario8:
                numvidas = player.numerovidas
                porcentaje = player.vida/100
                go_ventana4()
                comentario8 = False

            # Condiciones de ajuste automatico de parametros - Tomadas del Arbol de decision
            if pulso < 98 and numvidas >= 3 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont += 1
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic < 6:
                velocidad_enem_o_medic += 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -=1
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1
            
            # Restrablece el valor de variables como numero de vidas y porcetanje de vida 
            player.vida = 100
            player.numerovidas = 3
            nivel += 1
            comentario8 = True

        # Condicion para la etapa 4 de ejercicio
        if tiempo_actual - tiempo_pulsar_botón > 60000 and nivel == 4: 
            tiempo_pulsar_botón = tiempo_actual 
            t = False

            # Muestra la escena de bonificacion 4 y se guarda los valores "player.numerovidas" y "player.vida/100" 
            # en las variables "numvidas" y "porcentaje" para insertar estos valores en la base de datos SQLite
            show_go_nivel4()
            if comentario8:
                numvidas = player.numerovidas
                porcentaje = player.vida/100
                go_ventana4()
                comentario8 = False
            
            # Condiciones de ajuste automatico de parametros - Tomadas del Arbol de decision
            if pulso < 98 and numvidas >= 3 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont += 1
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic < 6:
                velocidad_enem_o_medic += 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -=1
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1
            
            # Restrablece el valor de variables como numero de vidas y porcetanje de vida 
            player.vida = 100
            player.numerovidas = 3
            nivel += 1
            comentario8 = True 
        
        # Condicion para la etapa 5 de ejercicio
        if tiempo_actual - tiempo_pulsar_botón > 60000 and nivel == 5:
            tiempo_pulsar_botón = tiempo_actual 
            t = False

            # Muestra la escena de bonificacion 5 y se guarda los valores "player.numerovidas" y "player.vida/100" 
            # en las variables "numvidas" y "porcentaje" para insertar estos valores en la base de datos SQLite
            show_go_nivel5()
            if comentario8:
                numvidas = player.numerovidas
                porcentaje = player.vida/100
                go_ventana4()
                comentario8 = False
            
            # Condiciones de ajuste automatico de parametros - Tomadas del Arbol de decision
            if pulso < 98 and numvidas >= 3 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont += 1
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic < 6:
                velocidad_enem_o_medic += 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -=1
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1
            
            # Restrablece el valor de variables como numero de vidas y porcetanje de vida 
            player.vida = 100
            player.numerovidas = 3
            nivel += 1
            comentario8 = True

        # Condicion para la etapa 6 de ejercicio
        if tiempo_actual - tiempo_pulsar_botón > 60000 and nivel == 6: 
            tiempo_pulsar_botón = tiempo_actual 
            t = False

            # Muestra la escena de bonificacion 6 y se guarda los valores "player.numerovidas" y "player.vida/100" 
            # en las variables "numvidas" y "porcentaje" para insertar estos valores en la base de datos SQLite
            show_go_nivel6()
            if comentario8:
                numvidas = player.numerovidas
                porcentaje = player.vida/100
                go_ventana4()
                comentario8 = False

            # Condiciones de ajuste automatico de parametros - Tomadas del Arbol de decision
            if pulso < 98 and numvidas >= 3 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont += 1
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic < 6:
                velocidad_enem_o_medic += 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -=1
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            # Restrablece el valor de variables como numero de vidas y porcetanje de vida 
            player.vida = 100
            player.numerovidas = 3
            nivel += 1
            comentario8 = True
        
        # Condicion para la etapa 7 de ejercicio
        if tiempo_actual - tiempo_pulsar_botón > 60000 and nivel == 7: 
            tiempo_pulsar_botón = tiempo_actual 
            t = False

            # Muestra la escena de bonificacion 7 y se guarda los valores "player.numerovidas" y "player.vida/100" 
            # en las variables "numvidas" y "porcentaje" para insertar estos valores en la base de datos SQLite
            show_go_nivel7()
            if comentario8:
                numvidas = player.numerovidas
                porcentaje = player.vida/100
                go_ventana4()
                comentario8 = False
            
            # Condiciones de ajuste automatico de parametros - Tomadas del Arbol de decision
            if pulso < 98 and numvidas >= 3 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont += 1
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic < 6:
                velocidad_enem_o_medic += 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso >= 98 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -=1
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 0:
                velocidad_enem_o_medic -= 0.5
            
            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic > 4 and cont == 1:
                velocidad_enem_o_medic -= 0.5
                cont -= 1

            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso >= 98 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic

            elif pulso < 98 and numvidas < 3 and velocidad_enem_o_medic == 4 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1

            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 0:
                velocidad_enem_o_medic == velocidad_enem_o_medic
            
            elif pulso < 98 and numvidas >= 3 and cont == 1 and velocidad_enem_o_medic == 6 and cont == 1:
                velocidad_enem_o_medic == velocidad_enem_o_medic
                cont -= 1
            
            # Restrablece el valor de variables como numero de vidas y porcetanje de vida 
            player.vida = 100
            player.numerovidas = 3
            nivel += 1
            comentario8 = True

        # Condicion para la etapa 8 de ejercicio
        if tiempo_actual - tiempo_pulsar_botón > 60000 and nivel == 8:
            tiempo_pulsar_botón = tiempo_actual
            t = True
            
            # Muestra la escena de bonificacion 8 y se guarda los valores "player.numerovidas" y "player.vida/100" 
            # en las variables "numvidas" y "porcentaje" para insertar estos valores en la base de datos SQLite
            show_go_nivel8() 
            if comentario8:
                numvidas = player.numerovidas
                porcentaje = player.vida/100
                go_ventana4()
                comentario8 = False
            
            # Muestra en orden la historia final del juego 
            if comentario3:
                show_go_ventana2()   
                comentario3 = False
            
            if comentario4:
                show_go_ventana4()
                comentario4 = False
            
            if comentario9:
                go_ventana5()
                game_over = True
        
    # Actualizar
    all_sprites.update()
    
    #########################################################
    #----- COLISION JUGADOR (PLAYER) CON ENEMIGO (MOB) -----#
    #########################################################
    colision()

    # Dibujar / Renderizar
    ventana.fill(NEGRO)
    esenarios()
    all_sprites.draw(ventana)

    # Movimiento del Instructor
    instru.comportamiento(tiempoinstru)
    
    # Muestra y ubica los objetos en la escena del juego
    dibujar_barra_vida(ventana, (20*3)+10, 8, player.vida)
    dibujar_numerovidas(ventana, 5, 5, player.numerovidas, vidas_img)
    dibujar_score_o_high_score_o_nivel(ventana, "Score", 27, (ANCHO-35, ALTO//3.5))
    dibujar_score_o_high_score_o_nivel(ventana, str(score), 25, (ANCHO-35, ALTO//3))
    dibujar_score_o_high_score_o_nivel(ventana, "High Score:", 23, (ANCHO-350, 0))
    dibujar_score_o_high_score_o_nivel(ventana, str(high_score), 23, (ANCHO-270, 1))
    dibujar_score_o_high_score_o_nivel(ventana, "Nivel", 22, (33, 20))  
    dibujar_score_o_high_score_o_nivel(ventana, str(nivel), 20, (33, 40))  
    draw_text1(ventana, "Time", 25, 762, 560)

    # Muestra y ubica por un determinado tiempo los dialogos motivacionales en la escena del juego 
    if mundo == 1:
        if tiempo_actual - tiempo_pulsar_botón > 3000 and tiempo_actual - tiempo_pulsar_botón < 11000 and nivel ==1:
            dibujar_dialogo(ventana, 320, 170) 
        if tiempo_actual - tiempo_pulsar_botón > 21000 and tiempo_actual - tiempo_pulsar_botón < 29000 and nivel ==1:
            dibujar_dialogo3(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 39000 and tiempo_actual - tiempo_pulsar_botón < 47000 and nivel ==1:
            dibujar_dialogo7(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 57000 and tiempo_actual - tiempo_pulsar_botón < 600000 and nivel ==1:
            dibujar_dialogo5(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 3000 and tiempo_actual - tiempo_pulsar_botón < 11000 and nivel ==2:
            dibujar_dialogo2(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 21000 and tiempo_actual - tiempo_pulsar_botón < 29000 and nivel ==2:
            dibujar_dialogo3(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 39000 and tiempo_actual - tiempo_pulsar_botón < 47000 and nivel ==2:
            dibujar_dialogo4(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 57000 and tiempo_actual - tiempo_pulsar_botón < 60000 and nivel ==2:
            dibujar_dialogo7(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 3000 and tiempo_actual - tiempo_pulsar_botón < 11000 and nivel ==3:
            dibujar_dialogo3(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 21000 and tiempo_actual - tiempo_pulsar_botón < 29000 and nivel ==3:
            dibujar_dialogo12(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 39000 and tiempo_actual - tiempo_pulsar_botón < 47000 and nivel ==3:
            dibujar_dialogo(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 57000 and tiempo_actual - tiempo_pulsar_botón < 60000 and nivel ==3:
            dibujar_dialogo7(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 2000 and tiempo_actual - tiempo_pulsar_botón < 10000 and nivel ==4:
            dibujar_dialogo4(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 20000 and tiempo_actual - tiempo_pulsar_botón < 28000 and nivel ==4:
            dibujar_dialogo3(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 38000 and tiempo_actual - tiempo_pulsar_botón < 46000 and nivel ==4:
            dibujar_dialogo7(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 56000 and tiempo_actual - tiempo_pulsar_botón < 60000 and nivel ==4:
            dibujar_dialogo5(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 3000 and tiempo_actual - tiempo_pulsar_botón < 11000 and nivel ==5:
            dibujar_dialogo12(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 21000 and tiempo_actual - tiempo_pulsar_botón < 29000 and nivel ==5:
            dibujar_dialogo3(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 39000 and tiempo_actual - tiempo_pulsar_botón < 47000 and nivel ==5:
            dibujar_dialogo4(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 57000 and tiempo_actual - tiempo_pulsar_botón < 60000 and nivel ==5:
            dibujar_dialogo7(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 3000 and tiempo_actual - tiempo_pulsar_botón < 11000 and nivel ==6:
            dibujar_dialogo2(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 21000 and tiempo_actual - tiempo_pulsar_botón < 29000 and nivel ==6:
            dibujar_dialogo3(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 39000 and tiempo_actual - tiempo_pulsar_botón < 47000 and nivel ==6:
            dibujar_dialogo4(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 57000 and tiempo_actual - tiempo_pulsar_botón < 60000 and nivel ==6:
            dibujar_dialogo7(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 3000 and tiempo_actual - tiempo_pulsar_botón < 11000 and nivel ==7:
            dibujar_dialogo(ventana, 320, 170) 
        if tiempo_actual - tiempo_pulsar_botón > 21000 and tiempo_actual - tiempo_pulsar_botón < 29000 and nivel ==7:
            dibujar_dialogo3(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 39000 and tiempo_actual - tiempo_pulsar_botón < 47000 and nivel ==7:
            dibujar_dialogo7(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 57000 and tiempo_actual - tiempo_pulsar_botón < 600000 and nivel ==7:
            dibujar_dialogo5(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 3000 and tiempo_actual - tiempo_pulsar_botón < 11000 and nivel ==8:
            dibujar_dialogo12(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 21000 and tiempo_actual - tiempo_pulsar_botón < 29000 and nivel ==8:
            dibujar_dialogo3(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 39000 and tiempo_actual - tiempo_pulsar_botón < 47000 and nivel ==8:
            dibujar_dialogo4(ventana, 320, 170)
        if tiempo_actual - tiempo_pulsar_botón > 57000 and tiempo_actual - tiempo_pulsar_botón < 60000 and nivel ==8:
            dibujar_dialogo7(ventana, 320, 170)
    
    # Mostrar en pantalla todo lo que se programa
    pygame.display.flip()

# Cierra Pygame
pygame.quit()
sys.exit(0)
