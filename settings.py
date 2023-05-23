import menu as m
import pygame
import sys

pygame.init()

# Set the music
pygame.mixer.init()

# Set the fps
clock = pygame.time.Clock()

# Set screen size
screen = pygame.display.set_mode((1400, 800))

font = pygame.font.Font(None, 35)

music = "theme.mp3"

pygame.mixer.music.load(music)
pygame.mixer.music.play(loops=-1)  # If the loops is -1 then the music will repeat indefinitely.

skin_list = ["Purple", "Orange", "White", "Green", "Yellow", "Brown", "Blue", "Black", "Red"]
selected_skin = None
menu_open = False

player_1 = {"skin": "Blue","up": "pygame.K_z ","grab": "pygame.K_s ","left": "pygame.K_q ","right": "pygame.K_d"}
player_2 = {"skin": "Red","up": "pygame.K_UP  ","grab": "pygame.K_DOWN","left": "pygame.K_LEFT ","right": "pygame.K_RIGHT"}


k_up_p1 = ""
k_grab_p1 = ""
k_left_p1 = ""
k_right_p1 = ""

k_up_p2 = ""
k_grab_p2 = ""
k_left_p2 = ""
k_right_p2 = ""

skin_p1 = ""
skin_p2 = ""

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2),
                self.y + (self.height / 2 - text.get_height() / 2)))

    def click(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
            return False


# Classe représentant le menu déroulant
class DropdownMenu:
    def __init__(self, x, y, width, height, options):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_option = None

    def handle_event(self, event):
        if self.rect.collidepoint(event.pos):
            global menu_open
            menu_open = True
        elif menu_open:
            for i, option_rect in enumerate(self.option_rects):
                    if option_rect.collidepoint(event.pos):
                        self.selected_option = self.options[i]
                        global selected_skin
                        selected_skin = self.selected_option
                        menu_open = False
        return self.selected_option

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        pygame.draw.line(screen, (255, 255, 255), (self.rect.right - 20, self.rect.top + 10),
                         (self.rect.right - 10, self.rect.top + 10), 2)

        text_surface = font.render(self.selected_option or "Select a skin", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        if menu_open:
            self.option_rects = []
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.bottom + i * self.rect.height, self.rect.width,
                                          self.rect.height)
                pygame.draw.rect(screen, (255, 255, 255), option_rect)
                text_surface = font.render(option, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=option_rect.center)
                screen.blit(text_surface, text_rect)
                self.option_rects.append(option_rect)



class ZoneTexte:
    def __init__(self, x, y, largeur, hauteur, police, couleur_fond=pygame.Color('white'), couleur_texte=pygame.Color('black')):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.police = police
        self.couleur_fond = couleur_fond
        self.couleur_texte = couleur_texte
        self.texte = ''
        self.actif = False

    def afficher(self, fenetre):
        # Dessiner la zone de texte
        pygame.draw.rect(fenetre, self.couleur_fond, (self.x, self.y, self.largeur, self.hauteur))
        pygame.draw.rect(fenetre, pygame.Color('black'), (self.x, self.y, self.largeur, self.hauteur), 2)

        # Afficher le texte
        texte_surface = self.police.render(self.texte, True, self.couleur_texte)
        fenetre.blit(texte_surface, (self.x + 5, self.y + 5))

    def gestion_evenements(self, event):
        if event.type == pygame.KEYDOWN:
            if self.actif:
                if event.key == pygame.K_RETURN:
                    self.actif = False
                elif event.key == pygame.K_BACKSPACE:
                    self.texte = self.texte[:-1]
                else:
                    self.texte = event.unicode
        return self.texte

    def est_clique(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            souris_x, souris_y = event.pos
            if self.x <= souris_x <= self.x + self.largeur and self.y <= souris_y <= self.y + self.hauteur:
                self.actif = True
            else:
                self.actif = False

def main_setting():


    # Set the background
    background = pygame.image.load("background.jpg").convert_alpha()
    background = pygame.transform.scale(background, (1400, 800))

    back_button = button((0, 0, 0), 1000, 270, 170, 70, 'Menu')
    apply_button = button((0, 0, 0), 1000, 370, 170, 70, 'Apply')

    player1_button = button((0, 0, 0), 100, 70, 170, 70, 'Player 1:')
    up_p1 = button((0, 0, 0), 100, 270, 170, 70, 'UP:')
    left_p1 = button((0, 0, 0), 100, 370, 170, 70, 'LEFT:')
    right_p1 = button((0, 0, 0), 100, 470, 170, 70, 'RIGHT:')
    grab_p1 = button((0, 0, 0), 100, 570, 170, 70, 'GRAB:')
    color_p1 = button((0, 0, 0), 100, 170, 170, 70, 'COLOR:')
    color_choise_p1= DropdownMenu(290, 195, 170, 30, skin_list)

    player2_button = button((0, 0, 0), 500, 70, 170, 70, 'Player 2:')
    up_p2 = button((0, 0, 0), 500, 270, 170, 70, 'UP:')
    left_p2 = button((0, 0, 0), 500, 370, 170, 70, 'LEFT:')
    right_p2 = button((0, 0, 0), 500, 470, 170, 70, 'RIGHT:')
    grab_p2 = button((0, 0, 0), 500, 570, 170, 70, 'GRAB:')
    color_p2 = button((0, 0, 0), 500, 170, 170, 70, 'COLOR:')
    color_choise_p2 = DropdownMenu(690, 195, 170, 30, skin_list)

    c_up_p1 = ZoneTexte(270, 295, 50, 35, font)
    c_grab_p1 = ZoneTexte(270, 395, 50, 35, font)
    c_left_p1 = ZoneTexte(270, 495, 50, 35, font)
    c_right_p1 = ZoneTexte(270, 595, 50, 35, font)

    c_up_p2 = ZoneTexte(670, 295, 50, 35, font)
    c_grab_p2 = ZoneTexte(670, 395, 50, 35, font)
    c_left_p2 = ZoneTexte(670, 495, 50, 35, font)
    c_right_p2 = ZoneTexte(670, 595, 50, 35, font)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                c_up_p1.est_clique(event)
                c_grab_p1.est_clique(event)
                c_left_p1.est_clique(event)
                c_right_p1.est_clique(event)

                c_up_p2.est_clique(event)
                c_grab_p2.est_clique(event)
                c_left_p2.est_clique(event)
                c_right_p2.est_clique(event)

                skin_p2 = color_choise_p2.handle_event(event)
                skin_p1 = color_choise_p1.handle_event(event)

            else:

                k_up_p1=c_up_p1.gestion_evenements(event)
                k_grab_p1=c_grab_p1.gestion_evenements(event)
                k_left_p1=c_left_p1.gestion_evenements(event)
                k_right_p1=c_right_p1.gestion_evenements(event)

                k_up_p2=c_up_p2.gestion_evenements(event)
                k_grab_p2=c_grab_p2.gestion_evenements(event)
                k_left_p2=c_left_p2.gestion_evenements(event)
                k_right_p2=c_right_p2.gestion_evenements(event)


        pos = pygame.mouse.get_pos()


        # Handle events
        pygame.time.delay(10)
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        back_button.draw(screen)
        apply_button.draw(screen)

        player1_button.draw(screen)
        up_p1.draw(screen)
        left_p1.draw(screen)
        right_p1.draw(screen)
        grab_p1.draw(screen)
        color_p1.draw(screen)

        player2_button.draw(screen)
        up_p2.draw(screen)
        left_p2.draw(screen)
        right_p2.draw(screen)
        grab_p2.draw(screen)
        color_p2.draw(screen)

        color_choise_p1.draw()
        color_choise_p2.draw()

        c_up_p1.afficher(screen)
        c_grab_p1.afficher(screen)
        c_left_p1.afficher(screen)
        c_right_p1.afficher(screen)

        c_up_p2.afficher(screen)
        c_grab_p2.afficher(screen)
        c_left_p2.afficher(screen)
        c_right_p2.afficher(screen)


        if apply_button.click(pos) is True and event.type == pygame.MOUSEBUTTONDOWN:
            player_1["skin"] = skin_p1
            player_1["up"] = k_up_p1
            player_1["grab"] = k_grab_p1
            player_1["left"] = k_left_p1
            player_1["right"] = k_right_p1

            player_2["skin"] = skin_p2
            player_2["up"] = k_up_p2
            player_2["grab"] = k_grab_p2
            player_2["left"] = k_left_p2
            player_2["right"] = k_right_p2

            print(player_1)
            print(player_2)



        if back_button.click(pos) is True and event.type == pygame.MOUSEBUTTONDOWN:
            m.menu()

        pygame.display.flip()
        clock.tick(60)

        # Update display
        pygame.display.update()