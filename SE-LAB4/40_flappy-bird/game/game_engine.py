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

        # Default difficulty
        self.difficulty = "Medium"

        # Difficulty settings: speed and gap
        self.difficulty_settings = {
            "Easy": {"speed": 3, "gap": 190},
            "Medium": {"speed": 4, "gap": 150},
            "Hard": {"speed": 6, "gap": 120},
        }

        self.bird = Bird(width // 4, height // 2)

        self.pipe_interval = 90
        self._spawn_timer = 0

        self.pipes = []
        self.reset_game()

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # Game Over screen fonts
        self.game_over_font = pygame.font.SysFont(
            "Arial", 60, bold=True
        )
        self.final_score_font = pygame.font.SysFont(
            "Arial", 40, bold=True
        )
        self.instruction_font = pygame.font.SysFont(
            "Arial", 24
        )

        self.game_over = False

    def reset_game(self):
        """Reset all gameplay state for a new game."""
        settings = self.difficulty_settings[self.difficulty]

        self.bird = Bird(self.width // 4, self.height // 2)

        self.pipe_speed = settings["speed"]
        self.pipe_gap = settings["gap"]

        self._spawn_timer = 0

        self.pipes = [
            Pipe(
                self.width + 100,
                self.height,
                gap=self.pipe_gap,
                speed=self.pipe_speed
            )
        ]

        self.score = 0
        self.game_over = False

    def handle_event(self, event):
        # Handle Game Over menu.
        if self.game_over:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    self.difficulty = "Easy"
                    self.reset_game()

                elif event.key == pygame.K_2:
                    self.difficulty = "Medium"
                    self.reset_game()

                elif event.key == pygame.K_3:
                    self.difficulty = "Hard"
                    self.reset_game()

                elif event.key == pygame.K_4:
                    pygame.event.post(
                        pygame.event.Event(pygame.QUIT)
                    )

            return

        # Normal gameplay input.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bird.flap()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.flap()

    def handle_input(self):
        # Reserved for continuously-held-key input.
        pass

    def update(self):
        # Stop gameplay while Game Over screen is displayed.
        if self.game_over:
            return

        self.bird.update()

        # Ceiling / ground collision.
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
                Pipe(
                    self.width,
                    self.height,
                    gap=self.pipe_gap,
                    speed=self.pipe_speed
                )
            )

        for pipe in self.pipes:
            pipe.move()

            # Task 1: Full bird rectangle collision detection.
            if (
                self.bird.rect().colliderect(pipe.top_rect())
                or self.bird.rect().colliderect(pipe.bottom_rect())
            ):
                self.game_over = True
                return

            # Score when bird passes pipe.
            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1

        self.pipes = [
            p for p in self.pipes
            if not p.off_screen()
        ]

    def render(self, screen):
        # Draw pipes.
        for pipe in self.pipes:
            pygame.draw.rect(
                screen,
                GREEN,
                pipe.top_rect()
            )

            pygame.draw.rect(
                screen,
                GREEN,
                pipe.bottom_rect()
            )

        # Draw bird.
        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.bird.x), int(self.bird.y)),
            self.bird.radius
        )

        # Current score.
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )

        screen.blit(score_text, (10, 10))

        # Game Over screen.
        if self.game_over:
            overlay = pygame.Surface(
                (self.width, self.height)
            )
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
                center=(
                    self.width // 2,
                    self.height // 2 - 150
                )
            )

            screen.blit(
                game_over_text,
                game_over_rect
            )

            # Final score
            final_score_text = self.final_score_font.render(
                f"Final Score: {self.score}",
                True,
                WHITE
            )

            final_score_rect = final_score_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 - 80
                )
            )

            screen.blit(
                final_score_text,
                final_score_rect
            )

            # Difficulty options
            options = [
                "1 - Easy",
                "2 - Medium",
                "3 - Hard",
                "4 - Exit"
            ]

            for i, option in enumerate(options):
                option_text = self.instruction_font.render(
                    option,
                    True,
                    WHITE
                )

                option_rect = option_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + i * 40
                    )
                )

                screen.blit(
                    option_text,
                    option_rect
                )