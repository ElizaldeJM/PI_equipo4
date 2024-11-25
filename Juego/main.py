import sys
import pygame
import dificultades  # Cambiado a dificultades en lugar de niveles
import json
import configuracion
import historia
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("musica/musica.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)
boton_sound = pygame.mixer.Sound("musica/sonidodeboton.mp3")
with open('idioma.json') as formato:
    textoConfig= json.load(formato)
# Dimensiones base de la pantalla
W, H = 1280, 720
pantalla = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("Tortuga al agua")

# Icono de la ventana
icono = pygame.image.load("imagenes/Run9.png")
pygame.display.set_icon(icono)
def cargar_fondo():
    global fondo_inicio
    with open('idioma.json') as formato:
        textoConfig = json.load(formato)
    fondo_inicio = pygame.image.load(textoConfig[lenguaje]['inicio']['imagen_inicio']).convert()

    
lenguaje = "esp"
cargar_fondo()
# Imágenes de fondo para la animación
fondos_animacion = [
    pygame.image.load("imagenes/fondo1final.png").convert(),
    pygame.image.load("imagenes/fondo1final2.png").convert(),
    pygame.image.load("imagenes/fondo1final3.png").convert()
]
imagenes_idiomas = [
    pygame.transform.scale(pygame.image.load("idiomas/mexico.png").convert_alpha(), (200, 200)),
    pygame.transform.scale(pygame.image.load("idiomas/usa.png").convert_alpha(), (200, 200))
]

indice_fondo = 0
contador_animacion = 0
duracion_animacion = 30

# Reloj
FPS = 120
RELOJ = pygame.time.Clock()

pantalla_completa = False

class AnimacionCangrejo:
    def __init__(self, x, y, escala, duracion, rango_x, velocidad):
        self.imagenes = [pygame.image.load(f"imagenes/cangre{i}.png").convert_alpha() for i in range(1, 9)]
        self.imagenes = [pygame.transform.scale(imagen, (int(imagen.get_width() * escala), int(imagen.get_height() * escala))) for imagen in self.imagenes]
        self.x = x
        self.y = y
        self.rango_x = rango_x
        self.velocidad = velocidad
        self.indice = 0
        self.contador = 0
        self.direccion = 1
        self.duracion = duracion
        self.invertida = False

    def actualizar(self):
        self.contador += 1
        if self.contador >= self.duracion:
            self.indice = (self.indice + 1) % len(self.imagenes)
            self.contador = 0

        self.x += self.velocidad * self.direccion

        if self.x >= 1000 and not self.invertida:
            self.invertida = True
            self.imagenes = [pygame.transform.flip(imagen, True, False) for imagen in self.imagenes]
        elif self.x <= 240 and self.invertida:
            self.invertida = False
            self.imagenes = [pygame.transform.flip(imagen, True, False) for imagen in self.imagenes]

        if self.x <= self.rango_x[0] or self.x >= self.rango_x[1]:
            self.direccion *= -1

    def dibujar(self, pantalla):
        pantalla.blit(self.imagenes[self.indice], (self.x, self.y))


cangrejo_animado = AnimacionCangrejo(
    x=600, y=420, escala=0.5, duracion=5,
    rango_x=(240, 1000),
    velocidad=1
)

class Boton:
    def __init__(self, imagen_normal, imagen_resaltada, x, y, accion):
        self.imagen_normal = pygame.image.load(imagen_normal).convert_alpha()
        self.imagen_resaltada = pygame.image.load(imagen_resaltada).convert_alpha()
        self.rect = self.imagen_normal.get_rect()
        self.rect.topleft = (x, y)
        self.accion = accion
        self.imagen_actual = self.imagen_normal
        self.pressed = False

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen_actual, self.rect.topleft)

    def click(self):
        if not self.pressed:
            self.pressed = True
            self.imagen_actual = self.imagen_resaltada
            if self.accion:
                self.accion()
    def release(self):
        self.pressed = False
        self.imagen_actual = self.imagen_normal

    def mouse_over(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.imagen_actual = self.imagen_resaltada
        else:
            self.imagen_actual = self.imagen_normal
            
def cambiar_idioma():
    boton_sound.play()
    global lenguaje
    if lenguaje == "ing":
        lenguaje = "esp"
    else:
        lenguaje = "ing"
    cargar_fondo()  # Cambiar el fondo según el idioma
    print(f"Idioma cambiado a: {lenguaje}, Fondo: {textoConfig[lenguaje]['inicio']['imagen_inicio']}")


def ver_controles():
    boton_sound.play()
    reloj = pygame.time.Clock()
    configuracion.mostrar_configuracion(pantalla, reloj)

    def actualizar(self):
        self.contador += 1
        if self.contador >= self.duracion:
            self.indice = (self.indice + 1) % len(self.imagenes)
            self.contador = 0
        
        self.x += self.velocidad_x
        if self.x > W or self.x < 0:
            self.velocidad_x *= -1

    def dibujar(self, pantalla):
        pantalla.blit(self.imagenes[self.indice], (self.x, self.y))

# Acciones de los botones
def iniciar_niveles():
    boton_sound.play()
    fondo = pygame.image.load("imagenes/fondo.jpg").convert()
    reloj = pygame.time.Clock()
    dificultades.mostrar_dificultades(pantalla, fondo, reloj)



def salir():
    pygame.quit()
    sys.exit()

def alternar_pantalla_completa():
    global pantalla, pantalla_completa
    pantalla_completa = not pantalla_completa
    if pantalla_completa:
        pantalla = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
    else:
        pantalla = pygame.display.set_mode((W, H), pygame.RESIZABLE)
def alternar_volumen():
    if pygame.mixer.music.get_volume() > 0:
        pygame.mixer.music.set_volume(0)
        boton_volumen.imagen_normal = pygame.image.load("botones/nada1.png").convert_alpha()
        boton_volumen.imagen_resaltada = pygame.image.load("botones/nada2.png").convert_alpha()
    else:
        pygame.mixer.music.set_volume(1.0)
        boton_volumen.imagen_normal = pygame.image.load("botones/maximo1.png").convert_alpha()
        boton_volumen.imagen_resaltada = pygame.image.load("botones/maximo2.png").convert_alpha()

# Creación de botones con imágenes
botones = [
    Boton("botones/boton_empezar.png", "botones/boton_presionado.png", W // 2, 320, iniciar_niveles),
    Boton ("idiomas/mexico.png", "idiomas/usa.png", W// 2, 440, cambiar_idioma)
]
# Crear un botón para los controles, suponiendo que tengas las imágenes para el botón
botones.append(Boton("botones/confi_1.png", "botones/confi_2.png", W // 2, 560, ver_controles))

boton_volumen = Boton(
    "botones/maximo1.png",  # Imagen inicial para volumen máximo
    "botones/maximo2.png",  # Imagen resaltada para volumen máximo
    50, 50,  # Coordenadas del botón (ajusta si es necesario)
    alternar_volumen  # Acción al presionar el botón
)
botones.append(boton_volumen)
def liberar_botones():
    for boton in botones:
        boton.release()
# Funciones de volumen
def ajustar_volumen(delta):
    volumen_actual = pygame.mixer.music.get_volume()
    nuevo_volumen = max(0, min(1, volumen_actual + delta))
    pygame.mixer.music.set_volume(nuevo_volumen)
def silenciar_volumen():
    if pygame.mixer.music.get_volume() > 0:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(1.0)
        

def main():
    global indice_fondo, contador_animacion, lenguaje
    
    lenguaje = "esp"
    with open('idioma.json') as formato:
        textoConfig= json.load(formato)

    print("play", textoConfig[lenguaje]['inicio']['imagen_inicio'])

    pygame.mixer.init()
    while True:
        contador_animacion += 1
        if contador_animacion >= duracion_animacion:
            indice_fondo = (indice_fondo + 1) % len(fondos_animacion)
            contador_animacion = 0

        pantalla.blit(fondo_inicio, (0, 0))  # Usar el fondo correspondiente al idioma

        cangrejo_animado.actualizar()
        cangrejo_animado.dibujar(pantalla)

        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_f:
                    alternar_pantalla_completa()
                elif evento.key == pygame.K_UP:
                    ajustar_volumen(0.1)
                elif evento.key == pygame.K_DOWN:
                    ajustar_volumen(-0.1)
                elif evento.key == pygame.K_m:
                    silenciar_volumen()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for boton in botones:
                    if boton.rect.collidepoint(mouse_pos):
                        boton.click()
            if evento.type == pygame.MOUSEBUTTONUP:
                for boton in botones:
                    boton.release()

        for boton in botones:
            boton.mouse_over(mouse_pos)
            boton.dibujar(pantalla)

        pygame.display.update()
        RELOJ.tick(FPS)

if __name__ == "__main__":
    main()