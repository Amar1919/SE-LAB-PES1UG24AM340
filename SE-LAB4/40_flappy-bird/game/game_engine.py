import pygame
from .bird import Bird
from .pipe import Pipe

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
RED = (220, 50, 50)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bird = Bird(width // 4, height // 2)
        self.pipe_speed = 4
        self.pipe_interval = 90  # frames between pipe spawns
        self._spawn_timer = 0
        self.pipes = [Pipe(width + 100, height, speed=self.pipe_speed)]

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # Fonts for Game Over screen
        self.game_over_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.final_score_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.instruction_font = pygame.font.SysFont("Arial", 24)

        self.game_over = False

    def handle_event(self, event):
        # Ignore gameplay input after game over.
        if self.game_over:
            return

        # Flap is edge-triggered (KEYDOWN / MOUSEBUTTONDOWN), not held.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bird.flap()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.flap()

    def handle_input(self):
        # Reserved for continuously-held-key input.
        pass

    def update(self):
        # Stop normal gameplay once the game is over.
        if self.game_over:
            return

        self.bird.update()

        # Check ceiling and ground collision.
        if (
            self.bird.y - self.bird.radius <= 0
            or self.bird.y + self.bird.radius >= self.height
        ):
            self.game_over = True
            return

        self._spawn_timer += 1

        if self._spawn_timer >= self.pipe_interval:
            self._spawn_timer = 0
            self.pipes.append(
                Pipe(self.width, self.height, speed=self.pipe_speed)
            )

        for pipe in self.pipes:
            pipe.move()

            # Task 1: Refined collision detection.
            # Check the bird's full bounding rectangle.
            if (
                self.bird.rect().colliderect(pipe.top_rect())
                or self.bird.rect().colliderect(pipe.bottom_rect())
            ):
                self.game_over = True
                return

            # Score when the bird passes a pipe.
            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1

        self.pipes = [p for p in self.pipes if not p.off_screen()]

    def render(self, screen):
        # Draw pipes.
        for pipe in self.pipes:
            pygame.draw.rect(screen, GREEN, pipe.top_rect())
            pygame.draw.rect(screen, GREEN, pipe.bottom_rect())

        # Draw bird.
        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.bird.x), int(self.bird.y)),
            self.bird.radius
        )

        # Draw current score.
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )
        screen.blit(score_text, (10, 10))

        # Task 2: Game Over screen.
        if self.game_over:
            # Dark transparent overlay.
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(170)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # GAME OVER
            game_over_text = self.game_over_font.render(
                "GAME OVER",
                True,
                RED
            )

            game_over_rect = game_over_text.get_rect(
                center=(self.width // 2, self.height // 2 - 80)
            )

            screen.blit(game_over_text, game_over_rect)

            # Final score
            final_score_text = self.final_score_font.render(
                f"Final Score: {self.score}",
                True,
                WHITE
            )

            final_score_rect = final_score_text.get_rect(
                center=(self.width // 2, self.height // 2)
            )

            screen.blit(final_score_text, final_score_rect)

            # Instruction
            instruction_text = self.instruction_font.render(
                "Close the window to exit",
                True,
                WHITE
            )

            instruction_rect = instruction_text.get_rect(
                center=(self.width // 2, self.height // 2 + 60)
            )

            screen.blit(instruction_text, instruction_rect)