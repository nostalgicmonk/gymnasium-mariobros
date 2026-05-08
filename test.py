from gymnasium_mariobros.wrappers import JoypadSpace
import gymnasium_mariobros
from gymnasium_mariobros.actions import SIMPLE_MOVEMENT

env = gymnasium_mariobros.make('SuperMarioBros-v2', render_mode="human")
env = JoypadSpace(env, SIMPLE_MOVEMENT)

done = True
for step in range(5000):
    if done:
        state, info = env.reset()
    state, reward, terminated, truncated, info = env.step(env.action_space.sample())
    done = terminated or truncated

env.close()
