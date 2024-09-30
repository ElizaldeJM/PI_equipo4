import sys
import pygame
import random
import pausa 
import niveles
pygame.mixer.init()
sound = pygame.mixer.Sound("Juego/sonido_comida.mp3")
death_sound = pygame.mixer.Sound("Juego/sonidogameovervoz.mp3")
otherdeath_sound = pygame.mixer.Sound("Juego/sonidosssgameover.mp3")
ancla_sound = pygame.mixer.Sound("Juego/golpe_ancla.mp3")

esc = pygame.K_ESCAPE

# Colores
negro = (0, 0, 0)
blanco = (255, 255, 255)
gris = (85, 85, 85)
# Dimensiones base de la pantalla
W, H = 1280, 720
# Nivel de volumen inicial
volumen = 0.5
# Función para ajustar el volumen
def ajustar_volumen(valor):
    global volumen
    volumen = max(0.0, min(1.0, volumen + valor))  # Limitar entre 0.0 y 1.0
    pygame.mixer.music.set_volume(volumen)
    sound.set_volume(volumen)
    death_sound.set_volume(volumen)
    otherdeath_sound.set_volume(volumen)
    ancla_sound.set_volume(volumen)
########################################################## Clase Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(
            f"imagenes/Run{i}.png").convert_alpha(), (75, 75)) for i in list(range(1, 10)) + list(range(8, 1, -1))]
        for image in self.images:
            image.set_colorkey(blanco)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(0, H // 2))
        self.velocidad = 5
        self.current_image = 0
        self.animation_counter = 0
        self.animation_speed = 10
        self.vida = 100
        self.vida_max = 100  # Vida máxima del jugador

    def update(self):
        teclas = pygame.key.get_pressed()
        self.rect.y += (teclas[pygame.K_s] - teclas[pygame.K_w]) * self.velocidad
        self.rect.x += (teclas[pygame.K_d] - teclas[pygame.K_a]) * self.velocidad
        self.rect.clamp_ip(pygame.Rect(0, 150, W, H - 150))
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]

        # Limitar la vida del jugador a un máximo de 100
        if self.vida > self.vida_max:
            self.vida = self.vida_max

################################################## Clase Medusa
class Medusa(pygame.sprite.Sprite):
    def __init__(self, color="azul"):
        super().__init__()
        self.images = [pygame.image.load(f"imagenes/Medusa{color[0].upper()}{i}.png").convert_alpha()
                       for i in list(range(1, 7)) + list(range(5, 1, -1))]
        for image in self.images:
            image.set_colorkey(gris)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, W - self.rect.width)
        self.rect.y = random.randrange(150, H - self.rect.height)
        self.velocidad_x = random.choice([-1, 1]) * random.randint(1, 3)
        self.velocidad_y = random.choice([-1, 1]) * random.randint(1, 3)
        self.current_image = 0
        self.animation_counter = 0
        self.animation_speed = 18

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        if self.rect.left < 0 or self.rect.right > W:
            self.velocidad_x *= -1
        if self.rect.top < 150 or self.rect.bottom > H:
            self.velocidad_y *= -1
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]

##############################################################Clase Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("imagenes/ancla1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = W  # Se genera en el extremo derecho de la pantalla
        self.rect.y = random.randint(150, H - self.rect.height)
        self.velocidad_x = -random.randint(4, 6)

    def update(self):
        self.rect.x += self.velocidad_x
        if self.rect.right < 0:
            self.kill()


class Basura(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cargar la imagen de la basura y convertirla para su uso
        self.image = pygame.image.load("imagenes/basura.png").convert_alpha()  
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensionar a 50x50
        self.rect = self.image.get_rect()  # Obtener el rectángulo de la imagen
        self.rect.x = random.randrange(0, W - self.rect.width)  # Posición X aleatoria
        self.rect.y = random.randrange(150, H - self.rect.height)  # Posición Y aleatoria
        self.velocidad_x = random.choice([-1, 1]) * random.randint(1, 2)  # Velocidad horizontal aleatoria
        self.velocidad_y = random.choice([-1, 1]) * random.randint(1, 2)  # Velocidad vertical aleatoria

    def update(self):
        # Actualizar la posición de la basura
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        # Cambiar de dirección si sale de la pantalla
        if self.rect.left < 0 or self.rect.right > W:
            self.velocidad_x *= -1
        if self.rect.top < 150 or self.rect.bottom > H:
            self.velocidad_y *= -1


# Clase Botón
class Boton:
    def __init__(self, texto, x, y, accion):
        self.font = pygame.font.SysFont(None, 48)
        self.texto = texto
        self.rect = None
        self.accion = accion
        self.dibujar()

    def dibujar(self):
        renderizado = self.font.render(self.texto, True, (255, 255, 255))
        self.rect = renderizado.get_rect(center=(W // 2, H // 2 + 50))
        return renderizado

    def click(self):
        if self.accion:
            self.accion()

# Función para mostrar Game Over
def game_over(pantalla):
    pygame.mixer.music.stop()
    otherdeath_sound.play()
    pantalla.fill(negro)
    death_sound.play()
    font = pygame.font.SysFont(None, 74)
    texto = font.render("Juego Terminado", True, (255, 0, 0))
    pantalla.blit(texto, (W // 2 - texto.get_width() // 2, H // 2 - texto.get_height() // 2))
    boton_reiniciar = Boton("Reiniciar", W // 2, H // 2 + 50, lambda: reiniciar_nivel())
    pantalla.blit(boton_reiniciar.dibujar(), boton_reiniciar.rect.topleft)
    pygame.display.update()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.rect.collidepoint(evento.pos):
                    boton_reiniciar.click()
                    return

# Función para reiniciar el juego
def reiniciar_nivel():
    jugar_nivel()

# Función para pausar el juego
def pausar_juego(pantalla):
    pausado = True
    font = pygame.font.SysFont(None, 74)
    texto = font.render("Juego en Pausa", True, (255, 255, 0))
    pantalla.blit(texto, (W // 2 - texto.get_width() // 2, H // 2 - texto.get_height() // 2))
    pygame.display.update()
    
    # Pausar la música
    pygame.mixer.music.pause()
    
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:  # Reanudar juego
                    pausado = False
                    # Reanudar la música
                    pygame.mixer.music.unpause()

def regresar_a_niveles():
    import niveles
    print ("regresando")
    niveles.mostrar_niveles()
# Función para jugar el nivel
def jugar_nivel():
    """Función para iniciar el nivel 1."""
    pygame.init()
    pantalla = pygame.display.set_mode((W, H))
    pygame.mixer.music.load("Juego/musicanivel1.mp3")
    pygame.mixer.music.play(-1)
    ajustar_volumen(0)  # Restablecer el volumen a su valor inicial
    fondo = pygame.image.load("imagenes/fondox.png").convert()
    fondo_x = 0  # Posición inicial del fondo
    reloj = pygame.time.Clock()
    jugador = Jugador()
    sprites = pygame.sprite.Group()
    sprites.add(jugador)

    # Temporización para regeneración de entidades
    tiempo_medusa = pygame.time.get_ticks()
    tiempo_enemigo = pygame.time.get_ticks()
    intervalo_medusa = 2000  # Intervalo en milisegundos (3 segundos)
    intervalo_enemigo = 1000  # Intervalo en milisegundos (1 segundo)

    # Aquí están las imágenes para mostrar (arriba, abajo, izquierda, derecha)
    imagenes_teclas = {
        pygame.K_w: pygame.transform.scale(pygame.image.load("imagenes/arriba.png"), (100, 100)),
        pygame.K_a: pygame.transform.scale(pygame.image.load("imagenes/izquierda.png"), (100, 100)),
        pygame.K_s: pygame.transform.scale(pygame.image.load("imagenes/abajo.png"), (100, 100)),
        pygame.K_d: pygame.transform.scale(pygame.image.load("imagenes/derecha.png"), (100, 100)),
    }
    teclas_presionadas = {key: False for key in imagenes_teclas.keys()}

    pantalla_completa = False  # Variable para controlar el modo de pantalla completa

    while True:
        tiempo_actual = pygame.time.get_ticks()

        # Mover el fondo de derecha a izquierda
        fondo_x -= 2  # Cambia este valor para ajustar la velocidad de movimiento
        if fondo_x <= -W:  # Reiniciar la posición del fondo
            fondo_x = 0

        # Generar medusas cada "x" segundos
        if tiempo_actual - tiempo_medusa >= intervalo_medusa:
            color = random.choice(["azul", "verde", "rojo"])
            medusa = Medusa(color=color)
            sprites.add(medusa)
            tiempo_medusa = tiempo_actual  # Reiniciar el temporizador de medusas

        # Generar enemigos cada "x" segundos
        if tiempo_actual - tiempo_enemigo >= intervalo_enemigo:
            enemigo = Enemigo()
            sprites.add(enemigo)
            tiempo_enemigo = tiempo_actual  # Reiniciar el temporizador de enemigos

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in teclas_presionadas:
                    teclas_presionadas[evento.key] = True
                if evento.key == pygame.K_p:  # Pausar juego
                    pausar_juego(pantalla)
                if evento.key == pygame.K_UP:  # Subir volumen
                    ajustar_volumen(0.1)
                if evento.key == pygame.K_DOWN:  # Bajar volumen
                    ajustar_volumen(-0.1)
                if evento.key == pygame.K_f:  # Alternar pantalla completa
                    pantalla_completa = not pantalla_completa
                    if pantalla_completa:
                        pantalla = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
                    else:
                        pantalla = pygame.display.set_mode((W, H))
                    if evento.key == K_ESCAPE:
                        regresar_a_niveles()

            if evento.type == pygame.KEYUP:
                if evento.key in teclas_presionadas:
                    teclas_presionadas[evento.key] = False

        # Actualizar jugador y sprites (medusas y enemigos)
        sprites.update()

        # Verificar colisiones
        for medusa in pygame.sprite.spritecollide(jugador, sprites, False):
            if isinstance(medusa, Medusa):
                sound.play()
                jugador.vida += 10  # Aumentar vida del jugador
                medusa.kill()  # Eliminar medusa
                print(f"vida del jugador: {jugador.vida}")

        for enemigo in pygame.sprite.spritecollide(jugador, sprites, False):
            if isinstance(enemigo, Enemigo):
                jugador.vida -= 20  # Disminuir vida del jugador
                enemigo.kill()  # Eliminar enemigo
                print(f"vida del jugador: {jugador.vida}")
                ancla_sound.play()

        # Jugador pierde xd
        if jugador.vida <= 0:
            game_over(pantalla)

        # Dibujar en pantalla
        pantalla.blit(fondo, (fondo_x, 0))  # Dibujar el fondo en la posición actual
        pantalla.blit(fondo, (fondo_x + W, 0))  # Dibujar otra instancia del fondo para crear el efecto de movimiento
        sprites.draw(pantalla)

        # Mostrar el texto de vida
        font_vida = pygame.font.SysFont(None, 36)
        texto_vida = font_vida.render(f"Vida: {jugador.vida}", True, (255, 0, 0))
        pantalla.blit(texto_vida, (10, 10))  # Mostrar vida en la parte superior izquierda

        # Mostrar nivel de volumen
        texto_volumen = font_vida.render(f"Volumen: {int(volumen * 100)}%", True, (255, 255, 255))
        pantalla.blit(texto_volumen, (W - 200, 10))  # Mostrar nivel de volumen en la esquina superior derecha

        # Mostrar imágenes en la parte inferior derecha
        posiciones_x = [1090, 1120, 1200, 1180]  # Posiciones para imágenes de teclas
        for idx, (key, imagen) in enumerate(imagenes_teclas.items()):
            if teclas_presionadas[key]:
                pantalla.blit(imagen, (posiciones_x[idx], 640))  # Separación de 50 píxeles en X

        # Actualizar el display
        pygame.display.flip()
        reloj.tick(60)

# Llamar a la función para jugar el nivel
if __name__ == "__main__":
    ajustar_volumen(1)  # Establecer el volumen inicial
    jugar_nivel()
