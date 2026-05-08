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

### 命令行

`gymnasium_mariobros` 提供命令行界面，支持键盘操控或随机动作：

```shell
gymnasium_mariobros -e <环境 ID> -m <human 或 random>
```

- 默认 `-e` 为 `SuperMarioBros-v0`，`-m` 为 `human`
- `SuperMarioBrosRandomStages-*` 支持 `--stages/-S` 参数指定关卡子集，如 `-S 1-4 2-4 3-4 4-4`

## Environments

这些环境允许 3 次尝试（3 条命）通过游戏中的 32 个关卡。
环境只将有奖励的游戏画面帧发送给智能体；过场动画、加载画面等不会发送给智能体，
智能体也无法在这些时刻执行动作。如果过场动画无法通过修改 NES 内存跳过，
环境将阻塞 Python 进程直到模拟器准备好接受下一个动作。

| Environment                     | Game | ROM           | 说明                              | Screenshot |
|:--------------------------------|:-----|:--------------|:----------------------------------|:-----------|
| `SuperMarioBros-v0`             | SMB  | standard      | 原版画面，推荐使用                  | ![][v0]    |
| `SuperMarioBros-v1`             | SMB  | downsample    | 降采样画面                        | ![][v1]    |
| `SuperMarioBros-v2`             | SMB  | pixel         | 像素模式画面                      | ![][v2]    |
| `SuperMarioBros-v3`             | SMB  | rectangle     | 矩形模式画面                      | ![][v3]    |
| `SuperMarioBros2-v0`            | SMB2 | standard      | 失落关卡原版画面                    | ![][2-v0]  |
| `SuperMarioBros2-v1`            | SMB2 | downsample    | 失落关卡降采样画面                  | ![][2-v1]  |

[v0]: https://user-images.githubusercontent.com/2184469/40948820-3d15e5c2-6830-11e8-81d4-ecfaffee0a14.png
[v1]: https://user-images.githubusercontent.com/2184469/40948819-3cff6c48-6830-11e8-8373-8fad1665ac72.png
[v2]: https://user-images.githubusercontent.com/2184469/40948818-3cea09d4-6830-11e8-8efa-8f34d8b05b11.png
[v3]: https://user-images.githubusercontent.com/2184469/40948817-3cd6600a-6830-11e8-8abb-9cee6a31d377.png
[2-v0]: https://user-images.githubusercontent.com/2184469/40948822-3d3b8412-6830-11e8-860b-af3802f5373f.png
[2-v1]: https://user-images.githubusercontent.com/2184469/40948821-3d2d61a2-6830-11e8-8789-a92e750aa9a8.png

## 联系方式

Mail: 4933149@qq.com

## 请喝咖啡

![请喝咖啡](res/wechat.png)

