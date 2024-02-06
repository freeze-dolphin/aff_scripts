import math
import random as rnd

import utils
from easing import *
from utils import gen_trace, calc_pos

# ------------------------------------------------------
# 基本参数
# ------------------------------------------------------

# 整首歌的长度
NOTE_OFFSET = 223709

# 控制整体速度
BPM = 130

# 帧数
FRAME_COUNT = 120


# ------------------------------------------------------
# 主程序
# ------------------------------------------------------

def gen_timing(t, b):
    return f"  timing({t:.0f},{b:.2f},999.00);"


def gen_arcs(t, _x, _y, _droplet_length, _overlapping, _radians):
    arcs = []

    delta_y = _droplet_length * math.cos(_radians)

    for _ in range(_overlapping):
        arcs.append(
            gen_trace(t, (_x - math.tan(_radians) * delta_y, _y - delta_y), (_x, _y))
        )

    return arcs


def gen_frame(
        show_timing, hide_timing, position, extra_note_offset, _droplet_length, _overlapping, _radians
):
    show_timing = int(show_timing)
    hide_timing = int(hide_timing)
    _result = [
                  gen_timing(0, BPM),
                  gen_timing(show_timing - 1, -BPM * NOTE_OFFSET - extra_note_offset),
                  gen_timing(show_timing, 0),
                  gen_timing(hide_timing - 1, -BPM * NOTE_OFFSET - extra_note_offset),
                  gen_timing(hide_timing, BPM),
              ] + gen_arcs(
        hide_timing + NOTE_OFFSET + extra_note_offset,
        *position,
        _droplet_length,
        _overlapping,
        _radians
    )
    return _result


def gen_anim(
        _timing,
        _duration,
        _start_position,
        _end_position,
        _easing_function,
        _extra_note_offset,
        _overlapping,
        _radians,
        _small_droplet_ratio,
        _small_droplet_length_rng,
        _large_droplet_length_rng
):
    position_diff = calc_pos(
        _end_position, _start_position, "-"
    )
    real_frame_count = int(FRAME_COUNT * (_duration / 1000.0))
    _result = []

    if rnd.random() < _small_droplet_ratio:
        droplet_length = rnd.uniform(*_small_droplet_length_rng)
    else:
        droplet_length = rnd.uniform(*_large_droplet_length_rng)

    for i in range(real_frame_count):
        progress = i / (
                real_frame_count - 1.0
        )

        nextprogress = (i + 1) / (real_frame_count - 1.0)
        _timing = _timing + _duration * progress
        _nextTiming = _timing + _duration * nextprogress

        if abs(_nextTiming - 205936) < 30:
            utils.eprint(_nextTiming)
            continue

        _result.append("timinggroup(noinput){")
        position = calc_pos(
            _start_position,
            calc_pos(
                position_diff,
                _easing_function(progress),
                "*",
            ),
            "+",
        )
        _result += gen_frame(
            _timing,
            _nextTiming,
            position,
            _extra_note_offset,
            droplet_length,
            _overlapping,
            _radians
        )

        _result.append("};")
    return _result


def gen_rain(_timings,
             _timing_step,
             _side_overlapping,
             _mid_overlapping,
             _x_left_rng,
             _x_right_rng,
             _x_mid_rng,
             _y_rng,
             _z_rng,
             _duration_rng,
             _radians,
             _easing_function,
             _small_droplet_ratio,
             _small_droplet_length_rng,
             _large_droplet_length_rng,
             _ground_y=0.0,
             _swap_start_and_end_position=False,
             ):
    """
    _timings: 下雨时间, 即动画生成的时间段
    _side_overlapping: 两边雨滴层数
    _mid_overlapping: 中间雨滴层数
    _x_left_rng: 左边下雨的 x 范围
    _x_right_rng: 右边下雨的 x 范围
    _x_mid_rng: 中间下雨的 x 范围
    _y_rng: 下雨的 y 范围 (定义天空)
    _z_rng: 下雨的 前后 z 范围
    _duration_rng: 每个雨滴的持续时间范围
    _radians: 雨滴倾斜角度的弧度制
    _easing_function: 缓动函数
    _small_droplet_ratio: 下小雨滴的概率
    _small_droplet_length_rng: 小雨滴的长度范围
    _large_droplet_length_rng: 大雨滴的长度范围
    _swap_start_and_end_position: 反转雨滴起落
    """

    timings = range(*_timings, _timing_step)

    _x_offset = math.tan(_radians) * (sum(_y_rng) / 2)
    _x_right_rng = tuple(map(lambda _x: _x + _x_offset, _x_right_rng))
    _x_left_rng = tuple(map(lambda _x: _x + _x_offset, _x_left_rng))
    _x_mid_rng = tuple(map(lambda _x: _x + _x_offset, _x_mid_rng))

    _result = []

    for timing in timings:
        overlapping = _side_overlapping
        if _x_mid_rng[0] != _x_mid_rng[1]:
            choice = rnd.randint(0, 2)

            if choice == 0:
                x = rnd.uniform(*_x_right_rng)
            elif choice == 1:
                x = rnd.uniform(*_x_left_rng)
            else:
                x = rnd.uniform(*_x_mid_rng)
                overlapping = _mid_overlapping
        else:
            choice = rnd.randint(0, 1)
            if choice == 0:
                x = rnd.uniform(*_x_right_rng)
            else:
                x = rnd.uniform(*_x_left_rng)

        y = rnd.uniform(*_y_rng)

        if _swap_start_and_end_position:
            _start_pos = (x - math.tan(_radians) * y, _ground_y)
            _end_pos = (x, y)
        else:
            _start_pos = (x, y)
            _end_pos = (x - math.tan(_radians) * y, _ground_y)

        _result += gen_anim(
            timing,
            rnd.randint(*_duration_rng),
            _start_pos,
            _end_pos,
            _easing_function,
            rnd.randint(*_z_rng),
            overlapping,
            _radians,
            _small_droplet_ratio,
            _small_droplet_length_rng,
            _large_droplet_length_rng)
    return _result


# ------------------------------------------------------
# 降雨参数
# ------------------------------------------------------

result = []

"""
75782-87320：黑线上升 [✔]
87320-90090：上升的黑线慢慢停止 [✔]

92397-95166：停止的黑线转为下雨 [✔]
95166-96090：停雨 [✔]

96090-98859：下雨（少量） [✔]
98859-103474：停雨 [✔]

103474-105320：下雨（少量） [✔]
105320-107166：停雨 [✔]

107166-108090：雨只下到一半停止下，没接触地面 [✔]
108090-109936：下雨（少量） [✔]
109936-110859：停雨 [✔]

110859-116859：下雨（微少量） [✔]
116859-118243：停雨 [✔]
118243-121936：下雨 [✔]

176859-205936: 一直下雨 []
"""

result += gen_rain(
    (75782, 89800),
    80,
    2,
    1,
    (-0.3, -1.0),
    (1.3, 2.0),
    (0, 0),
    (2.2, 2.2),
    (0, 2800),
    (173, 173),
    math.radians(0),
    ease_out_quad,
    1.0,
    (0.2, 0.35),
    (0, 0),
    _swap_start_and_end_position=True,
)

result += gen_rain(
    (92397 - 90, 95116 - 90),
    20,
    2,
    1,
    (-0.5, -1.0),
    (1.5, 2.0),
    (-0.5, 1.5),
    (2.2, 2.2),
    (0, 2800),
    (50, 50),
    math.radians(9),
    ease_linear,
    0.4,
    (0.1, 0.2),
    (0.5, 0.8),
)

result += gen_rain(
    (96090 - 90, 98759 - 90),
    60,
    1,
    1,
    (-0.5, -1.0),
    (1.5, 2.0),
    (-0.5, 1.5),
    (2.2, 2.2),
    (0, 2800),
    (50, 75),
    math.radians(4),
    ease_linear,
    0.5,
    (0.1, 0.2),
    (0.4, 0.6),
)

result += gen_rain(
    (103474 - 90, 105220 - 90),
    60,
    1,
    1,
    (-0.5, -1.0),
    (1.5, 2.0),
    (-0.5, 1.5),
    (2.2, 2.2),
    (0, 2800),
    (50, 75),
    math.radians(2),
    ease_linear,
    0.6,
    (0.1, 0.2),
    (0.4, 0.6),
)

result += gen_rain(
    (107166 - 90, 107940 - 150 - 90),
    30,
    2,
    1,
    (0, -0.8),
    (1, 1.8),
    (0, 1),
    (2.2, 2.2),
    (0, 2000),
    (100, 120),
    math.radians(4),
    ease_out_cubic,
    0.6,
    (0.1, 0.2),
    (0.3, 0.5),
    _ground_y=0.75
)

result += gen_rain(
    (108090 - 90, 109886 - 90),
    40,
    1,
    1,
    (-0.5, -1.0),
    (1.5, 2.0),
    (-0.5, 1.5),
    (2.2, 2.2),
    (0, 2800),
    (50, 50),
    math.radians(4),
    ease_linear,
    0.4,
    (0.1, 0.2),
    (0.4, 0.6),
)

result += gen_rain(
    (110859 - 90, 116779 - 90),
    90,
    1,
    1,
    (-0.5, -1.0),
    (1.5, 2.0),
    (-0.5, 1.5),
    (2.2, 2.2),
    (0, 2800),
    (60, 80),
    math.radians(2),
    ease_linear,
    0.4,
    (0.1, 0.2),
    (0.4, 0.6),
)

result += gen_rain(
    (118243 - 90, 121886 - 90),
    20,
    2,
    1,
    (-0.5, -1.0),
    (1.5, 2.0),
    (-0.5, 1.5),
    (2.2, 2.2),
    (0, 2800),
    (50, 50),
    math.radians(9),
    ease_linear,
    0.6,
    (0.1, 0.2),
    (0.5, 0.8),
)

result += gen_rain(
    (176859, 205936),
    70,
    2,
    1,
    (-0.5, -1.5),
    (1.5, 2.5),
    (-0.5, 1.5),
    (2.2, 2.2),
    (0, 1400),
    (50, 50),
    math.radians(43.09),
    ease_linear,
    0.6,
    (0.1, 0.2),
    (0.5, 0.8),
    _swap_start_and_end_position=True
)

print("AudioOffset:0\n-")
print(gen_timing(0, BPM).strip())
# print("scenecontrol(0,enwidencamera,1000.00,1);")

print("\n".join(result))
