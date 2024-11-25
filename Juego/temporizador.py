import pygame

# Función para iniciar el temporizador
def iniciar_temporizador():
    return pygame.time.get_ticks()

# Función para obtener el tiempo transcurrido
def tiempo_transcurrido(tiempo_inicio):
    return (pygame.time.get_ticks() - tiempo_inicio) / 1000 # Devuelve el tiempo en segundos

# Función para mostrar el temporizador en la pantalla
def mostrar_temporizador(pantalla, tiempo_transcurrido):
    font = pygame.font.SysFont(None, 74)
    texto_temporizador = font.render(f"Tiempo: {int(tiempo_transcurrido)}s", True, (255, 255, 255))
    pantalla.blit(texto_temporizador, (20, 20))
