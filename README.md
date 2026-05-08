# gymnasium-mariobros

[![PyPI version](https://badge.fury.io/py/gymnasium-mariobros.svg)](https://pypi.org/project/gymnasium-mariobros/)
[![Python Version](https://img.shields.io/pypi/pyversions/gymnasium-mariobros.svg)](https://python.org)
[![License](https://img.shields.io/pypi/l/gymnasium-mariobros.svg)](LICENSE)

![Mario](https://user-images.githubusercontent.com/2184469/40949613-7542733a-6834-11e8-895b-ce1cc3af9dbb.gif)

A [Gymnasium](https://github.com/Farama-Foundation/Gymnasium) environment for
Super Mario Bros. & Super Mario Bros. 2 (Lost Levels) on The Nintendo
Entertainment System (NES) using
[the cynes emulator](https://github.com/Youlixx/cynes).

## 安装

使用 pip 安装：

```shell
pip install gymnasium-mariobros
```

## 使用方法

使用前必须先 `import gymnasium_mariobros`，因为 gymnasium 环境在导入时注册。
默认情况下，`gymnasium_mariobros` 环境使用完整的 256 个 NES 离散动作空间。
为了缩减动作空间，`gymnasium_mariobros.actions` 提供了三个动作列表
（`RIGHT_ONLY`、`SIMPLE_MOVEMENT` 和 `COMPLEX_MOVEMENT`）供 `JoypadSpace` 使用。

```python
from gymnasium_mariobros.wrappers import JoypadSpace
import gymnasium_mariobros
from gymnasium_mariobros.actions import SIMPLE_MOVEMENT

# 创建环境，render_mode="human" 弹窗显示游戏画面
env = gymnasium_mariobros.make('SuperMarioBros-v2', render_mode="human")
# JoypadSpace 将 256 个 NES 动作缩减为指定的动作子集
env = JoypadSpace(env, SIMPLE_MOVEMENT)

done = True
for step in range(5000):
    if done:
        state, info = env.reset()
    state, reward, terminated, truncated, info = env.step(env.action_space.sample())
    done = terminated or truncated

env.close()
```

- `gymnasium_mariobros.make` 是 `gymnasium.make` 的别名
- `render_mode="human"` 弹窗显示游戏画面，`"rgb_array"` 返回画面数组（用于录制/训练），`None` 不渲染
- 训练时建议设为 `render_mode="rgb_array"` 或不传（默认 `None`）以提升速度

## 联系方式

Mail: 4933149@qq.com

## 请喝咖啡

![请喝咖啡](res/wechat.png)

