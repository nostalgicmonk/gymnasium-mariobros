"""A Gymnasium-compatible NES environment using cynes as the backend."""
import numpy as np
import gymnasium as gym
from gymnasium.spaces import Box, Discrete
from cynes import NES

SCREEN_HEIGHT = 240
SCREEN_WIDTH = 256
SCREEN_SHAPE = (SCREEN_HEIGHT, SCREEN_WIDTH, 3)
RAM_SIZE = 0x800


class _RAMProxy:
    """A proxy for NES RAM that syncs writes to the cynes emulator."""

    def __init__(self, nes):
        self._nes = nes
        self._data = np.zeros(RAM_SIZE, dtype=np.uint8)

    def __getitem__(self, address):
        if isinstance(address, slice):
            return self._data[address]
        return int(self._data[address])

    def __setitem__(self, address, value):
        if isinstance(address, slice):
            indices = range(*address.indices(RAM_SIZE))
            vals = value if hasattr(value, '__iter__') else [value] * len(indices)
            for idx, val in zip(indices, vals):
                self._data[idx] = val & 0xFF
                self._nes[idx] = int(val & 0xFF)
        else:
            self._data[address] = value & 0xFF
            self._nes[address] = int(value & 0xFF)

    def __len__(self):
        return RAM_SIZE

    def __array__(self, dtype=None):
        if dtype is not None:
            return self._data.astype(dtype)
        return self._data.copy()

    def __repr__(self):
        return repr(self._data)

    def sync_from_emulator(self):
        """Read all RAM from the emulator into the local cache."""
        for i in range(RAM_SIZE):
            self._data[i] = self._nes[i]


class NESEnv(gym.Env):
    """A Gymnasium environment wrapping the cynes NES emulator."""

    metadata = {
        'render_modes': ['human', 'rgb_array'],
        'render_fps': 60,
    }

    reward_range = (-float('inf'), float('inf'))

    observation_space = Box(
        low=0,
        high=255,
        shape=SCREEN_SHAPE,
        dtype=np.uint8,
    )

    action_space = Discrete(256)

    def __init__(self, rom_path, render_mode=None):
        """
        Create a new NES environment.

        Args:
            rom_path (str): the path to the ROM for the environment
            render_mode (str): the render mode, 'human' or 'rgb_array'

        Returns:
            None

        """
        super().__init__()
        self.render_mode = render_mode
        self._rom_path = rom_path
        self._nes = NES(rom_path)
        self._screen = np.zeros(SCREEN_SHAPE, dtype=np.uint8)
        self._ram_proxy = _RAMProxy(self._nes)
        self._ram_proxy.sync_from_emulator()
        self._backup_data = None
        self.done = False
        self._viewer = None

    @property
    def ram(self):
        """Return the RAM of the NES as a proxy that syncs writes."""
        return self._ram_proxy

    @property
    def screen(self):
        """Return the current screen as a numpy array."""
        return self._screen

    def _frame_advance(self, action):
        """
        Advance the emulator by one frame with the given action.

        This is a low-level method that does not trigger reward/done/info
        computation. It is used for internal operations like skipping frames.

        Args:
            action (int): the action to take (bitmap of button presses)

        Returns:
            None

        """
        self._nes.controller = int(action)
        frame = self._nes.step()
        if frame is not None:
            self._screen = np.array(frame, dtype=np.uint8).reshape(SCREEN_SHAPE)
        self._ram_proxy.sync_from_emulator()

    def _backup(self):
        """Backup the emulator state."""
        self._backup_data = self._nes.save()

    def _restore(self):
        """Restore the emulator state from backup."""
        if self._backup_data is not None:
            self._nes.load(self._backup_data)
            self._ram_proxy.sync_from_emulator()

    def _will_reset(self):
        """Handle any RAM hacking before a reset occurs."""
        pass

    def _did_reset(self):
        """Handle any RAM hacking after a reset occurs."""
        pass

    def _did_step(self, done):
        """
        Handle any RAM hacking after a step occurs.

        Args:
            done: whether the done flag is set to true

        Returns:
            None

        """
        pass

    def _get_reward(self):
        """Return the reward after a step occurs."""
        return 0

    def _get_done(self):
        """Return True if the episode is over, False otherwise."""
        return False

    def _get_info(self):
        """Return the info after a step occurs."""
        return {}

    def reset(self, *, seed=None, options=None):
        """
        Reset the state of the environment and returns an initial observation.

        Args:
            seed (int): an optional random number seed for the next episode
            options (dict): An optional options for resetting the environment.

        Returns:
            observation (np.ndarray): the initial observation
            info (dict): the info dictionary

        """
        super().reset(seed=seed)
        self._will_reset()
        self._restore()
        self._frame_advance(0)
        self._did_reset()
        self.done = False
        if self.render_mode == 'human':
            self.render()
        return self._screen.copy(), self._get_info()

    def step(self, action):
        """
        Run one frame of the NES and return the relevant observation data.

        Args:
            action (int): the action to take

        Returns:
            observation (np.ndarray): next frame
            reward (float): amount of reward returned
            terminated (bool): whether the episode has ended
            truncated (bool): whether the episode was truncated
            info (dict): contains auxiliary diagnostic information

        """
        if self.done:
            raise ValueError('cannot step in a done environment! call `reset`')
        self._frame_advance(action)
        reward = self._get_reward()
        done = self._get_done()
        info = self._get_info()
        self.done = done
        self._did_step(done)
        if self.render_mode == 'human':
            self.render()
        return self._screen.copy(), reward, done, False, info

    def render(self):
        """Render the environment."""
        if self.render_mode == 'rgb_array':
            return self._screen.copy()
        elif self.render_mode == 'human':
            try:
                import pygame
                if self._viewer is None:
                    pygame.init()
                    self._viewer = pygame.display.set_mode(
                        (SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2)
                    )
                    pygame.display.set_caption('NES')
                    self._clock = pygame.time.Clock()
                pygame.event.pump()
                surface = pygame.surfarray.make_surface(
                    self._screen.transpose(1, 0, 2)
                )
                surface = pygame.transform.scale(
                    surface, (SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2)
                )
                self._viewer.blit(surface, (0, 0))
                pygame.display.flip()
                self._clock.tick(self.metadata['render_fps'])
            except ImportError:
                pass

    def close(self):
        """Close the environment."""
        if self._viewer is not None:
            try:
                import pygame
                pygame.quit()
            except ImportError:
                pass
            self._viewer = None
        del self._nes
        self._nes = None

    def get_keys_to_action(self):
        """Return the dictionary of keyboard keys to actions."""
        return {}

    def get_action_meanings(self):
        """Return a list of action meanings."""
        return [f'{i}' for i in range(256)]
