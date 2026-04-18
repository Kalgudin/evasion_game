
from settings import *


class Player:
    def __init__(self, lane_idx=1, color=BLUE, character_type="standard"):
        self.lane_idx = lane_idx
        self.character_type = character_type
        self.color = color
        self.rect = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect.centerx = LANE_X[lane_idx]
        self.rect.y = PLAYER_Y

        self.is_jumping = False
        self.jump_timer = 0
        self.y_velocity = 0
        self.original_y = PLAYER_Y

        self.walk_cycle = 0
        self.animation_speed = 0.2

    def set_lane(self, lane_idx):
        if 0 <= lane_idx < len(LANE_X):
            self.lane_idx = lane_idx
            if not self.is_jumping:
                self.rect.centerx = LANE_X[lane_idx]

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_timer = PLAYER_JUMP_DURATION
            self.y_velocity = PLAYER_JUMP_POWER
            return True
        return False

    def update(self):
        if self.is_jumping:
            self.y_velocity += PLAYER_GRAVITY
            self.rect.y += self.y_velocity
            self.jump_timer -= 1
            if self.jump_timer <= 0 or self.rect.y >= self.original_y:
                self.rect.y = self.original_y
                self.is_jumping = False
                self.y_velocity = 0
        else:
            self.rect.centerx = LANE_X[self.lane_idx]
            self.rect.y = self.original_y
            self.walk_cycle += self.animation_speed
            if self.walk_cycle >= 2 * 3.14159:
                self.walk_cycle = 0

    def draw_character(self, screen, x, y, is_jumping):
        head_radius = 18
        body_height = 25

        if self.character_type == 'blue':
            skin = (255, 220, 177)
            hair = (92, 64, 51)
            shirt = (70, 130, 230)
            pants = (30, 60, 120)
        elif self.character_type == 'red':
            skin = (255, 220, 177)
            hair = (200, 60, 30)
            shirt = (220, 60, 50)
            pants = (120, 30, 30)
        else:
            skin = (255, 220, 177)
            hair = (60, 40, 30)
            shirt = (60, 180, 80)
            pants = (30, 100, 40)

        cx = x + PLAYER_WIDTH // 2
        cy = y + PLAYER_HEIGHT // 2 + 5

        if not is_jumping:
            angle = self.walk_cycle
            arm_offset = int(5 * pygame.math.Vector2(1, 0).rotate(angle * 30).x)
            leg_offset_anim = int(4 * pygame.math.Vector2(1, 0).rotate(angle * 40).x)
        else:
            arm_offset = 0
            leg_offset_anim = 0

        # Ноги
        leg_left = (cx - 8 + leg_offset_anim, cy + body_height - 5)
        leg_right = (cx + 8 - leg_offset_anim, cy + body_height - 5)
        pygame.draw.line(screen, pants, (cx - 5, cy + body_height - 10), leg_left, 5)
        pygame.draw.line(screen, pants, (cx + 5, cy + body_height - 10), leg_right, 5)

        # Тело
        body_rect = pygame.Rect(cx - 12, cy, 24, body_height)
        pygame.draw.rect(screen, shirt, body_rect)

        # Руки
        arm_left = (cx - 15 + arm_offset, cy + 12)
        arm_right = (cx + 15 - arm_offset, cy + 12)
        pygame.draw.line(screen, skin, (cx - 10, cy + 8), arm_left, 6)
        pygame.draw.line(screen, skin, (cx + 10, cy + 8), arm_right, 6)

        # Голова
        pygame.draw.circle(screen, skin, (cx, cy - 5), head_radius)

        # Глаза
        eye_offset = 6
        eye_radius = 3
        pygame.draw.circle(screen, WHITE, (cx - eye_offset, cy - 10), eye_radius + 1)
        pygame.draw.circle(screen, WHITE, (cx + eye_offset, cy - 10), eye_radius + 1)
        pygame.draw.circle(screen, BLACK, (cx - eye_offset, cy - 10), eye_radius - 1)
        pygame.draw.circle(screen, BLACK, (cx + eye_offset, cy - 10), eye_radius - 1)
        pygame.draw.circle(screen, WHITE, (cx - eye_offset - 1, cy - 11), 1)
        pygame.draw.circle(screen, WHITE, (cx + eye_offset - 1, cy - 11), 1)

        # Рот
        if not is_jumping:
            pygame.draw.arc(screen, BLACK, (cx - 8, cy - 8, 16, 12), 0.1, 3.0, 2)
        else:
            pygame.draw.arc(screen, BLACK, (cx - 8, cy - 5, 16, 10), 3.5, 6.0, 2)

        # Волосы
        hair_points = [(cx - 12, cy - 18), (cx - 5, cy - 25), (cx, cy - 28),
                       (cx + 5, cy - 25), (cx + 12, cy - 18)]
        pygame.draw.polygon(screen, hair, hair_points)

        # Пояс
        pygame.draw.line(screen, BLACK, (cx - 10, cy + body_height - 12), (cx + 10, cy + body_height - 12), 2)
        pygame.draw.rect(screen, (200, 200, 200), (cx - 4, cy + body_height - 20, 8, 8))

    def draw(self, screen):
        self.draw_character(screen, self.rect.x, self.rect.y, self.is_jumping)


