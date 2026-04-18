import random
from settings import *


class Obstacle:
    def __init__(self, lane_idx):
        self.lane_idx = lane_idx
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(DARK_GRAY)
        pygame.draw.rect(self.image, BLACK, (0, 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT), 2)
        pygame.draw.circle(self.image, RED, (OBSTACLE_WIDTH // 2, OBSTACLE_HEIGHT // 2), 12)

        self.rect = self.image.get_rect()
        self.rect.centerx = LANE_X[lane_idx]
        self.rect.y = -OBSTACLE_HEIGHT  # появляется сверху
        self.speed = OBSTACLE_BASE_SPEED

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_offscreen(self):
        return self.rect.top > SCREEN_HEIGHT

    @staticmethod
    def spawn_logic(obstacles, frame_count, current_speed):
        if frame_count % max(30, OBSTACLE_SPAWN_DELAY - current_speed) == 0 and len(obstacles) < MAX_OBSTACLES:
            lane = random.randint(0, 2)
            return Obstacle(lane)
        return None


class Coin:
    def __init__(self, lane_idx):
        self.lane_idx = lane_idx
        self.image = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (COIN_SIZE // 2, COIN_SIZE // 2), COIN_SIZE // 2)
        pygame.draw.circle(self.image, (255, 215, 0), (COIN_SIZE // 2, COIN_SIZE // 2), COIN_SIZE // 2 - 3)
        self.rect = self.image.get_rect()
        self.rect.centerx = LANE_X[lane_idx]
        self.rect.y = -COIN_SIZE
        self.speed = COIN_BASE_SPEED

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_offscreen(self):
        return self.rect.top > SCREEN_HEIGHT