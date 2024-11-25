import pygame
import sys
import nivel1
import nivel2
import nivel3

# Configuración de Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("musica/musica.mp3")
pygame.mixer.music.play(-1)
boton_sound = pygame.mixer.Sound("musica/sonidodeboton.mp3")

W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Selección de Niveles")

# Cargar las imágenes de fondo y de los botones
fondo = pygame.image.load('imagenes/fondo.jpg')  # Imagen de fondo
boton_normal = pygame.image.load('botones/nivel11.png')  # Botón nivel 1 normal
boton_presionado = pygame.image.load('botones/nivel11p.png')  # Botón nivel 1 presionado

boton_normal2 = pygame.image.load('botones/nivel22.png')  # Botón nivel 2 normal
boton_presionado2 = pygame.image.load('botones/nivel22p.png')  # Botón nivel 2 presionado

boton_normal3 = pygame.image.load('botones/nivel33.png')  # Botón nivel 3 normal
boton_presionado3 = pygame.image.load('botones/nivel33p.png')  # Botón nivel 3 presionado

# Botón regresar
boton_regresar_normal = pygame.image.load('botones/regresar1.png')  # Botón normal
boton_regresar_presionado = pygame.image.load('botones/regresar2.png')  # Botón presionado
boton_regresar_rect = boton_regresar_normal.get_rect(topleft=(10, 10))  # Coloca en la esquina superior izquierda

# Rectángulos de los botones, centrar en pantalla
boton_rect = boton_normal.get_rect(center=(W // 2, 300))  # Botón nivel 1
boton_rect2 = boton_normal2.get_rect(center=(W // 2, 400))  # Botón nivel 2
boton_rect3 = boton_normal3.get_rect(center=(W // 2, 500))  # Botón nivel 3

boton_presionado_flag = None

def liberar_botones():
    global boton_presionado_flag
    boton_presionado_flag = None

def mostrar_niveles(pantalla, fondo, reloj):
    """Función para mostrar la pantalla de selección de niveles."""
    global boton_presionado_flag
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Asegurarse de salir completamente
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                boton_sound.play()
                return
            if event.type == pygame.MOUSEBUTTONUP:
                liberar_botones()
        # Dibujar la imagen de fondo
        pantalla.blit(fondo, (0, 0))

        # Obtener la posición del mouse y los clics
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Mostrar el botón de regresar
        if boton_regresar_rect.collidepoint(mouse_pos):
            if mouse_click[0]:
                boton_sound.play()
                return  # Salir de la función y regresar al menú anterior
            pantalla.blit(boton_regresar_presionado, boton_regresar_rect)
        else:
            pantalla.blit(boton_regresar_normal, boton_regresar_rect)

        # Nivel 1
        if boton_rect.collidepoint(mouse_pos):
            if mouse_click[0] and boton_presionado_flag is None:
                boton_presionado_flag = boton_rect
                pantalla.blit(boton_presionado, boton_rect)
                boton_sound.play()
                nivel1.jugar_nivel()  # Inicia el nivel 1
                return
            pantalla.blit(boton_presionado if boton_presionado_flag == boton_rect else boton_normal, boton_rect)
        else:
            pantalla.blit(boton_normal, boton_rect)

        # Nivel 2
        if boton_rect2.collidepoint(mouse_pos):
            if mouse_click[0] and boton_presionado_flag is None:
                boton_presionado_flag = boton_rect2
                pantalla.blit(boton_presionado2, boton_rect2)
                boton_sound.play()
                nivel2.jugar_nivel()  # Inicia el nivel 2
                return
        else:
            pantalla.blit(boton_normal2, boton_rect2)

        # Nivel 3 (nuevo botón añadido)
        if boton_rect3.collidepoint(mouse_pos):
            if mouse_click[0] and boton_presionado_flag is None:
                boton_presionado_flag = boton_rect3
                pantalla.blit(boton_presionado3, boton_rect3)
                boton_sound.play()
                nivel3.jugar_nivel()  # Inicia el nivel 3
                return
        else:
            pantalla.blit(boton_normal3, boton_rect3)
        
        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)  # Limitar a 60 FPS


if __name__ == "__main__":
    # Pasar pantalla y reloj al llamar
    mostrar_niveles(screen, fondo, pygame.time.Clock())
