import pygame
import os

from .bird import Bird
from .pipe import Pipe


# Game colors
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
RED = (220, 50, 50)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # -------------------------------------------------
        # Task 4: Sound Effects
        # -------------------------------------------------
        sound_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "sounds"
        )

        self.flap_sound = pygame.mixer.Sound(
            os.path.join(sound_path, "flap.wav")
        )

        self.score_sound = pygame.mixer.Sound(
            os.path.join(sound_path, "score.wav")
        )

        self.death_sound = pygame.mixer.Sound(
            os.path.join(sound_path, "death.wav")
        )

        # Prevent death sound from playing multiple times
        self.death_sound_played = False

        # -------------------------------------------------
        # Task 3: Difficulty Settings
        # -------------------------------------------------
        self.difficulty = "Medium"

        self.difficulty_settings = {
            "Easy": {
                "speed": 3,
                "gap": 190
            },
            "Medium": {
                "speed": 4,
                "gap": 150
            },
            "Hard": {
                "speed": 6,
                "gap": 120
            }
        }

        # Bird
        self.bird = Bird(
            width // 4,
            height // 2
        )

        # Pipe settings
        self.pipe_interval = 90
        self._spawn_timer = 0

        self.pipes = []

        # Initialize game
        self.reset_game()

        # Score
        self.score = 0

        # Normal score font
        self.font = pygame.font.SysFont(
            "Arial",
            30
        )

        # Game Over fonts
        self.game_over_font = pygame.font.SysFont(
            "Arial",
            60,
            bold=True
        )

        self.final_score_font = pygame.font.SysFont(
            "Arial",
            40,
            bold=True
        )

        self.instruction_font = pygame.font.SysFont(
            "Arial",
            24
        )

        self.game_over = False

    # -------------------------------------------------
    # Reset Game
    # -------------------------------------------------
    def reset_game(self):
        """Reset all gameplay state for a new game."""

        settings = self.difficulty_settings[
            self.difficulty
        ]

        # Reset bird
        self.bird = Bird(
            self.width // 4,
            self.height // 2
        )

        # Apply difficulty settings
        self.pipe_speed = settings["speed"]
        self.pipe_gap = settings["gap"]

        # Reset timers
        self._spawn_timer = 0

        # Create first pipe
        self.pipes = [
            Pipe(
                self.width + 100,
                self.height,
                gap=self.pipe_gap,
                speed=self.pipe_speed
            )
        ]

        # Reset score
        self.score = 0

        # Reset Game Over
        self.game_over = False

        # Allow death sound to play again
        self.death_sound_played = False

    # -------------------------------------------------
    # Task 4: Death Sound
    # -------------------------------------------------
    def play_death_sound(self):
        """Play death sound only once."""

        if not self.death_sound_played:
            self.death_sound.play()
            self.death_sound_played = True

    # -------------------------------------------------
    # Handle Events
    # -------------------------------------------------
    def handle_event(self, event):

        # -------------------------------------------------
        # Task 3: Game Over Menu
        # -------------------------------------------------
        if self.game_over:

            if event.type == pygame.KEYDOWN:

                # Easy
                if event.key == pygame.K_1:
                    self.difficulty = "Easy"
                    self.reset_game()

                # Medium
                elif event.key == pygame.K_2:
                    self.difficulty = "Medium"
                    self.reset_game()

                # Hard
                elif event.key == pygame.K_3:
                    self.difficulty = "Hard"
                    self.reset_game()

                # Exit
                elif event.key == pygame.K_4:
                    pygame.event.post(
                        pygame.event.Event(
                            pygame.QUIT
                        )
                    )

            return

        # -------------------------------------------------
        # Normal Gameplay
        # -------------------------------------------------

        # Space → flap
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
        ):
            self.bird.flap()

            # Task 4: Flap sound
            self.flap_sound.play()

        # Mouse click → flap
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.flap()

            # Task 4: Flap sound
            self.flap_sound.play()

    # -------------------------------------------------
    # Handle Continuous Input
    # -------------------------------------------------
    def handle_input(self):
        # Reserved for continuously-held-key input.
        pass

    # -------------------------------------------------
    # Update Game
    # -------------------------------------------------
    def update(self):

        # Stop gameplay after Game Over
        if self.game_over:
            return

        # Update bird
        self.bird.update()

        # -------------------------------------------------
        # Ground / Ceiling Collision
        # -------------------------------------------------
        if (
            self.bird.y - self.bird.radius <= 0
            or
            self.bird.y + self.bird.radius >= self.height
        ):
            self.game_over = True

            # Task 4: Death sound
            self.play_death_sound()

            return

        # -------------------------------------------------
        # Spawn Pipes
        # -------------------------------------------------
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

        # -------------------------------------------------
        # Update Pipes
        # -------------------------------------------------
        for pipe in self.pipes:

            pipe.move()

            # -------------------------------------------------
            # Task 1: Improved Collision Detection
            # -------------------------------------------------
            if (
                self.bird.rect().colliderect(
                    pipe.top_rect()
                )
                or
                self.bird.rect().colliderect(
                    pipe.bottom_rect()
                )
            ):
                self.game_over = True

                # Task 4: Death sound
                self.play_death_sound()

                return

            # -------------------------------------------------
            # Score
            # -------------------------------------------------
            if (
                not pipe.scored
                and pipe.x + pipe.width < self.bird.x
            ):
                pipe.scored = True

                self.score += 1

                # Task 4: Score sound
                self.score_sound.play()

        # Remove pipes that have gone off screen
        self.pipes = [
            p for p in self.pipes
            if not p.off_screen()
        ]

    # -------------------------------------------------
    # Render Game
    # -------------------------------------------------
    def render(self, screen):

        # -------------------------------------------------
        # Draw Pipes
        # -------------------------------------------------
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

        # -------------------------------------------------
        # Draw Bird
        # -------------------------------------------------
        pygame.draw.circle(
            screen,
            WHITE,
            (
                int(self.bird.x),
                int(self.bird.y)
            ),
            self.bird.radius
        )

        # -------------------------------------------------
        # Current Score
        # -------------------------------------------------
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (10, 10)
        )

        # -------------------------------------------------
        # Game Over Screen
        # -------------------------------------------------
        if self.game_over:

            # Dark overlay
            overlay = pygame.Surface(
                (self.width, self.height)
            )

            overlay.set_alpha(170)

            overlay.fill(
                (0, 0, 0)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

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

            # Final Score
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

            # Difficulty / Replay options
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