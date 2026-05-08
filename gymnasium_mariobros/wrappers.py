"""Wrappers for NES environments to modify action spaces."""
import gymnasium
import numpy as np
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


_BUTTON_MAP = {
    'A': NES_INPUT_A,
    'B': NES_INPUT_B,
    'SELECT': NES_INPUT_SELECT,
    'START': NES_INPUT_START,
    'UP': NES_INPUT_UP,
    'DOWN': NES_INPUT_DOWN,
    'LEFT': NES_INPUT_LEFT,
    'RIGHT': NES_INPUT_RIGHT,
    'NOOP': 0,
}


class JoypadSpace(gymnasium.ActionWrapper):
    """Wrapper to limit the action space to a subset of joystick combinations."""

    def __init__(self, env, actions):
        """
        Initialize a new JoypadSpace wrapper.

        Args:
            env: the environment to wrap
            actions: a list of lists of button names, e.g.
                [['NOOP'], ['right'], ['right', 'A']]

        Returns:
            None

        """
        super().__init__(env)
        self._actions = []
        self._action_meanings = []
        for action in actions:
            mask = 0
            for button in action:
                mask |= _BUTTON_MAP[button.upper()]
            self._actions.append(mask)
            self._action_meanings.append(' '.join(action))
        self.action_space = gymnasium.spaces.Discrete(len(self._actions))

    def action(self, act):
        """Map a discrete action to the original action space."""
        return self._actions[act]

    def get_action_meanings(self):
        """Return a list of action meanings."""
        return self._action_meanings
