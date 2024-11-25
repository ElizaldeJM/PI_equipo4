import pygame
import sys

def mostrar_controls(pantalla, reloj):
    """
    Muestra una pantalla de controles donde se alterna entre tres imágenes
    utilizando las teclas izquierda y derecha.
    """
    # Cargar las imágenes
    imagen_controles = pygame.image.load("imagenes/controles.png").convert_alpha()
    imagen_instrucciones1 = pygame.image.load("imagenes/instrucciones1.jpg").convert_alpha()
    imagen_instrucciones2 = pygame.image.load("imagenes/instrucciones2.jpg").convert_alpha()

    # Ajustar el tamaño de las imágenes al tamaño de la pantalla
    W, H = 1280, 720
    imagen_controles = pygame.transform.scale(imagen_controles, (W, H))
    imagen_instrucciones1 = pygame.transform.scale(imagen_instrucciones1, (W, H))
    imagen_instrucciones2 = pygame.transform.scale(imagen_instrucciones2, (W, H))

    # Lista de imágenes
    imagenes = [imagen_controles, imagen_instrucciones1, imagen_instrucciones2]

    # Índice para controlar la imagen que se muestra
    indice_imagen = 0  # Comienza con la primera imagen

    # Bucle principal de la pantalla de controles
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Salir al menú con ESC
                    running = False
                elif event.key == pygame.K_RIGHT:  # Avanzar a la siguiente imagen
                    indice_imagen = (indice_imagen + 1) % len(imagenes)  # Ciclar adelante
                elif event.key == pygame.K_LEFT:  # Retroceder a la imagen anterior
                    indice_imagen = (indice_imagen - 1) % len(imagenes)  # Ciclar atrás

        # Mostrar la imagen correspondiente según el índice
        pantalla.fill((0, 0, 0))  # Limpiar la pantalla con negro
        pantalla.blit(imagenes[indice_imagen], (0, 0))  # Mostrar imagen actual

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)
