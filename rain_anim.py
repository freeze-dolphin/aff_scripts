import random as rnd

from easing import *
from utils import gen_trace, calc_pos

_SQRT = math.sqrt
_SIN = math.sin
_COS = math.cos

_PI = 3.14159265
_HALF_PI = 1.57079633

# ------------------------------------------------------
# 基本参数
# ------------------------------------------------------


NOTE_OFFSET = 150000
BPM = 175
FRAME_COUNT = 180

# 下雨的时间段
TIMING = (1000, 3000)

# 下雨的 y 坐标随机范围 (定义天空的 y 坐标)
Y_RNG = (2.0, 2.0)

# 下雨的前后随机范围 (0 是 判定平面, 1500 是判定平面往前推 1500ms)
Z_RNG = (0, 1500)

# 雨滴持续时间随机范围, 20ms 到 50ms 之间
DURATION_RNG = (20, 50)

# 下「小型雨滴」的概率
SMALL_DROPLET_RATIO = 0.45

# 「小型雨滴」的长度随机范围
SMALL_DROPLET_LENGTH_RNG = (0.1, 0.3)

# 「大型雨滴」的长度随机范围
LARGE_DROPLET_LENGTH_RNG = (0.5, 0.8)

# 每组雨滴的数量范围, 用于调整雨点密度
GROUP_COUNT_RNG = (1, 3)

# 两边的雨滴厚度 (叠层)
SIDE_OVERLAPPING = 3

# 中间的雨滴厚度 (叠层)
MID_OVERLAPPING = 1

# 雨点倾斜的弧度, 用 math.radians() 将角度转换成弧度制
# 正角是从右往左下
# 负角反之
RADIANS = math.radians(9)

# X 坐标的偏移量, 取平均
X_OFFSET = math.tan(RADIANS) * (sum(Y_RNG) / 2)

# 左侧下雨的 x 坐标范围
# calc_pos( (x, y), X_OFFSET, "+") 表示在 (x, y) 的基础上向右偏移 X_OFFSET
# 因为雨是倾斜的
X_LEFT_RNG = calc_pos((-0.5, -0.8), X_OFFSET, "+")

# 右侧下雨的 x 坐标范围
X_RIGHT_RNG = calc_pos((1.5, 1.8), X_OFFSET, "+")

# 中间下雨的 x 坐标范围
X_MID_RNG = calc_pos((-0.5, 1.5), X_OFFSET, "+")


# ------------------------------------------------------
# 主程序
# ------------------------------------------------------

def gen_timing(t, b):
    return f"  timing({t:.0f},{b:.2f},999.00);"


def gen_arcs(t, _x, _y, _droplet_length, _overlapping):
    arcs = []

    delta_y = _droplet_length * math.cos(RADIANS)

    for _ in range(_overlapping):
        arcs.append(
            gen_trace(t, (_x - math.tan(RADIANS) * delta_y, _y - delta_y), (_x, _y))
        )

    return arcs


def gen_frame(
        show_timing, hide_timing, position, extra_note_offset, _droplet_length, _overlapping
):
    show_timing = int(show_timing)
    hide_timing = int(hide_timing)
    _result = [
                  gen_timing(0, BPM),
                  gen_timing(show_timing - 1, -BPM * NOTE_OFFSET),
                  gen_timing(show_timing, 0),
                  gen_timing(hide_timing - 1, -BPM * NOTE_OFFSET),
                  gen_timing(hide_timing, BPM),
              ] + gen_arcs(
        hide_timing + NOTE_OFFSET + extra_note_offset,
        *position,
        _droplet_length,
        _overlapping
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
):
    position_diff = calc_pos(
        _end_position, _start_position, "-"
    )
    real_frame_count = int(FRAME_COUNT * (_duration / 1000.0))  # 计算出需要处理多少帧后
    _result = []

    if rnd.random() < SMALL_DROPLET_RATIO:
        droplet_length = rnd.uniform(*SMALL_DROPLET_LENGTH_RNG)
    else:
        droplet_length = rnd.uniform(*LARGE_DROPLET_LENGTH_RNG)

    for i in range(real_frame_count):
        progress = i / (
                real_frame_count - 1.0
        )
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

        nextprogress = (i + 1) / (real_frame_count - 1.0)
        _timing = _timing + _duration * progress
        _nextTiming = _timing + _duration * nextprogress
        _result += gen_frame(
            _timing,
            _nextTiming,
            position,
            _extra_note_offset,
            droplet_length,
            _overlapping
        )

        _result.append("};")
    return _result


timings = range(*TIMING, 20)

result = []

extra_offset = 0

for timing in timings:
    choice = rnd.randint(0, 2)
    overlapping = SIDE_OVERLAPPING

    if choice == 0:
        x = rnd.uniform(*X_RIGHT_RNG)
    elif choice == 1:
        x = rnd.uniform(*X_LEFT_RNG)
    else:
        x = rnd.uniform(*X_MID_RNG)
        overlapping = MID_OVERLAPPING

    y = rnd.uniform(*Y_RNG)

    result += gen_anim(
        timing,
        rnd.randint(*DURATION_RNG),
        (x, y),
        (x - math.tan(RADIANS) * y, 0),
        ease_linear,
        rnd.randint(*Z_RNG),
        overlapping)

PER_OFFSET = 5

print("AudioOffset:0\n-")
print(gen_timing(0, BPM).strip())

print("\n".join(result))
