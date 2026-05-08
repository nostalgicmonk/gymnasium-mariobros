"""Utilities for playing NES environments interactively or with random actions."""
import numpy as np


def play_human(env):
    """
    Play the environment using keyboard input via pygame.

    Args:
        env: the Gymnasium environment to play

    Returns:
        None

    """
    import pygame
    from cynes import (
        NES_INPUT_A,
        NES_INPUT_B,
        NES_INPUT_SELECT,
        NES_INPUT_START,
        NES_INPUT_UP,
        NES_INPUT_DOWN,
        NES_INPUT_LEFT,
        NES_INPUT_RIGHT,
    )

    key_to_button = {
        pygame.K_UP: NES_INPUT_UP,
        pygame.K_DOWN: NES_INPUT_DOWN,
        pygame.K_LEFT: NES_INPUT_LEFT,
        pygame.K_RIGHT: NES_INPUT_RIGHT,
        pygame.K_z: NES_INPUT_B,
        pygame.K_x: NES_INPUT_A,
        pygame.K_a: NES_INPUT_SELECT,
        pygame.K_s: NES_INPUT_START,
    }

    pygame.init()
    scale = 2
    screen = pygame.display.set_mode((256 * scale, 240 * scale))
    pygame.display.set_caption('NES - Press ESC to quit')
    clock = pygame.time.Clock()

    state, info = env.reset()
    done = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        action = 0
        for key, button in key_to_button.items():
            if keys[key]:
                action |= button

        if done:
            state, info = env.reset()
            done = False
        else:
            state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

        surface = pygame.surfarray.make_surface(state.transpose(1, 0, 2))
        surface = pygame.transform.scale(surface, (256 * scale, 240 * scale))
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)


def play_random(env, steps=500):
    """
    Play the environment with random actions.

    Args:
        env: the Gymnasium environment to play
        steps: the number of random steps to take

    Returns:
        None

    """
    state, info = env.reset()
    for step in range(steps):
        action = env.action_space.sample()
        state, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            state, info = env.reset()
    env.close()
