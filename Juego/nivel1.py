import sys
import pygame
import random
import pausa
import niveles
pygame.mixer.init()
sound = pygame.mixer.Sound("musica/sonido_comida.mp3")
death_sound = pygame.mixer.Sound("musica/sonidogameovervoz.mp3")
otherdeath_sound = pygame.mixer.Sound("musica/sonidosssgameover.mp3")
ancla_sound = pygame.mixer.Sound("musica/golpe_ancla.mp3")
asco_sound = pygame.mixer.Sound("musica/asco.mp3")
boton_sound= pygame.mixer.Sound("musica/sonidodeboton.mp3")
ganaste_sound = pygame.mixer.Sound("musica/musicawin.mp3")

pygame.display.set_caption("Tortuga al agua")
icono = pygame.image.load("imagenes/Run9.png")
pygame.display.set_icon(icono)

puntos = 0
win_image = pygame.image.load("imagenes/win.jpg")
an = 100
al = 100
# Colores
negro = (0, 0, 0)
blanco = (255, 255, 255)
gris = (85, 85, 85)
# Dimensiones base de la pantalla
W, H = 1280, 720
# Nivel de volumen inicial
volumen = 0.5
# ajustar volumen inicial

def ajustar_volumen(valor):
    global volumen
    volumen = max(0.0, min(1.0, volumen + valor))
    pygame.mixer.music.set_volume(volumen)
    sound.set_volume(volumen)
    death_sound.set_volume(volumen)
    otherdeath_sound.set_volume(volumen)
    ancla_sound.set_volume(volumen)
# clase jugador (tortuga)
def cambiar_color(imagen, color):
    imagen_coloreada = imagen.copy()
    color_surface = pygame.Surface(imagen.get_size(), pygame.SRCALPHA)
    color_surface.fill(color)
    imagen_coloreada.blit(color_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return imagen_coloreada



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
        self.vida_max = 100  # Vida máxima de tortuga
        self.color_cambio_tiempo = 0
        

    def update(self):
        teclas = pygame.key.get_pressed()
        self.rect.y += (teclas[pygame.K_s] -
                        teclas[pygame.K_w]) * self.velocidad
        self.rect.x += (teclas[pygame.K_d] -
                        teclas[pygame.K_a]) * self.velocidad
        self.rect.clamp_ip(pygame.Rect(0, 150, W, H - 150))
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]

        # Limitar la vida del jugador a un máximo de 100(se pasaba de 100)
        if self.vida > self.vida_max:
            self.vida = self.vida_max

# Clase Medusa(comida)


class Medusa(pygame.sprite.Sprite):
    def __init__(self, color="azul", nuevo_ancho=85, nueva_altura=75):
        super().__init__()
        # Cargar y redimensionar las imágenes
        self.images = [pygame.transform.scale(
                        pygame.image.load(f"imagenes/Medusa{color[0].upper()}{i}.png").convert_alpha(),
                        (nuevo_ancho, nueva_altura))  # Redimensionar cada imagen
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
        self.rect = self.rect.inflate(-100, -50)  # Ajustar colisión si es necesario

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
class Basura(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("imagenes/basura.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(
            0, W - self.rect.width)
        self.rect.y = random.randrange(
            150, H - self.rect.height)
        self.velocidad_x = random.choice([-1, 1]) * random.randint(1, 2)
        self.velocidad_y = random.choice([-1, 1]) * random.randint(1, 2)

    def update(self):
        # Actualizar la posición de la basura
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Eliminar si toca el borde izquierdo, superior o inferior
        if self.rect.left < 0 or self.rect.top < 150 or self.rect.bottom > H:
            self.kill()  # Elimina el sprite del grupo

        # Cambiar de dirección si toca el borde derecho
        if self.rect.right > W:
            self.velocidad_x *= -1



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
def ganaste_xd(pantalla):
    pantalla.fill(negro)
    pantalla.blit(win_image, (500, 200))
    fuente = pygame.font.Font(None, 74)
    texto_ganar = fuente.render("¡Ganaste :D!", True, (255, 255, 255))
    pantalla.blit(texto_ganar, (500, 500))
    boton_g = "!Ganaste :D¡"
    ganaste_sound.play()
    texto_ganar = fuente.render(boton_g, True, (255, 255, 255))
    boton_re = texto_ganar.get_rect(center=(640, 500))
    pygame.display.flip()
    pygame.mixer.music.pause()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_re.collidepoint(evento.pos):
                    import niveles
                    
                    
def regresar_a_niveles():
    boton_sound.play()
    pygame.quit()
    niveles.mostrar_niveles()


def game_over(pantalla):
    pygame.mixer.music.stop()
    otherdeath_sound.play()
    pantalla.fill(negro)
    #death_sound.play()

    # Cargar las imágenes de la animación
    frames = [
        pygame.image.load("imagenes/go1.png").convert_alpha(),
        pygame.image.load("imagenes/go2.png").convert_alpha(),
        pygame.image.load("imagenes/go3.png").convert_alpha(),
        pygame.image.load("imagenes/go4.png").convert_alpha(),
        pygame.image.load("imagenes/go5.png").convert_alpha(),
        pygame.image.load("imagenes/go6.png").convert_alpha(),
        pygame.image.load("imagenes/go7.png").convert_alpha(),
        pygame.image.load("imagenes/go8.png").convert_alpha(),
        pygame.image.load("imagenes/go9.png").convert_alpha(),
    ]
    frames = [pygame.transform.scale(frame, (500, 300)) for frame in frames]

    # Mostrar la animación
    for frame in frames:
        pantalla.fill(negro)
        pantalla.blit(frame, (W // 2 - frame.get_width() //
                      2, H // 2 - frame.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(100)

    # Botón de reiniciar
    boton_reiniciar = Boton("Reiniciar", 1000, 900,
                            lambda: reiniciar_nivel())
    pantalla.blit(boton_reiniciar.dibujar(), boton_reiniciar.rect.topleft)
    pygame.display.update()

    # Esperar interacción del jugador
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.rect.collidepoint(evento.pos):
                    boton_reiniciar.click()
                    return

# reiniciar el juego
def reiniciar_nivel():
    jugar_nivel()

# pausar el juego
def pausar_juego(pantalla, fondo, reloj):
    pausado = True
    font = pygame.font.SysFont(None, 74)
    texto = font.render("Juego en Pausa :p", True, (255, 255, 0))
    pantalla.blit(texto, (W // 2 - texto.get_width() // 2, H // 2 - texto.get_height() // 2))

    # Crear el botón para regresar a niveles
    font_boton = pygame.font.SysFont(None, 48)
    texto_boton = font_boton.render("Salir al Menú de Niveles", True, blanco)
    boton_rect = texto_boton.get_rect(center=(W // 2, H // 2 + 100))
    pantalla.blit(texto_boton, boton_rect.topleft)

    pygame.display.update()
    pygame.mixer.music.pause()  # Pausa la música

    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):  # Si el botón es clickeado
                    pygame.mixer.music.unpause()
                    regresar_a_niveles(pantalla, fondo, reloj)
                    return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:  # Reanudar juego
                    pausado = False
                    # reanudar la música
                    pygame.mixer.music.unpause()


def regresar_a_niveles(pantalla, fondo, reloj):
    import niveles
    print("regresando")
    niveles.mostrar_niveles(pantalla, fondo, reloj)
# jugar el nivel



def jugar_nivel():
    """Función para iniciar el nivel 1."""
    pygame.init()
    pantalla = pygame.display.set_mode((W, H))
    boton_sound.play()
    jugador_imagen = pygame.image.load('imagenes/Run1.png').convert_alpha()
    pygame.mixer.music.load("musica/musicanivel1.mp3")
    pygame.mixer.music.play(-1)
    ajustar_volumen(0)
    fondo = pygame.image.load("imagenes/fondox.png").convert()
    fondo_x = 0  # Posición inicial del fondo
    reloj = pygame.time.Clock()
    jugador = Jugador()
    sprites = pygame.sprite.Group()
    sprites.add(jugador)
    puntos = 0
    
    # Temporización para regeneración de mobs
    tiempo_medusa = pygame.time.get_ticks()
    tiempo_enemigo = pygame.time.get_ticks()
    tiempo_basura = pygame.time.get_ticks()
    intervalo_medusa = 2000  # Intervalo en milisegundos (3 segundos)
    intervalo_enemigo = 10000  # Intervalo en milisegundos (1 segundo)
    intervalo_basura = 3000

    imagenes_teclas = {
        pygame.K_w: pygame.transform.scale(pygame.image.load("imagenes/arriba.png"), (100, 100)),
        pygame.K_a: pygame.transform.scale(pygame.image.load("imagenes/izquierda.png"), (100, 100)),
        pygame.K_s: pygame.transform.scale(pygame.image.load("imagenes/abajo.png"), (100, 100)),
        pygame.K_d: pygame.transform.scale(pygame.image.load("imagenes/derecha.png"), (100, 100)),
    }
    teclas_presionadas = {key: False for key in imagenes_teclas.keys()}

    pantalla_completa = False

    while True:
        tiempo_actual = pygame.time.get_ticks()
        fondo_x -= 2
        if fondo_x <= -W:
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
            # Generar basura cada "x" segundos
            if tiempo_actual - tiempo_basura >= intervalo_basura:
                basura = Basura()
                sprites.add(basura)
                tiempo_basura = tiempo_actual  # Reiniciar el temporizador de basura

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in teclas_presionadas:
                    teclas_presionadas[evento.key] = True
                if evento.key == pygame.K_SPACE:  # Pausar juego
                    pausar_juego(pantalla, fondo, reloj)
                if evento.key == pygame.K_UP:  # Subir volumen
                    ajustar_volumen(0.1)
                if evento.key == pygame.K_DOWN:  # Bajar volumen
                    ajustar_volumen(-0.1)
                if evento.key == pygame.K_f:  # Alternar pantalla completa
                    pantalla_completa = not pantalla_completa
                    if pantalla_completa:
                        pantalla = pygame.display.set_mode(
                            (W, H), pygame.FULLSCREEN)
                    else:
                        pantalla = pygame.display.set_mode((W, H))

            if evento.type == pygame.KEYUP:
                if evento.key in teclas_presionadas:
                    teclas_presionadas[evento.key] = False

        # Actualizar jugador y sprites (medusas, enemigos y objetos de puntuacion)
        sprites.update()

        for medusa in pygame.sprite.spritecollide(jugador, sprites, False):
            if isinstance(medusa, Medusa):
                if puntos < 6:
                    puntos += 2
                sound.play()
                jugador.vida += 10  # Aumentar vida de tortuga
                medusa.kill()  # Eliminar medusa
                print(f"vida del jugador: {jugador.vida}")

        for basura in pygame.sprite.spritecollide(jugador, sprites, False):
            if isinstance(basura, Basura):
                if puntos < 6:
                    puntos += 2
                jugador.vida -= 20
                basura.kill()  # Eliminar basuras
                asco_sound.play()
                jugador.image = cambiar_color(jugador_imagen, (255, 255, 255))  # Rojo con algo de transparencia
                jugador.color_cambio_tiempo = pygame.time.get_ticks() 
        if jugador.color_cambio_tiempo and pygame.time.get_ticks() - jugador.color_cambio_tiempo > 10000:
            jugador.image = jugador_imagen
            jugador.color_cambio_tiempo = 0
        if puntos >= 6:
            ganaste_xd(pantalla)
            print("ganaste")
            # Jugador pierde xd
        if jugador.vida <= 0:
            game_over(pantalla)
        elif puntos >= 6:
            ganaste_xd(pantalla)
        pantalla.blit(fondo, (fondo_x, 0))
        pantalla.blit(fondo, (fondo_x + W, 0))
        sprites.draw(pantalla)

        texto_puntuacion = f"Puntuacion : {puntos} / 6"
        font = pygame.font.Font(None, 36)
        superficie_texto = font.render(texto_puntuacion, True, (0, 0, 0))
        pantalla.blit(superficie_texto, (640, 10))
        # Mostrar el texto de vida
        font_vida = pygame.font.SysFont(None, 36)
        texto_vida = font_vida.render(
            f"Vida: {jugador.vida} / 100", True, (0, 0, 0))
        # Mostrar vida en la parte superior izquierda
        pantalla.blit(texto_vida, (10, 10))

        # Mostrar nivel de volumen
        texto_volumen = font_vida.render(
            f"Volumen: {int(volumen * 100)}%", True, (255, 255, 255))
        pantalla.blit(texto_volumen, (W - 200, 10))
        posiciones_x = [1090, 1120, 1200, 1180]
        for idx, (key, imagen) in enumerate(imagenes_teclas.items()):
            if teclas_presionadas[key]:
                pantalla.blit(imagen, (posiciones_x[idx], 640))

        pygame.display.flip()
        reloj.tick(60)



if __name__ == "__main__":
    ajustar_volumen(1)
    jugar_nivel()
