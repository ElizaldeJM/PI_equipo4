import pygame
import os

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO = 1280
ALTO = 720
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Animación con Pantalla Negra Gradual")

# Cargar todos los sprites desde la nueva ruta con el nuevo formato
sprites = []
for i in range(43):  # Nombres de los sprites: sprite_00.png, sprite_01.png, ..., sprite_38.png
    sprite_path = os.path.join("tortuga", f"sprite_{i:02d}.png")  # Formato con 2 dígitos
    sprite = pygame.image.load(sprite_path).convert_alpha()  # Cargar y mantener la transparencia
    sprites.append(sprite)

# Variables de control
reloj = pygame.time.Clock()
index_sprite = 0
velocidad_animacion = 7  # Velocidad de la animación (frames por segundo)
running = True

# Control de la "pantalla negra" gradual
opacidad_negra = 0  # Valor de opacidad inicial (0 es completamente transparente, 255 es completamente opaco)
oscurecer_velocidad = 3  # Controla cuán rápido oscurece la pantalla (ajustar según sea necesario)

# Bucle principal
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    # Limpiar la pantalla con el fondo negro
    ventana.fill((0, 0, 0))

    # Si no hemos mostrado todos los sprites, mostramos el siguiente
    if index_sprite < len(sprites):
        # Dibujar el sprite actual
        ventana.blit(sprites[index_sprite], (ANCHO // 2 - sprites[index_sprite].get_width() // 2, ALTO // 2 - sprites[index_sprite].get_height() // 2))

        # Aumentar el índice del sprite
        index_sprite += 1  # Pasamos al siguiente sprite

        # Aumentar gradualmente la opacidad de la capa negra
        if opacidad_negra < 255:
            opacidad_negra += oscurecer_velocidad  # Aumentar opacidad de la capa negra gradualmente

    # Dibujar la capa negra con la opacidad actual
    capa_negra = pygame.Surface((ANCHO, ALTO))
    capa_negra.fill((0, 0, 0))  # Llenar de negro
    capa_negra.set_alpha(opacidad_negra)  # Establecer la opacidad
    ventana.blit(capa_negra, (0, 0))  # Dibujar la capa negra sobre la ventana

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de la animación
    reloj.tick(velocidad_animacion)

    # Terminar el programa cuando la opacidad sea 255 (pantalla completamente negra)
    if opacidad_negra >= 255 and index_sprite >= len(sprites):
        running = False  # Finalizar el programa cuando la pantalla esté completamente negra y todos los sprites hayan sido mostrados

# Cerrar Pygame
pygame.quit()
