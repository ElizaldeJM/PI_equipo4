import pygame
import sys
import time
import configuracion  # Importar configuracion.py

pygame.init()

# Configuración de la pantalla
W, H = 1280, 720
pantalla = pygame.display.set_mode((W, H))
pygame.display.set_caption("Créditos")

# Colores y fuente personalizada
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Cargar la fuente personalizada
fuente = pygame.font.Font("fuentes/minecraft.ttf", 48)
fuente_descripcion = pygame.font.Font("fuentes/minecraft.ttf", 36)

# Lista de créditos
creditos = [
    ("Yureni Sierra Aguilar", "Jefa de equipo y documentadora de información"),
    ("Pamela Rodríguez Gomez", "Diseñadora gráfica y compositora musical"),
    ("Juan Angelina Murillo", "Contribuidor de código y diseños gráficos"),
    ("Isabela Vidrio Camarena", "Diseñadora gráfica"),
    ("Fernando Benitez Astudillo", "Ilustraciones"),
    ("Jonathan Elizalde Moran", "Desarrollador")
]

# Función para mostrar texto centrado en pantalla
def mostrar_texto_centrado(texto, y, fuente, color=BLANCO, alpha=255):
    renderizado = fuente.render(texto, True, color)
    renderizado.set_alpha(alpha)
    rect = renderizado.get_rect(center=(W // 2, y))
    pantalla.blit(renderizado, rect)

# Función de desvanecimiento
def desvanecer_texto(nombre, descripcion):
    for alpha in range(255, 0, -15):
        pantalla.fill(NEGRO)
        mostrar_texto_centrado(nombre, H // 2 - 20, fuente, BLANCO, alpha)
        mostrar_texto_centrado(descripcion, H // 2 + 40, fuente_descripcion, BLANCO, alpha)
        pygame.display.flip()
        pygame.time.delay(50)

# Función para disminuir el volumen de la música
def disminuir_volumen():
    volumen_actual = pygame.mixer.music.get_volume()
    while volumen_actual > 0:
        volumen_actual = max(0, volumen_actual - 0.1)  # Reducir el volumen gradualmente
        pygame.mixer.music.set_volume(volumen_actual)
        pygame.time.delay(50)  # Controlar la velocidad del desvanecimiento

# Función para aumentar el volumen de la música
def aumentar_volumen():
    volumen_actual = pygame.mixer.music.get_volume()
    while volumen_actual < 1.0:  # Asumiendo que el volumen máximo es 1.0
        volumen_actual = min(1.0, volumen_actual + 0.1)  # Incrementar gradualmente
        pygame.mixer.music.set_volume(volumen_actual)
        pygame.time.delay(100)

# Función principal de créditos
def mostrar_creditos():
    disminuir_volumen()  # Disminuir el volumen de la música al iniciar los créditos

    for nombre, descripcion in creditos:
        for i in range(40):  # Espera dividida en pasos para revisar eventos
            pantalla.fill(NEGRO)
            mostrar_texto_centrado(nombre, H // 2 - 20, fuente)
            mostrar_texto_centrado(descripcion, H // 2 + 40, fuente_descripcion)
            pygame.display.flip()
            pygame.time.delay(50)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:  # Regresar a configuracion
                        aumentar_volumen()  # Restaurar volumen antes de salir
                        return

        desvanecer_texto(nombre, descripcion)

    pantalla.fill(NEGRO)
    mostrar_texto_centrado("Gracias por jugar", H // 2, fuente)
    pygame.display.flip()
    time.sleep(6)
    aumentar_volumen()  # Restaurar volumen al finalizar los créditos
