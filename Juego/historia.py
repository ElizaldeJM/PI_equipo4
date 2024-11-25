import pygame
import sys
import configuracion  # Importar configuracion.py para volver a la pantalla de configuración

def mostrar_historia(pantalla):
    """
    Muestra la historia con navegación entre imágenes.
    """
    # Cargar las imágenes de la historia
    imagenes_historia = [
        pygame.image.load("historia/historia1.jpg").convert(),
        pygame.image.load("historia/historia2.jpg").convert(),
        pygame.image.load("historia/historia3.jpg").convert(),
        pygame.image.load("historia/historia4.jpg").convert(),
        pygame.image.load("historia/historia5.jpg").convert(),
        pygame.image.load("historia/historia6.jpg").convert(),
        pygame.image.load("historia/historia7.jpg").convert()
    ]
    imagenes_historia = [pygame.transform.scale(img, pantalla.get_size()) for img in imagenes_historia]

    # Índice inicial
    indice_actual = 0

    # Reloj para control del tiempo
    reloj = pygame.time.Clock()

    # Disminuir el volumen de la música al ingresar a la pantalla de historia
    pygame.mixer.music.set_volume(0.1)  # Ajustar el volumen a un 20%

    mostrando_historia = True
    while mostrando_historia:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:  # Avanzar a la siguiente imagen
                    indice_actual = (indice_actual + 1) % len(imagenes_historia)
                elif evento.key == pygame.K_LEFT:  # Regresar a la imagen anterior
                    indice_actual = (indice_actual - 1) % len(imagenes_historia)
                elif evento.key == pygame.K_ESCAPE:  # Volver a configuración
                    configuracion.mostrar_configuracion(pantalla, reloj)
                    mostrando_historia = False

        # Dibujar la imagen actual en la pantalla
        pantalla.blit(imagenes_historia[indice_actual], (0, 0))
        pygame.display.flip()
        reloj.tick(60)

    # Cuando se salga de la pantalla de historia, restaurar el volumen a su nivel anterior
    pygame.mixer.music.set_volume(0.5)  # Restaurar volumen al 50% (puedes ajustarlo según lo necesites)

