
import random
from settings import *
from player import Player
from obstacle import Obstacle, Coin


class Game:
    def __init__(self, screen, player_color=BLUE):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.highscore = self.load_highscore()
        self.player_color = player_color

        self.player = None
        self.obstacles = []
        self.coins = []

        self.frame_count = 0
        self.game_speed = OBSTACLE_BASE_SPEED
        self.difficulty_timer = 0

        self.init_sounds()

    def init_sounds(self):
        pygame.mixer.init()
        self.jump_sound = self.create_beep(440, 0.1)
        self.coin_sound = self.create_beep(880, 0.08)
        self.hit_sound = self.create_beep(220, 0.3)

    def create_beep(self, freq, duration):
        try:
            sample_rate = 44100
            n_samples = int(sample_rate * duration)
            buf = pygame.sndarray.make_sound(
                (32767 * [0.5 * (1 - abs(2 * i / n_samples - 1)) *
                          (1 if i < n_samples / 2 else -1) for i in range(n_samples)])
            )
            return buf
        except:
            return None

    def load_highscore(self):
        try:
            with open(HIGHSCORE_FILE, 'r') as f:
                return int(f.read())
        except:
            return 0

    def save_highscore(self):
        try:
            with open(HIGHSCORE_FILE, 'w') as f:
                f.write(str(self.highscore))
        except:
            pass

    def reset(self):
        if self.player_color == BLUE:
            char_type = 'blue'
        elif self.player_color == RED:
            char_type = 'red'
        else:
            char_type = 'green'
        self.player = Player(lane_idx=1, color=self.player_color, character_type=char_type)
        self.obstacles.clear()
        self.coins.clear()
        self.score = 0
        self.running = True
        self.frame_count = 0
        self.game_speed = OBSTACLE_BASE_SPEED
        self.difficulty_timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_LEFT:
                    self.player.set_lane(self.player.lane_idx - 1)
                elif event.key == pygame.K_RIGHT:
                    self.player.set_lane(self.player.lane_idx + 1)
                elif event.key == pygame.K_UP:
                    if self.player.jump() and self.jump_sound:
                        self.jump_sound.play()
        return True

    def update(self):
        self.frame_count += 1
        self.difficulty_timer += 1

        if self.difficulty_timer > 300:
            self.difficulty_timer = 0
            self.game_speed = min(12, self.game_speed + 0.5)

        self.player.update()

        # Обновление препятствий
        for obs in self.obstacles[:]:
            obs.speed = self.game_speed
            obs.update()
            if obs.is_offscreen():
                self.obstacles.remove(obs)
                self.score += SCORE_PER_OBSTACLE

        # Обновление монет
        for coin in self.coins[:]:
            coin.speed = self.game_speed
            coin.update()
            if coin.is_offscreen():
                self.coins.remove(coin)

        # Спавн препятствий
        new_obs = Obstacle.spawn_logic(self.obstacles, self.frame_count, self.game_speed)
        if new_obs:
            self.obstacles.append(new_obs)

        # Спавн монет
        if self.frame_count % max(30, COIN_SPAWN_DELAY - int(self.game_speed)) == 0 and len(self.coins) < 6:
            lane = random.randint(0, 2)
            self.coins.append(Coin(lane))

        # === ПРОСТАЯ И НАДЁЖНАЯ ПРОВЕРКА ===
        # Если игрок в прыжке - он неуязвим для препятствий
        for obs in self.obstacles[:]:
            if self.player.lane_idx == obs.lane_idx and self.player.rect.colliderect(obs.rect):
                if self.player.is_jumping:
                    # Перепрыгнул - ничего не делаем
                    continue
                else:
                    if self.hit_sound:
                        self.hit_sound.play()
                    self.running = False
                    return
        # =================================

        # Сбор монет (без изменений)
        for coin in self.coins[:]:
            if self.player.lane_idx == coin.lane_idx and self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.score += COIN_VALUE
                if self.coin_sound:
                    self.coin_sound.play()

        if self.score > self.highscore:
            self.highscore = self.score
            self.save_highscore()

    def draw_background(self):
        self.screen.fill(SKY_BLUE)
        for i, x in enumerate(LANE_X):
            color = GRAY if i == 1 else DARK_GRAY
            pygame.draw.line(self.screen, color, (x - 30, 0), (x - 30, SCREEN_HEIGHT), 4)
            pygame.draw.line(self.screen, BLACK, (x - 30, 0), (x - 30, SCREEN_HEIGHT), 1)
            pygame.draw.line(self.screen, color, (x + 30, 0), (x + 30, SCREEN_HEIGHT), 4)
            pygame.draw.line(self.screen, BLACK, (x + 30, 0), (x + 30, SCREEN_HEIGHT), 1)
            for y in range(0, SCREEN_HEIGHT, 50):
                pygame.draw.rect(self.screen, BROWN, (x - 15, y, 30, 10))
        pygame.draw.rect(self.screen, (34, 139, 34), (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

    def draw(self):
        self.draw_background()
        for obs in self.obstacles:
            obs.draw(self.screen)
        for coin in self.coins:
            coin.draw(self.screen)
        self.player.draw(self.screen)

        font = pygame.font.Font(None, FONT_MEDIUM)
        score_txt = font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_txt, (10, 10))
        high_txt = font.render(f"Best: {self.highscore}", True, BLACK)
        self.screen.blit(high_txt, (10, 50))
        speed_txt = font.render(f"Speed: {self.game_speed:.1f}", True, BLACK)
        self.screen.blit(speed_txt, (SCREEN_WIDTH - 120, 10))

        # Отладочная информация (показывает позиции игрока и препятствия)
        if self.obstacles:
            nearest = self.obstacles[0]
            debug_font = pygame.font.Font(None, 18)
            debug_txt = debug_font.render(f"Player Y: {self.player.rect.bottom} Obs Top: {nearest.rect.top}", True,
                                          BLACK)
            self.screen.blit(debug_txt, (10, 90))

    def show_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, FONT_LARGE)
        game_over = font_large.render("GAME OVER", True, RED)
        self.screen.blit(game_over, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 80))

        font_med = pygame.font.Font(None, FONT_MEDIUM)
        final = font_med.render(f"Final Score: {self.score}", True, WHITE)
        self.screen.blit(final, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
        best = font_med.render(f"Best: {self.highscore}", True, YELLOW)
        self.screen.blit(best, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 20))
        restart = font_med.render("Press SPACE to restart, ESC to quit", True, WHITE)
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 80))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False
        return False

    def run(self):
        self.reset()
        while True:
            if not self.handle_events():
                return False
            if self.running:
                self.update()
                self.draw()
            else:
                if not self.show_game_over():
                    return False
                else:
                    self.reset()
            pygame.display.flip()
            self.clock.tick(FPS)


