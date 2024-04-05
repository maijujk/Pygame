# Asenna Pygame-paketti koneelle:
# Kirjoita komentokehoteikkunaan seuraava komentosarja ja paina enter:
# pip3 install pygame
import pygame
from random import randint
import time
from pygame.locals import *

class AsteroidGame:
    def __init__(self, width=800, height=600):
        # Alustetaan pelimoottori ja pelin parametrit
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE | SCALED)
        pygame.display.set_caption("AsteroidGame")
        # Ladataan peliin kuvat ja fontti
        self.robo = pygame.image.load("robo2.png")
        self.asteroid = pygame.image.load("asteroid.png")
        self.font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()
        # Alustetaan muuttujat pistemäärälle ja peliajalle
        self.points = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.asteroids = []
        # Alustetaan robottiliikkeen x- ja y-suunnat
        self.robo_movement_x = 0
        self.robo_movement_y = 0

    def handle_events(self):
        # Käsitellään näppäinpainallukset ja pelin lopetus
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
           
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.robo_movement_x = -5
                elif event.key == pygame.K_RIGHT:
                    self.robo_movement_x = 5
                elif event.key == pygame.K_UP:
                    self.robo_movement_y = -5
                elif event.key == pygame.K_DOWN:
                    self.robo_movement_y = 5
                    
                # Käynnistetään uusi peli F2-näppäimestä
                elif event.key == pygame.K_F2:
                    self.points = 0
                    self.start_time = time.time()
                    # Tyhjennetään asteroidien lista uutta peliä varten
                    self.asteroids = []
                    self.run()
                    
                # Suljetaan peli ESC-näppäimestä
                elif event.key == pygame.K_ESCAPE:
                    exit()
                    
            elif event.type == pygame.KEYUP:
                # Pysäytetään liike kun näppäin vapautetaan
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.robo_movement_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.robo_movement_y = 0
                    
        if not self.game_over():
            # Kulunut aika pelin alusta
            self.elapsed_time = time.time() - self.start_time

    def draw_text(self, text, color, x, y):
        # Piirretään teksti näytölle
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def update(self):
        if not self.game_over():
            # Päivitetään pelin tila ja sijainti
            self.robo_rect.move_ip(self.robo_movement_x, self.robo_movement_y)
            # Tarkistetaan, ettei robotti mene pelialueen ulkopuolelle
            if self.robo_rect.left < 0:
                self.robo_rect.left = 0
            elif self.robo_rect.right > self.width:
                self.robo_rect.right = self.width
            if self.robo_rect.top < 0:
                self.robo_rect.top = 0
            elif self.robo_rect.bottom > self.height:
                self.robo_rect.bottom = self.height

            for asteroid in self.asteroids:
                # Liikutetaan asteroidia alaspäin
                asteroid['rect'].move_ip(0, 1)
                # Tarkistetaan törmäys robottiin
                if asteroid['rect'].colliderect(self.robo_rect):
                    # Jos törmäys tapahtuu, lisätään pisteitä
                    self.points += 1
                    asteroid['rect'].top = -randint(100, 1000)
                    asteroid['rect'].left = randint(0, self.width - self.asteroid.get_width())

    def draw(self):
        # Piirretään pelin tila näytölle
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.robo, self.robo_rect)
        for asteroid in self.asteroids:
            self.screen.blit(self.asteroid, asteroid['rect'])
        if self.game_over():
            self.draw_text("Peli loppu!", (255, 0, 0), self.width // 2 - 100, self.height // 2 - 50)
        self.draw_text("Aika: {:.2f}s".format(self.elapsed_time), (255, 0, 0), 50, 10)
        self.draw_text("Pisteet: " + str(self.points), (255, 0, 0), 200, 10)
        self.draw_text("F2 = uusi peli", (0, 255, 0), 500, 10)
        self.draw_text("Esc = sulje peli", (0, 255, 0), 650, 10)        
        pygame.display.flip()

    def run(self):
        # Asetetaan robotin alkukoordinaatit
        self.robo_rect = self.robo.get_rect()
        self.robo_rect.topleft = (self.width - self.robo.get_width(), self.height - self.robo.get_height())

        # Luodaan aluksi viisi asteroidia satunnaisiin kohtiin
        for _ in range(5):
            asteroid_rect = self.asteroid.get_rect()
            asteroid_rect.topleft = (randint(0, self.width - self.asteroid.get_width()), -randint(100, 1000))
            self.asteroids.append({'rect': asteroid_rect})

        # Peli-looppi
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            
    def game_over(self):
        # Tarkistetaan, onko peli päättynyt (eli onko jokin asteroidi saavuttanut alareunan)
        for asteroid in self.asteroids:
            if asteroid['rect'].top >= self.height:
                return True
        return False

if __name__ == '__main__':
    game = AsteroidGame()
    game.run()






