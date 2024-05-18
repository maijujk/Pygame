import pygame
import time
from pygame.locals import *

class Robottuseikkailu:
    def __init__(self):
        pygame.init()
        
        # Lataa pelin kuvat
        self.lataa_kuvat()
        
        # Alusta uusi peli
        self.uusi_peli()
   
        # Määritä pelin mitat
        self.korkeus = len(self.kartta)
        self.leveys = len(self.kartta[0])
        self.skaala = self.kuvat[0].get_width()

        # Alusta näyttö
        nayton_korkeus = self.skaala * self.korkeus
        nayton_leveys = self.skaala * self.leveys
        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus + self.skaala), RESIZABLE | SCALED)
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.fontti2 = pygame.font.SysFont("Arial", 30)

        pygame.display.set_caption("Robottuseikkailu") # Pelin nimi
        
        # Alusta pelin muuttujat
        self.nimi = ""
        self.kysely = True
        self.tulokset = []
        self.peli_kaynnissa = False
        self.miinus_robot = False

        self.robot = 3
        self.aika_kulunut = 0
        self.portaalin_kulma = 0
        
        self.input = pygame.Rect(nayton_leveys // 2 - 100, nayton_korkeus // 2 - 15, 225, 40)
        
        self.anim = pygame.time.Clock()

        # Käynnistä pelisilmukka
        self.silmukka()

    def lataa_kuvat(self):
        # Lataa pelin kuvat
        self.kuvat = []
        for nimi in ["lattia", "seina", "energia", "monsteri", "robo", "portaali", "loppu"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))
                
    def uusi_peli(self):    
        # Alusta uusi peli kartan ja muuttujien kanssa
        self.kartta = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 0, 2, 1, 1, 1, 0, 1, 1, 0, 1, 0, 2, 2, 0, 2, 0, 1, 2, 2, 2, 1],
                       [1, 2, 0, 1, 0, 2, 0, 1, 1, 0, 1, 0, 2, 0, 1, 1, 0, 2, 2, 0, 2, 1],
                       [1, 1, 2, 0, 2, 0, 0, 2, 1, 0, 1, 0, 1, 0, 1, 1, 2, 2, 0, 1, 0, 1],
                       [1, 2, 0, 1, 0, 0, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 3, 1, 1, 0, 1],
                       [1, 1, 2, 1, 0, 2, 0, 3, 1, 0, 2, 0, 1, 0, 2, 0, 3, 0, 0, 0, 0, 1],
                       [1, 2, 0, 0, 2, 0, 0, 2, 1, 0, 1, 0, 1, 2, 0, 2, 1, 2, 0, 1, 3, 1],
                       [1, 1, 0, 1, 0, 2, 1, 1, 1, 0, 2, 0, 1, 2, 0, 2, 1, 2, 1, 1, 0, 1],
                       [1, 2, 0, 1, 0, 0, 1, 2, 1, 0, 1, 0, 1, 0, 3, 1, 2, 0, 2, 0, 0, 1],
                       [1, 0, 0, 1, 0, 2, 0, 2, 1, 0, 2, 0, 1, 2, 0, 1, 2, 1, 0, 1, 1, 1],
                       [1, 4, 0, 2, 3, 0, 2, 0, 1, 3, 1, 0, 1, 0, 0, 1, 1, 0, 2, 0, 5, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        
        self.lataus = 0
        self.alkuaika = time.time()  # Tallenna pelin alkamisaika
        
        # Tarkista, onko F2-näppäin painettu
        keys = pygame.key.get_pressed()
        if keys[pygame.K_F2]:
            self.robot = 3
            self.aika = 0
            self.aika = time.time() - self.alkuaika 
            self.nimi = ""
            self.kysely = True
            self.miinus_robot = False  # Nollaa muuttuja
            
    def silmukka(self):
        # Pelin aloituskuva
        robo = pygame.image.load("robo2.png")
        
        x = 0
        y = 0
        nopeus_x = 2
        nopeus_y = 2
        max_pituus = 15
        
        while not self.peli_kaynnissa:            
            self.naytto.fill((0, 0, 0))

            # Näytä aloitusviesti
            teksti = self.fontti2.render("Tervetuloa Robottiseikkailuun!", True, (0, 255, 0))                
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2 
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2 - 200
            self.naytto.blit(teksti, (teksti_x, teksti_y))
            
            teksti2 = self.fontti2.render("Lataa robottisi täyteen energiaa ja ohjaa se turvallisesti portaaliin.", True, (0, 255, 0))
            teksti2_x = self.skaala * self.leveys / 2 - teksti2.get_width() / 2
            teksti2_y = teksti_y + teksti.get_height() + 10
            self.naytto.blit(teksti2, (teksti2_x, teksti2_y))
            
            teksti3 = self.fontti2.render("Mutta ole varovainen, sillä matkallesi saattaa osua monstereita!", True, (0, 255, 0))
            teksti3_x = self.skaala * self.leveys / 2 - teksti3.get_width() / 2
            teksti3_y = teksti2_y + teksti2.get_height() + 10
            self.naytto.blit(teksti3, (teksti3_x, teksti3_y))
            
            teksti4 = self.fontti2.render("Anna nimimerkkisi ja paina Enter", True, (0, 255, 0))     
            teksti4_x = self.skaala * self.leveys / 2 - teksti4.get_width() / 2
            teksti4_y = teksti3_y + teksti3.get_height() + 25
            self.naytto.blit(teksti4, (teksti4_x, teksti4_y))
            
            pygame.draw.rect(self.naytto, (0, 0, 0), self.input)
            nimimerkki = self.fontti2.render(self.nimi, True, (0, 255, 0))
            self.naytto.blit(nimimerkki, (self.input.x + 10, self.input.y))
            pygame.draw.rect(self.naytto, (0, 255, 0), self.input, 3)
            
            x += nopeus_x
            y += nopeus_y
        
            if x == 0 or x + robo.get_width() == self.skaala * self.leveys:
                nopeus_x = -nopeus_x
            if y == 0 or y + robo.get_height() == self.skaala * self.korkeus:
                nopeus_y = -nopeus_y
        
            self.naytto.blit(robo, (x, y))

            pygame.display.flip()
        
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    # Aseta pelaajan nimimerkki ja käynnistä peli
                    if tapahtuma.key == pygame.K_RETURN: # Enter
                        self.kysely = False
                        self.tulokset.append(self.nimi)  # Lisää pelaajan nimimerkki listaan
                        self.peli_kaynnissa = True
                    elif tapahtuma.key == pygame.K_BACKSPACE: 
                        self.nimi = self.nimi[:-1]
                    else:
                        # Nimimerkin max pituus 15 merkkiä
                        if len(self.nimi) < max_pituus:
                            self.nimi += tapahtuma.unicode 
                    
                if tapahtuma.type == pygame.QUIT:
                    exit()
                    
        # Pelisilmukka
        while self.peli_kaynnissa:
            sek = self.anim.tick()
            self.aika_kulunut += sek
            # Käsittele näppäimistön painalluksia pelin aikana
            self.nappaimet()
            # Hidasta monsteri animaatioita
            if self.aika_kulunut > 700:
                if not self.peli_lapi() and not self.peli_loppu():
                    self.monsteri_anim()
                self.aika_kulunut = 0
            self.piirra_naytto()

    def nappaimet(self):
        # Käsittele pelaajan näppäimistötoiminnot
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.liiku(0, -1)
                if tapahtuma.key == pygame.K_RIGHT:
                    self.liiku(0, 1)
                if tapahtuma.key == pygame.K_UP:
                    self.liiku(-1, 0)
                if tapahtuma.key == pygame.K_DOWN:
                    self.liiku(1, 0)
                    
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
            if tapahtuma.type == pygame.QUIT:
                exit()

        # Päivitä kulunut aika portaaliin pääsystä
        if self.robot > 0 and not self.peli_lapi():
            self.aika = time.time() - self.alkuaika    
            
    def liiku(self, liike_y, liike_x):
        if self.peli_loppu() or self.peli_lapi():
            return
        if self.etsi_robo() is not None: 
            # Liikuta robottia kartalla
            robon_vanha_y, robon_vanha_x = self.etsi_robo()
            
            # Tarkista uusi sijainti
            robon_uusi_y = robon_vanha_y + liike_y
            robon_uusi_x = robon_vanha_x + liike_x 

            if self.kartta[robon_uusi_y][robon_uusi_x] == 1:
                return

            # Tarkista, onko energia saavutettu
            if self.kartta[robon_uusi_y][robon_uusi_x] == 2:
                # Poista energia kartalta
                self.kartta[robon_uusi_y][robon_uusi_x] -= 2
                self.lataus += 2
            
            # Tarkista, onko monsteri reitillä
            if self.kartta[robon_uusi_y][robon_uusi_x] == 3:
                # Jos, muuta robotti Noneksi
                self.etsi_robo() == None
                return self.monsteri_anim()

            # Tarkista, onko portaali saavutettu
            if self.kartta[robon_uusi_y][robon_uusi_x] == 5:
                if self.lataus != 100:
                    return
                # Poista portaali ja lisää loppu kuva
                self.kartta[robon_uusi_y][robon_uusi_x] += 1

                if self.kartta[robon_uusi_y][robon_uusi_x] == 6:
                    # Poista robotti kartalta
                    self.kartta[robon_vanha_y][robon_vanha_x] -= 4
                return self.peli_lapi()

            self.kartta[robon_vanha_y][robon_vanha_x] -= 4
            self.kartta[robon_uusi_y][robon_uusi_x] += 4

            # Päivitä näyttö
            pygame.display.flip()

    def monsteri_anim(self):
        monsteri_koordinaatit = self.etsi_monsteri()  # Etsi kaikki monsterit kartalta
        robo_sijainti = self.etsi_robo() # Etsi robotti kartalta

        for monsteri_x, monsteri_y in monsteri_koordinaatit:
            if robo_sijainti is not None and monsteri_koordinaatit:

                # Hae kartan alueet, jossa monsteri saa liikkua
                alat = [(y, x) for y in range(self.korkeus) for x in range(self.leveys) if self.kartta[y][x] in [0, 4]]  

                # Jos monsteri on jo alueella, ei tarvitse etsiä suuntaa
                if (monsteri_y, monsteri_x) in alat:
                    continue

                # Etsi lähin alue
                lahimmalle = min(alat, key=lambda pos: abs(pos[0] - monsteri_y) + abs(pos[1] - monsteri_x))

                # Suunta yhden askeleen liikkumiseen
                suunta_y = 0 if lahimmalle[0] == monsteri_y else 1 if lahimmalle[0] > monsteri_y else -1
                suunta_x = 0 if lahimmalle[1] == monsteri_x else 1 if lahimmalle[1] > monsteri_x else -1

                # Liiku 5 askelta eteen- ja taaksepäin
                for _ in range(4):
                    uusi_y = monsteri_y + suunta_y
                    uusi_x = monsteri_x + suunta_x

                    # Varmista, miten monsteri ei syö kartalla
                    if 0 <= uusi_y < self.korkeus and 0 <= uusi_x < self.leveys and self.kartta[uusi_y][uusi_x] not in [1, 2, 3, 5]:
                        self.kartta[monsteri_y][monsteri_x] = 0 
                        self.kartta[uusi_y][uusi_x] = 3   # aseta monsteri uuteen sijaintiin                            
                        self.piirra_naytto()
                        monsteri_y, monsteri_x = uusi_y, uusi_x
                    
            else:
                if not self.peli_loppu():
                    self.robot -= 1
                    self.miinus_robot = True
                    if self.robot != 0:
                        # Palaa alkusijaintiin
                        return self.uusi_peli()

    def etsi_robo(self):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [4]:
                    return (y, x)
                
    def etsi_monsteri(self):
        monsteri_koordinaatit = []
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] == 3:  # Tarkista, onko monsteri
                    monsteri_koordinaatit.append((x, y))
        return monsteri_koordinaatit

    def piirra_naytto(self):
        self.naytto.fill((0, 0, 0)) 

        for y in range(self.korkeus):
            for x in range(self.leveys):
                ruutu = self.kartta[y][x]
                if not self.peli_loppu():
                    self.portaalin_kulma += 0.05
                if ruutu != 5:
                    self.naytto.blit(self.kuvat[ruutu], (x * self.skaala, y * self.skaala))
                else:
                    # Pyöritä portaalia
                    tausta = pygame.image.load("lattia.png")
                    kuva = pygame.transform.rotate(self.kuvat[ruutu], self.portaalin_kulma)
                                                    
                    # Piirrä kuva
                    self.naytto.blit(tausta, (x * self.skaala, y * self.skaala))
                    self.naytto.blit(kuva, (x * self.skaala, y * self.skaala))

        if self.peli_lapi():
            pelaaja_aika = f"{round(self.aika, 2)}"
            if pelaaja_aika not in self.tulokset:
                self.tulokset.append(pelaaja_aika)

            teksti = self.fontti2.render(f"Onnea, {self.tulokset[0]} läpäisit pelin!", True, (0, 255, 0))
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2 - 100
            marginaali = 50
            
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x - marginaali, teksti_y - 30, teksti.get_width() + 2 * marginaali, teksti.get_height() + marginaali))
            self.naytto.blit(teksti, (teksti_x, teksti_y))

            teksti2 = self.fontti.render("Tulokset:", True, (0, 255, 0))
            teksti2_x = self.skaala * self.leveys / 2 - teksti2.get_width() / 2
            teksti_y += teksti2.get_height() + 10
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x - marginaali, teksti_y, teksti.get_width() + 2 * marginaali, teksti.get_height() + marginaali))
            self.naytto.blit(teksti2, (teksti2_x, teksti_y))

            # Tulosta tulokset yksi kerrallaan allekkain
            for i, aika_jono in enumerate(self.tulokset[1:], start=1):  # [:0:-1]
                peli_aika = self.fontti.render(f"{i}. Peli aika: {aika_jono}s", True, (0, 255, 0))
                peli_aika_x = self.skaala * self.leveys / 2 - peli_aika.get_width() / 2
                teksti_y += peli_aika.get_height()  # Siirry seuraavan ajan koordinaatteihin
                pygame.draw.rect(self.naytto, (0, 0, 0),
                                (teksti_x - marginaali, teksti_y, teksti.get_width() + 2 * marginaali, teksti.get_height() + marginaali))
                self.naytto.blit(peli_aika, (peli_aika_x, teksti_y))

        elif self.peli_loppu():
            teksti = self.fontti2.render(f"Robottisi tuhoutui, {self.tulokset[0]}", True, (0, 255, 0))
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2 - 100
            marginaali = 25
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x - marginaali, teksti_y - marginaali, teksti.get_width() + 2 * marginaali, teksti.get_height() + 2 * marginaali))
            self.naytto.blit(teksti, (teksti_x, teksti_y))

            teksti2 = self.fontti2.render(f"Peli loppu!", True, (0, 255, 0))
            teksti2_x = self.skaala * self.leveys / 2 - teksti2.get_width() / 2
            teksti2_y = teksti_y + teksti.get_height() + 10
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x - marginaali, teksti2_y, teksti.get_width() + 2 * marginaali, teksti.get_height() + marginaali))
            self.naytto.blit(teksti2, (teksti2_x, teksti2_y))

        elif self.miinus_robot:
            if not hasattr(self, 'nayta_teksti') or self.nayta_teksti is None:
                self.nayta_teksti = pygame.time.get_ticks()
            teksti = self.fontti2.render(f"Robotteja jäljellä {self.robot}", True, (0, 255, 0))
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2 - 100
            marginaali = 10
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x - marginaali, teksti_y - marginaali, teksti.get_width() + 2 * marginaali, teksti.get_height() + 2 * marginaali))

            self.naytto.blit(teksti, (teksti_x, teksti_y))
            nykyinen_aika = pygame.time.get_ticks()
            if nykyinen_aika - self.nayta_teksti > 2000:  # 2000 millisekuntia = 2 sekuntia, teksti näytöllä
                self.miinus_robot = False
                self.nayta_teksti = None  # Nollaa aika
                
        teksti = f"Aika: {round(self.aika, 2)}s"
        teksti = self.fontti.render(teksti, True, (0, 255, 0))
        pygame.draw.rect(self.naytto, (0, 0, 0), (40, 10, teksti.get_width() + 330, teksti.get_height()))
        self.naytto.blit(teksti, (50, 10))
            
        teksti = f"Robotit: {self.robot}"
        teksti = self.fontti.render(teksti, True, (0, 255, 0))
        self.naytto.blit(teksti, (200, 10))

        teksti = f"Energia: {self.lataus}%"
        teksti = self.fontti.render(teksti, True, (0, 255, 0))
        self.naytto.blit(teksti, (350, 10))

        teksti = self.fontti.render("F2 = uusi peli", True, (0, 255, 0))
        # pygame.draw.rect(self.naytto, (0, 0, 0), (350, 610, teksti.get_width(), teksti.get_height()))
        self.naytto.blit(teksti, (350, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("Esc = sulje peli", True, (0, 255, 0))
        self.naytto.blit(teksti, (550, self.korkeus * self.skaala + 10))

        # Päivitä näyttö
        pygame.display.flip()

    def peli_loppu(self):
        if self.robot > 0:
            return False
        return True

    def peli_lapi(self):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [2, 5]:
                    return False
        return True
    
if __name__ == "__main__":
    Robottuseikkailu()