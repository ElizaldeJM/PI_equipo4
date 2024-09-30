import pygame
import sys
import nivel1 

# Configuración de Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Juego/musica.mp3")
pygame.mixer.music.play(-1)
W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Selección de Niveles")

# Cargar las imágenes de fondo y del botón
fondo = pygame.image.load('imagenes/fondo.jpg')  # Cargar imagen de fondo
boton_normal = pygame.image.load(
    'imagenes/nivel11.png')  # Imagen del botón normal
boton_presionado = pygame.image.load(
    'imagenes/nivel11p.png')  # Imagen del botón presionado



# Dimensiones del botón
# Centra el botón en la pantalla
boton_rect = boton_normal.get_rect(center=(W // 2, H // 2 + 40))


def mostrar_niveles(pantalla, fondo, reloj):
    """Función para mostrar la pantalla de selección de niveles."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Asegurarse de salir completamente

        # Dibujar la imagen de fondo
        pantalla.blit(fondo, (0, 0))

        # Comprobar si el mouse está sobre el botón
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Si el mouse está sobre el botón
        if boton_rect.collidepoint(mouse_pos):
            # Mostrar imagen presionada
            pantalla.blit(boton_presionado, boton_rect)
            if mouse_click[0]:  # Si se hace clic izquierdo
                nivel1.jugar_nivel()  # Inicia el nivel 1
                pygame.mixer.music.load("Juego/musicanivel1.mp3")
                pygame.mixer.music.play(-1)
                return  # Regresar a la selección de niveles (o terminar)
        else:
            pantalla.blit(boton_normal, boton_rect)  # Mostrar imagen normal

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)  # Limitar a 60 FPS


if __name__ == "__main__":
    # Pasar pantalla y reloj al llamar
    mostrar_niveles(screen, fondo, pygame.time.Clock())
