import pygame
import sys
import settings as S

pygame.init()

# Set the music
pygame.mixer.init()

# Set the fps
clock = pygame.time.Clock()

# Set screen size
screen = pygame.display.set_mode((1400, 800))


music = "theme.mp3"

pygame.mixer.music.load(music)
pygame.mixer.music.play(loops=-1)  # If the loops is -1 then the music will repeat indefinitely.

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

def menu():
    # Set the background
    background = pygame.image.load("background.jpg").convert_alpha()
    background = pygame.transform.scale(background, (1400, 800))

    play_button = button((0, 0, 0), 100, 100, 170, 70, 'Play')
    settings_button = button((0, 0, 0), 100, 200, 170, 70, 'Settings')
    exit_button = button((0, 0, 0), 100, 300, 170, 70, 'Exits')

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Handle events
        pygame.time.delay(10)
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        play_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

        pos = pygame.mouse.get_pos()

        if exit_button.click(pos) is True and event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()

        if play_button.click(pos) is True and event.type == pygame.MOUSEBUTTONDOWN:
            print("go jouer")

        if settings_button.click(pos) is True and event.type == pygame.MOUSEBUTTONDOWN:
            S.main_setting()

        pygame.display.flip()
        clock.tick(60)

        # Update display
        pygame.display.update()


menu()

