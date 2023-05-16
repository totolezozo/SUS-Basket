import pygame
import sys
import time
# sus


class Joueur:
    # masque 0 and 1: a l'arret \\ masque 2 : avance vers la droite 1 \\ masque 3 : avance vers la droite 2
    # masque 4 : avance vers la gauche 1 \\ masque 5 : avance vers la gauche 2 \\ masque 6 : saute
    def __init__(self, pos_x, pos_y, masque, number, list_key, point=0):
        self.keys = list_key
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.objet = None
        self.possession = False
        self.masque_on = 0
        self.number = number
        self.masque = masque
        for i in range(len(masque)):
            self.masque[i] = pygame.image.load(masque[i]).convert_alpha()
            if i == 0 :
                self.masque[ i ]=pygame.transform.scale(self.masque[ i ], (150, 200))
            else :
                self.masque[i] = pygame.transform.scale(self.masque[i], (100, 200))
        self.saute = False
        self.jump_state = -12
        self.point = point

    def deplacement(self, jeu):
        keys = pygame.key.get_pressed()
        # deplacement joueur
        if keys[self.keys[3]] and self.pos_x < 1200:
            self.pos_x += 5
            # ajustement des masques
            if self.pos_x % 25 == 0:
                if self.masque_on == 0:
                    self.masque_on = 1
                elif self.masque_on == 1:
                    self.masque_on = 2
                elif self.masque_on == 2:
                    self.masque_on = 3
                elif self.masque_on == 3:
                    self.masque_on = 4
                else :
                    self.masque_on = 1
        if keys[self.keys[2]] and self.pos_x > 100:
            self.pos_x -= 5
            # ajustement des masques
            if self.pos_x % 25 == 0:
                if self.masque_on == 0:
                    self.masque_on = 1
                elif self.masque_on == 1:
                    self.masque_on = 2
                elif self.masque_on == 2:
                    self.masque_on = 3
                elif self.masque_on == 3:
                    self.masque_on = 4
                else :
                    self.masque_on = 1
        if keys[self.keys[0]]:
            self.saute = True
        if self.saute:
            self.jump_state += 1
            self.pos_y = self.pos_y + ((1 / 30) * (self.jump_state ** 3))
            if self.jump_state == 11:
                self.saute = False
                self.jump_state = -12

        if not keys[self.keys[0]] and keys[self.keys[0]] == keys[self.keys[3]] == keys[self.keys[2]]:
            self.masque_on = 0
        if self.objet.colliderect(jeu.ballon) and jeu.possession == 0:
            self.possession = True
            jeu.possession = self.number
            jeu.b_pos_x = 500
            jeu.x = 5

        if self.possession:
            if self.saute:
                jeu.b_pos_x = self.pos_y + 100
            elif jeu.b_pos_x < 500:
                jeu.b_pos_x = 500
                jeu.x = 5
            jeu.b_pos_y=self.pos_x + 50


class Game:
    def __init__(self, player1, player2, board, ball, surface):
        # position de depart de la balle
        self.b_pos_x = 200
        self.b_pos_y = 700
        self.x = 0
        self.y = 0
        self.ballon=None
        self.possession = 0
        self.joueur1 = player1
        self.joueur2 = player2
        self.terrain = board
        self.img_ballon = ball
        self.surf = surface
        self.panierdroit = None
        self.paniergauche = None
        self.panierdroit_comptage = None
        self.paniergauche_comptage = None
    def printbox(self):
        self.paniergauche = pygame.draw.rect(self.surf, "red", ((200, 295), (10, 10)), 1)
        self.paniergauche_comptage = pygame.draw.rect(self.surf, "red", ((120, 320), (30, 10)), 1)
        self.panierdroit = pygame.draw.rect(self.surf, "red", ((1190, 295), (10, 10)), 1)
        self.panierdroit_comptage = pygame.draw.rect(self.surf, "red", ((1260, 320), (30, 10)), 1)
        self.ballon = pygame.draw.rect(self.surf, "red", ((self.b_pos_y - 30, self.b_pos_x - 16), (60, 60)), 1)
        self.joueur1.objet = pygame.draw.rect(self.surf, "red",
                                            ((self.joueur1.pos_x + 20, self.joueur1.pos_y + 20), (60, 160)), 1)
        self.joueur2.objet = pygame.draw.rect(self.surf, "red",
                                            ((self.joueur2.pos_x + 20, self.joueur2.pos_y + 20), (60, 160)), 1)
    def print_joueur(self):
        self.surf.blit(self.joueur1.masque[ self.joueur1.masque_on ],
                       (self.joueur1.pos_x, self.joueur1.pos_y))
        self.surf.blit(self.joueur2.masque[ self.joueur2.masque_on ],
                       (self.joueur2.pos_x, self.joueur2.pos_y))
        self.surf.blit(self.img_ballon, (self.b_pos_y - 30, self.b_pos_x - 16))

        label = myfont.render(str(self.joueur2.point), 10, (255, 0, 0))
        self.surf.blit(label, (610, 25))

        label = myfont.render(str(self.joueur1.point), 10, (255, 0, 0))
        self.surf.blit(label, (760, 25))

        label = sus.render("SUS", 5, (255, 0, 0))
        self.surf.blit(label, (665, 30))
    def rebond(self, friction_force=0.2):

        # This function acts on the ball.
        # The floor is at 560 pixels vertically from the top of the page.
        # The ball cannot go under 50 pixels horizontally or go higher than 1350 horizontally.
        # Horizontally, the left of the screen is 0 pixels and the right is 1400 pixels.
        # Vertically, the top is 0 pixels and the bottom is 800 pixels.
        # 'x' is the vertical force and 'y' is the horizontal force acting on the ball.
        # If the ball is going left, y < 0; if it's going right, y > 0.
        # If the ball is going upward, x < 0, else x > 0.
        # This function defines the displacement of the ball according to the forces 'x' and 'y'.
        # The coordinates of the ball are self.b_pos_x and self.b_pos_y.

        # Gravity acceleration
        gravity=0.6
        if 4 > self.y > -4:
            friction_force = 0.01
        # Update vertical force with gravity
        self.x += gravity

        # Decrease horizontal force due to friction
        if self.y > 0:
            self.y -= friction_force
            if self.y < 0:
                self.y = 0
        elif self.y < 0:
            self.y += friction_force
            if self.y > 0:
                self.y = 0

        # Update horizontal position with horizontal force
        if self.b_pos_y + self.y < 100:  # If the ball goes too much to the left
            self.b_pos_y = 100
            self.y = -self.y  # Invert the horizontal force and decrease it
            self.y *= 0.9  # Decrease the horizontal force by 10%
        elif self.b_pos_y + self.y > 1300:  # If the ball goes too much to the right
            self.b_pos_y = 1300
            self.y = -self.y  # Invert the horizontal force and decrease it
            self.y *= 0.9  # Decrease the horizontal force by 10%
        else:
            self.b_pos_y += self.y

        # Update vertical position with vertical force
        if self.b_pos_x + self.x > 560:  # If the ball goes too high
            self.b_pos_x = 560
            self.x = -self.x  # Invert the vertical force and decrease it
            self.x *= 0.9  # Decrease the vertical force by 10%
        else:
            self.b_pos_x += self.x

        if self.ballon.colliderect(self.panierdroit) or self.ballon.colliderect(self.paniergauche):
            self.x=- self.x // 1.2
            self.y=- self.y // 1.2
            self.b_pos_x+=3 * self.x
            self.b_pos_y+=3 * self.y
        COLLIDING=False
        if self.ballon.colliderect(self.panierdroit_comptage):
            self.joueur2.point+=1
            print(self.joueur2.point)
            if self.joueur2.point >= 5 :
                pygame.mixer.music.stop()
                win =pygame.image.load("j1win.png").convert_alpha()
                win =pygame.transform.scale(win, (500, 500))
                self.surf.blit(win,(450, 200))
                pygame.display.update()
                panier = pygame.mixer.Sound("victoire.mp3")
                panier.play()
                time.sleep(5)
            else :
                pygame.mixer.pause()
                goal=pygame.mixer.Sound("goal.mp3")
                goal.play()
                time.sleep(1)
                pygame.mixer.unpause()
            COLLIDING=True
        if self.ballon.colliderect(self.paniergauche_comptage):
            self.joueur1.point+=1
            print(self.joueur1.point)
            if self.joueur1.point >= 5:
                pygame.mixer.music.stop()
                win = pygame.image.load("j2win.png").convert_alpha()
                win = pygame.transform.scale(win, (500, 500))
                self.surf.blit(win,(450, 200))
                pygame.display.update()
                panier = pygame.mixer.Sound("victoire.mp3")
                panier.play()
                time.sleep(5)
            else :
                pygame.mixer.pause()
                goal = pygame.mixer.Sound("goal.mp3")
                goal.play()
                time.sleep(1)
                pygame.mixer.unpause()
            COLLIDING=True
        if COLLIDING:
            self.b_pos_x=200
            self.b_pos_y=700
            self.x=0
            self.y=0
            self.possession=0
            self.joueur1.saute=False
            self.joueur1.jump_state=-12
            self.joueur1.pos_x=300
            self.joueur1.pos_y=400
            self.joueur2.saute=False
            self.joueur2.jump_state=-12
            self.joueur2.pos_x=1000
            self.joueur2.pos_y=400

    def collision(self):
        keys=pygame.key.get_pressed()
        if self.joueur1.objet.colliderect(self.joueur2.objet):
            if keys[ self.joueur1.keys[ 1 ] ] and self.joueur2.possession:
                kill = pygame.mixer.Sound("kill.mp3")
                kill.play()
                self.joueur2.possession=False
                self.possession=0
                self.b_pos_x-=200
                self.x-=10

            elif keys[ self.joueur2.keys[ 1 ] ] and self.joueur1.possession:
                kill = pygame.mixer.Sound("kill.mp3")
                kill.play()
                self.joueur1.possession=False
                self.possession=0
                self.b_pos_x-=200
                self.x-=10

    def tir(self):
        keys=pygame.key.get_pressed()
        if self.possession != 0:
            if keys[ self.joueur1.keys[ 1 ] ] and self.joueur1.possession:
                self.b_pos_x-=200
                self.b_pos_y+=20
                self.y=(1400 - self.joueur1.pos_x) // 52 + 2
                self.x=-15
                self.joueur1.possession=False
                self.possession=0
            if keys[ self.joueur2.keys[ 1 ] ] and self.joueur2.possession:
                self.b_pos_x-=200
                self.b_pos_y-=20
                self.y=(-self.joueur2.pos_x // 52) - 2
                self.x=-15
                self.joueur2.possession=False
                self.possession=0


if __name__ == '__main__':

    color = {
        "black": [
            [ "black_d_0.png", "black_d_1.png", "black_d_2.png", "black_d_3.png", "black_d_4.png" ],
            [ "black_g_0.png", "black_g_1.png", "black_g_2.png", "black_g_3.png", "black_g_4.png" ]
        ],
        "blue": [
            [ "blue_d_0.png", "blue_d_1.png", "blue_d_2.png", "blue_d_3.png", "blue_d_4.png" ],
            [ "blue_g_0.png", "blue_g_1.png", "blue_g_2.png", "blue_g_3.png", "blue_g_4.png" ]
        ],
        "green": [
            [ "green_d_0.png", "green_d_1.png", "green_d_2.png", "green_d_3.png", "green_d_4.png" ],
            [ "green_g_0.png", "green_g_1.png", "green_g_2.png", "green_g_3.png", "green_g_4.png" ]
        ],
        "gray": [
            [ "gray_d_0.png", "gray_d_1.png", "gray_d_2.png", "gray_d_3.png", "gray_d_4.png" ],
            [ "gray_g_0.png", "gray_g_1.png", "gray_g_2.png", "gray_g_3.png", "gray_g_4.png" ]
        ],
        "orange": [
            [ "orange_d_0.png", "orange_d_1.png", "orange_d_2.png", "orange_d_3.png", "orange_d_4.png" ],
            [ "orange_g_0.png", "orange_g_1.png", "orange_g_2.png", "orange_g_3.png", "orange_g_4.png" ]
        ],
        "purple": [
            [ "purple_d_0.png", "purple_d_1.png", "purple_d_2.png", "purple_d_3.png", "purple_d_4.png" ],
            [ "purple_g_0.png", "purple_g_1.png", "purple_g_2.png", "purple_g_3.png", "purple_g_4.png" ]
        ],
        "red": [
            [ "red_d_0.png", "red_d_1.png", "red_d_2.png", "red_d_3.png", "red_d_4.png" ],
            [ "red_g_0.png", "red_g_1.png", "red_g_2.png", "red_g_3.png", "red_g_4.png" ]
        ],
        "white": [
            [ "white_d_0.png", "white_d_1.png", "white_d_2.png", "white_d_3.png", "white_d_4.png" ],
            [ "white_g_0.png", "white_g_1.png", "white_g_2.png", "white_g_3.png", "white_g_4.png" ]
        ],
        "yellow": [
            [ "yellow_d_0.png", "yellow_d_1.png", "yellow_d_2.png", "yellow_d_3.png", "yellow_d_4.png" ],
            [ "yellow_g_0.png", "yellow_g_1.png", "yellow_g_2.png", "yellow_g_3.png", "yellow_g_4.png" ]
        ]
    }


    pygame.init()
    pygame.mixer.init()
    myfont=pygame.font.SysFont("LED", 80)
    sus=pygame.font.SysFont("LED", 50)
    clock=pygame.time.Clock()
    pygame.display.set_caption('SUS Basket')
    surf=pygame.display.set_mode((1400, 800))

    #l1=[ "amongus0.png", "amongus0bis.png", "amongus1.png", "amongus2.png", "amongus3.png","amongus4.png" ]  # the first element of the list is two element depending on what side the player is
    l1 = color["black"][0]
    joueur1=Joueur(300, 400, l1, 1, [ pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d ])  # right coordinate : 300,600
    #l2=[ "amongus0.png", "amongus0bis.png", "amongus1.png", "amongus2.png", "amongus3.png", "amongus4.png" ]
    l2 = color[ "purple" ][ 1 ]
    joueur2=Joueur(1000, 400, l2, 2, [ pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT ])
    # right coordinate : 1100,600

    terrain=pygame.image.load("terrain.png").convert_alpha()
    terrain=pygame.transform.scale(terrain, (1400, 800))

    ballon=pygame.image.load("ballon.png").convert_alpha()
    ballon=pygame.transform.scale(ballon, (60, 60))

    game=Game(joueur1, joueur2, terrain, ballon, surf)
    game.print_joueur()

    file = "theme.mp3"
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops=-1)
    while True:
        pygame.time.delay(10)
        surf.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        game.printbox()
        surf.blit(terrain, (0, 0))
        game.rebond()
        joueur1.deplacement(game)
        joueur2.deplacement(game)
        game.tir()
        game.collision()
        game.print_joueur()
        clock.tick(60)
        pygame.display.update()
