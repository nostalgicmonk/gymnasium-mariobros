# gym-super-mario-bros

> **注意：** 本项目尚未发布 pip 包，仍在持续完善中。如需使用，请直接从源码安装。

[![BuildStatus][build-status]][ci-server]
[![PackageVersion][pypi-version]][pypi-home]
[![PythonVersion][python-version]][python-home]
[![Stable][pypi-status]][pypi-home]
[![Format][pypi-format]][pypi-home]
[![License][pypi-license]](LICENSE)

[build-status]: https://app.travis-ci.com/Kautenja/gym-super-mario-bros.svg?branch=master
[ci-server]: https://app.travis-ci.com/Kautenja/gym-super-mario-bros
[pypi-version]: https://badge.fury.io/py/gym-super-mario-bros.svg
[pypi-license]: https://img.shields.io/pypi/l/gym-super-mario-bros.svg
[pypi-status]: https://img.shields.io/pypi/status/gym-super-mario-bros.svg
[pypi-format]: https://img.shields.io/pypi/format/gym-super-mario-bros.svg
[pypi-home]: https://badge.fury.io/py/gym-super-mario-bros
[python-version]: https://img.shields.io/pypi/pyversions/gym-super-mario-bros.svg
[python-home]: https://python.org

![Mario](https://user-images.githubusercontent.com/2184469/40949613-7542733a-6834-11e8-895b-ce1cc3af9dbb.gif)

An [Gymnasium](https://github.com/Farama-Foundation/Gymnasium) environment for
Super Mario Bros. & Super Mario Bros. 2 (Lost Levels) on The Nintendo
Entertainment System (NES) using
[the cynes emulator](https://github.com/Youlixx/cynes).

## Installation

The preferred installation of `gym-super-mario-bros` is from `pip`:

```shell
pip install gym-super-mario-bros
```

## Usage

### Python

使用前必须先 `import gym_super_mario_bros`，因为 gymnasium 环境在运行时注册。
默认情况下，`gym_super_mario_bros` 环境使用完整的 256 个 NES 离散动作空间。
为了缩减动作空间，`gym_super_mario_bros.actions` 提供了三个动作列表
（`RIGHT_ONLY`、`SIMPLE_MOVEMENT` 和 `COMPLEX_MOVEMENT`）供 `JoypadSpace` 使用。
详见 [gym_super_mario_bros/actions.py](https://github.com/Kautenja/gym-super-mario-bros/blob/master/gym_super_mario_bros/actions.py)。

```python
from gym_super_mario_bros.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

# render_mode: "human" 弹窗显示游戏画面, "rgb_array" 返回画面数组(用于录制/训练), None 不渲染
env = gym_super_mario_bros.make('SuperMarioBros-v0', render_mode="human")
# JoypadSpace 将 256 个 NES 动作缩减为指定的动作子集
env = JoypadSpace(env, SIMPLE_MOVEMENT)

done = True
for step in range(5000):
    if done:
        # gymnasium 新 API: reset() 返回 (observation, info)
        state, info = env.reset()
    # gymnasium 新 API: step() 返回 (observation, reward, terminated, truncated, info)
    state, reward, terminated, truncated, info = env.step(env.action_space.sample())
    done = terminated or truncated

env.close()
```

**NOTE:** `gym_super_mario_bros.make` is just an alias to `gymnasium.make` for
convenience.

**NOTE:** `render_mode="human"` 时会自动渲染画面，无需手动调用 `env.render()`。
训练时建议设为 `render_mode="rgb_array"` 或不传(默认 `None`)以提升速度。

### Command Line

`gym_super_mario_bros` 提供命令行界面，支持键盘操控或随机动作：

```shell
gym_super_mario_bros -e <环境 ID> -m <human 或 random>
```

**NOTE:** 默认 `-e` 为 `SuperMarioBros-v0`，`-m` 为 `human`。

**NOTE:** `SuperMarioBrosRandomStages-*` 支持 `--stages/-S` 参数指定关卡子集，如 `-S 1-4 2-4 3-4 4-4`。

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

### Individual Stages

这些环境允许单次尝试（一条命）通过游戏的单个关卡。

使用模板

    SuperMarioBros-<world>-<stage>-v<version>

其中：

-   `<world>`: 世界编号，取值 {1, 2, 3, 4, 5, 6, 7, 8}
-   `<stage>`: 关卡编号，取值 {1, 2, 3, 4}
-   `<version>`: ROM 模式，取值 {0, 1, 2, 3}
    - 0: 原版 ROM（推荐）
    - 1: 降采样 ROM
    - 2: 像素 ROM
    - 3: 矩形 ROM

例如，要在降采样 ROM 上游玩 4-2 关卡，使用环境 ID `SuperMarioBros-4-2-v1`。

### Random Stage Selection

随机关卡选择环境会随机选择一个关卡，允许单次尝试通关。死亡后调用 `reset` 时会随机选择新关卡。
目前仅支持标准 Super Mario Bros.，不支持失落关卡。
使用时在 `SuperMarioBros` 后加上 `RandomStages`，例如使用原版 ROM 进行随机关卡选择：
`SuperMarioBrosRandomStages-v0`。可通过 `seed` 方法设置随机种子，如 `env.seed(222)`，
或直接在 `reset` 时传入 `reset(seed=222)`。

除了从全部 32 个原版关卡中随机选择外，还可以指定关卡子集来限制随机范围。
例如限制只从城堡关卡、水下关卡、地下关卡等中选取。

指定关卡子集的方式：创建一个关卡列表传给 `gym.make()` 函数。例如：

```python
gymnasium.make('SuperMarioBrosRandomStages-v0', stages=['1-4', '2-4', '3-4', '4-4'])
```

上面的示例将在每次 `reset` 时从 1-4、2-4、3-4、4-4 中随机选择一个关卡。

## Step

Info about the rewards and info returned by the `step` method.

### Reward Function

奖励函数假设游戏目标是在不死亡的前提下，尽可能快地向右移动。
奖励由三部分组成：

1.  _v_: 水平位移奖励（相邻两步的 x 坐标差值）
    -   即当前步的瞬时速度
    -   _v = x1 - x0_
        -   _x0_: 执行动作前的 x 坐标
        -   _x1_: 执行动作后的 x 坐标
    -   向右移动 ⇔ _v > 0_
    -   向左移动 ⇔ _v < 0_
    -   未移动 ⇔ _v = 0_
2.  _c_: 时间惩罚（游戏时钟的差值）
    -   防止智能体原地不动
    -   _c = c0 - c1_
        -   _c0_: 执行动作前的时钟值
        -   _c1_: 执行动作后的时钟值
    -   时钟未走 ⇔ _c = 0_
    -   时钟走动 ⇔ _c < 0_
3.  _d_: 死亡惩罚
    -   鼓励智能体避免死亡
    -   存活 ⇔ _d = 0_
    -   死亡 ⇔ _d = -15_

_r = v + c + d_

奖励被裁剪到 _(-15, 15)_ 范围内。

### `info` dictionary

The `info` dictionary returned by the `step` method contains the following
keys:

| Key        | Type   | Description
|:-----------|:-------|:------------------------------------------------------|
| `coins`    | `int`  | 已收集金币数
| `flag_get` | `bool` | 是否到达旗杆或斧头
| `life`     | `int`  | 剩余生命数，即 _{3, 2, 1}_
| `score`    | `int`  | 累计游戏得分
| `stage`    | `int`  | 当前关卡，即 _{1, ..., 4}_
| `status`   | `str`  | Mario 状态，即 _{'small', 'tall', 'fireball'}_
| `time`     | `int`  | 剩余时间
| `world`    | `int`  | 当前世界，即 _{1, ..., 8}_
| `x_pos`    | `int`  | Mario 的 _x_ 坐标（距左侧距离）
| `y_pos`    | `int`  | Mario 的 _y_ 坐标（距底部距离）

## Citation

Please cite `gym-super-mario-bros` if you use it in your research.

```tex
@misc{gym-super-mario-bros,
  author = {Christian Kauten},
  howpublished = {GitHub},
  title = {{S}uper {M}ario {B}ros for {G}ymnasium},
  URL = {https://github.com/Kautenja/gym-super-mario-bros},
  year = {2018},
}
```
