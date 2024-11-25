import pygame
import sys
import niveles
import nivdific  # Importa el archivo nivdific
import main  # Importa el archivo main

# Configuración de Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("musica/musica.mp3")
pygame.mixer.music.play(-1)
boton_sound = pygame.mixer.Sound("musica/sonidodeboton.mp3")

W, H = 1280, 720
screen = pygame.display.set_mode((W, H)) 
pygame.display.set_caption("Selección de Dificultad")
fondo = pygame.image.load('imagenes/fondo.jpg') 

boton_normal = pygame.image.load('botones/simple1.png')  # Botón dificultad normal
boton_presionado = pygame.image.load('botones/simple2.png')  # Botón dificultad presionado

boton_normal2 = pygame.image.load('botones/complicado1.png')  # Botón dificultad complicado
boton_presionado2 = pygame.image.load('botones/complicado2.png')  # Botón complicado presionado

boton_regresar_normal =pygame.transform.scale(pygame.image.load('botones/regresar1.png'), (100,80))  # Botón regresar
boton_regresar_presionado =pygame.transform.scale(pygame.image.load('botones/regresar2.png'), (100,80))  # Botón regresar

# Rectángulos de los botones, centrar en pantalla
boton_rect = boton_normal.get_rect(center=(W // 2, 350))  # Botón sencillo
boton_rect2 = boton_normal2.get_rect(center=(W // 2, 450))  # Botón complicado
boton_regresar_rect = boton_regresar_normal.get_rect(center=(W // 2, 550))  # Botón regresar


def mostrar_dificultades(pantalla, fondo, reloj):
    """Función para mostrar la pantalla de selección de dificultades."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Asegurarse de salir completamente

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    boton_sound.play()
                    main.main()
                    return



        # Dibujar la imagen de fondo
        pantalla.blit(fondo, (0, 0))

        # Obtener la posición del mouse y los clics
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Dificultad Sencilla
        if boton_rect.collidepoint(mouse_pos):
            pantalla.blit(boton_presionado, boton_rect)
            if mouse_click[0]:
                boton_sound.play()
                niveles.mostrar_niveles(pantalla, fondo, reloj)
                return
        else:
            pantalla.blit(boton_normal, boton_rect)

        # Dificultad Complicada
        if boton_rect2.collidepoint(mouse_pos):
            pantalla.blit(boton_presionado2, boton_rect2)
            if mouse_click[0]:
                boton_sound.play()
                nivdific.dificil()  # Llama a la función del archivo nivdific.py
                return
        else:
            pantalla.blit(boton_normal2, boton_rect2)

        # Botón Regresar
        if boton_regresar_rect.collidepoint(mouse_pos):
            pantalla.blit(boton_regresar_presionado, boton_regresar_rect)
            if mouse_click[0]:
                boton_sound.play()
                main.main()  # Llama a la función de main.py
                return
        else:
            pantalla.blit(boton_regresar_normal, boton_regresar_rect)

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)  # Limitar a 60 FPS


if __name__ == "__main__":
    # Pasar pantalla y reloj al llamar
    mostrar_dificultades(screen, fondo, pygame.time.Clock())
