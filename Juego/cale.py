import pygame

# Inicializa Pygame
pygame.init()

# Carga la imagen
imagen = pygame.image.load('imagenes/Run9.png')

# Crea una máscara de color (por ejemplo, rojo)
rojo = pygame.Surface(imagen.get_size())
rojo.fill((255, 0, 0))

# Aplica la máscara de color a la imagen
imagen_coloreada = imagen.copy()
imagen_coloreada.blit(rojo, (0, 0), special_flags=pygame.BLEND_MULT)

# Configura la pantalla
pantalla = pygame.display.set_mode((800, 600))
pantalla.blit(imagen_coloreada, (100, 100))
pygame.display.flip()

# Mantén la ventana abierta
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()