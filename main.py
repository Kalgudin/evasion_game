import sys
from settings import *
from game import Game
from button import Button


class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Vertical Dodge - Три дорожки (стрелки)")
        self.clock = pygame.time.Clock()

        self.selected_color = BLUE
        self.characters = {
            "Синий бегун": BLUE,
            "Красный спринтер": RED,
            "Зелёный прыгун": GREEN
        }
        self.create_buttons()

    def create_buttons(self):
        btn_w, btn_h = 220, 50
        center_x = SCREEN_WIDTH // 2 - btn_w // 2

        self.btns_chars = {}
        y = 150
        for name, color in self.characters.items():
            self.btns_chars[name] = Button(center_x, y, btn_w, btn_h, name, color, WHITE, (0, 100, 200), FONT_MEDIUM)
            y += 70

        self.btn_start = Button(center_x, 380, btn_w, btn_h, "Старт", GREEN, WHITE, (0, 150, 0), FONT_LARGE)
        self.btn_quit = Button(center_x, 460, btn_w, btn_h, "Выход", RED, WHITE, (150, 0, 0), FONT_MEDIUM)

    def draw(self):
        self.screen.fill(SKY_BLUE)
        font_title = pygame.font.Font(None, 60)
        title = font_title.render("VERTICAL DODGE", True, BLACK)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 150, 50))
        subtitle = pygame.font.Font(None, FONT_SMALL).render("Выбери персонажа и нажми Старт", True, BLACK)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - 150, 110))

        for btn in self.btns_chars.values():
            btn.draw(self.screen)
            btn.update_hover(pygame.mouse.get_pos())
        self.btn_start.draw(self.screen)
        self.btn_start.update_hover(pygame.mouse.get_pos())
        self.btn_quit.draw(self.screen)
        self.btn_quit.update_hover(pygame.mouse.get_pos())

        preview_rect = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80, 60, 60)
        pygame.draw.rect(self.screen, self.selected_color, preview_rect)
        pygame.draw.rect(self.screen, BLACK, preview_rect, 2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for name, btn in self.btns_chars.items():
                    if btn.is_clicked(pos):
                        self.selected_color = self.characters[name]
                if self.btn_start.is_clicked(pos):
                    self.start_game()
                if self.btn_quit.is_clicked(pos):
                    return False
        return True

    def start_game(self):
        game = Game(self.screen, self.selected_color)
        game.run()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    menu = MainMenu()
    menu.run()