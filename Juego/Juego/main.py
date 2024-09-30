import sys
import pygame
import niveles  # Cambiado de Nivel1 a niveles


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Juego/musica.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

# Dimensiones base de la pantalla
W, H = 1280, 720
pantalla = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("Menú Principal")

# Icono de la ventana
icono = pygame.image.load("imagenes/Run9.png")
pygame.display.set_icon(icono)

# Imágenes de fondo para la animación
fondos_animacion = [
    pygame.image.load("imagenes/menu1.jpg").convert(),
    pygame.image.load("imagenes/menu2.jpg").convert(),
    pygame.image.load("imagenes/menu3.jpg").convert()
]

# Índice y contador para la animación del fondo
indice_fondo = 0
contador_animacion = 0
# Número de fotogramas que dura cada imagen (ajústalo según la velocidad deseada)
duracion_animacion = 30

# Reloj
FPS = 120
RELOJ = pygame.time.Clock()

# Bandera de pantalla completa
pantalla_completa = False


class Boton:
    def __init__(self, imagen_normal, imagen_resaltada, x, y, accion):
        self.imagen_normal = pygame.image.load(imagen_normal).convert_alpha()
        self.imagen_resaltada = pygame.image.load(
            imagen_resaltada).convert_alpha()
        self.rect = self.imagen_normal.get_rect()
        self.rect.topleft = (x, y)
        self.accion = accion
        self.imagen_actual = self.imagen_normal

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen_actual, self.rect.topleft)

    def click(self):
        self.imagen_actual = self.imagen_resaltada  # Cambiar imagen al hacer clic
        if self.accion:
            self.accion()

    def mouse_over(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.imagen_actual = self.imagen_resaltada
        else:
            self.imagen_actual = self.imagen_normal

# Acciones de los botones


def iniciar_niveles():
    # Aquí llamamos a la función de mostrar_niveles de niveles.py
    fondo = pygame.image.load("imagenes/fondo.jpg").convert()
    reloj = pygame.time.Clock()
    niveles.mostrar_niveles(pantalla, fondo, reloj)
    


def ver_historia():
    # Aquí puedes definir la función para mostrar la historia
    pass


def mostrar_creditos():
    # Aquí puedes definir la función para mostrar los créditos
    pass


def salir():
    pygame.quit()
    sys.exit()

# Función para alternar entre pantalla completa y ventana


def alternar_pantalla_completa():
    global pantalla, pantalla_completa
    pantalla_completa = not pantalla_completa
    if pantalla_completa:
        pantalla = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
    else:
        pantalla = pygame.display.set_mode((W, H), pygame.RESIZABLE)


# Creación de botones con imágenes
botones = [
    Boton("imagenes/boton_empezar.png","imagenes/boton_presionado.png", 640, 360, iniciar_niveles),
    Boton("imagenes/confi_1.png", "imagenes/confi_2.png", 10, 30, iniciar_niveles)
]


def main():
    global indice_fondo, contador_animacion

    while True:
        # Controlar la animación del fondo
        contador_animacion += 1
        if contador_animacion >= duracion_animacion:
            # Cambiar al siguiente fondo
            indice_fondo = (indice_fondo + 1) % len(fondos_animacion)
            contador_animacion = 0

        # Dibujar fondo animado
        pantalla.blit(fondos_animacion[indice_fondo], (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir()

            if evento.type == pygame.KEYDOWN:
                # Tecla para alternar pantalla completa (por ejemplo, la tecla 'F')
                if evento.key == pygame.K_f:
                    alternar_pantalla_completa()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for boton in botones:
                    if boton.rect.collidepoint(mouse_pos):
                        boton.click()

        # Actualizar estado de los botones
        for boton in botones:
            boton.mouse_over(mouse_pos)
            boton.dibujar(pantalla)

        pygame.display.update()
        RELOJ.tick(FPS)


if __name__ == "__main__":
    main()
