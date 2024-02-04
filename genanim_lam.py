import math
from utils import eprint

_SQRT = math.sqrt
_SIN = math.sin
_COS = math.cos

_PI = 3.14159265
_HALF_PI = 1.57079633

NOTE_OFFSET = 150000
BPM = 175
FRAME_COUNT = 50


def ease_linear(x):
    return x


def ease_in_cubic(x):
    return x * x * x


def ease_out_cubic(x):
    return 1 - pow(1 - x, 3)


def ease_in_sine(x):
    return 1 - _COS(x * _HALF_PI)


def ease_out_sine(x):
    return _SIN(x * _HALF_PI)


def ease_out_quad(x: float) -> float:
    return 1 - (1 - x) * (1 - x)


def ease_in_expo(x: float) -> float:
    return 0 if x == 0 else math.pow(2, 10 * x - 10)


def ease_in_out_back(x):
    c1 = 1.70158
    c2 = c1 * 1.525
    if x < 0.5:
        return (2 * x ** 2 * ((c2 + 1) * 2 * x - c2)) / 2
    else:
        return ((2 * x - 2) ** 2 * ((c2 + 1) * (2 * x - 2) + c2) + 2) / 2


def ease_out_bounce(x):
    n1 = 7.5625
    d1 = 2.75
    if x < 1 / d1:
        return n1 * x * x
    elif x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + 0.75
    elif x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + 0.9375
    else:
        x -= 2.625 / d1
        return n1 * x * x + 0.984375


def calc_pos(a, b, op):
    """
    a: 二元组
    b: 数字, 用于对 a 进行修改

    函数接受两个二元组 a, b 和一个字符串类型的操作符 op
    将 a 中的每一项以 op 操作符与 b 中的每一项分别进行运算
    将两次运算的结果以二元组类型返回
    """
    if isinstance(b, (float, int)):
        b = (b, b)

    if op == "+":
        return a[0] + b[0], a[1] + b[1]
    elif op == "-":
        return a[0] - b[0], a[1] - b[1]
    elif op == "*":
        return a[0] * b[0], a[1] * b[1]
    elif op == "/":
        return a[0] / b[0], a[1] / b[1]


def genarc(t, a, b):
    """
    t: 时间, ms
    a: 二元组, 分别表示起始和结束时的横坐标
    b: 二元组, 分别表示起始和结束时的纵坐标

    生成一条直线黑线
    """
    return f"  arc({t:.0f},{t:.0f},{a[0]:.2f},{b[0]:.2f},s,{a[1]:.2f},{b[1]:.2f},0,none,true);"


def gentiming(t, b):
    """
    t: 时间, ms
    b: 数字, bpm

    生成一条 timing 指令, beats 为 999.00 推测用于控速
    """
    return f"  timing({t:.0f},{b:.2f},999.00);"


def min_positive_angle(angle):
    """
    计算给定角度的最小正角
    :param angle: 给定的角度，单位为度
    :return: 最小正角的度数
    """
    # 将角度转换为0-360度之间的等价角度
    angle %= 360

    return angle


def genarcs(t, r, x, y, angle=0, extra=0):
    """
    t: 时间, ms
    r: 数字, 半径, 从菱形的中心到四个角的距离
    x, y: 数字, 用于确定菱形的中心坐标

    生成一个组黑线, 构成一个菱形
    函数以 string list 返回, 用于和其他部分的 string list 拼接, 构成整个 timinggroup

    通过修改本函数可以实现图像效果的变换, 比如你想要用一个五角星, 修改本函数即可
    """
    l1 = r * math.cos(math.radians(angle))
    h1 = r * math.sin(math.radians(angle))
    l2 = r * math.cos(math.radians(60 - angle))
    h2 = r * math.sin(math.radians(60 - angle))
    l3 = r * math.cos(math.radians(angle - 30))
    h3 = r * math.sin(math.radians(angle - 30))
    l4 = r * math.sin(math.radians(angle + 18))
    h4 = r * math.cos(math.radians(angle + 18))
    l5 = r * math.sin(math.radians(min_positive_angle(18 - angle)))
    h5 = r * math.cos(math.radians(min_positive_angle(18 - angle)))
    l6 = r * math.sin(math.radians(min_positive_angle(36 - angle)))
    h6 = r * math.cos(math.radians(min_positive_angle(36 - angle)))
    l7 = r * math.sin(math.radians(min_positive_angle(36 + angle)))
    h7 = r * math.cos(math.radians(min_positive_angle(36 + angle)))

    if extra == 0:
        top = (x - l1, y + h1 * 2)
        right = (x + h1, y + l1 * 2)
        bottom = (x + l1, y - h1 * 2)
        left = (x - h1, y - l1 * 2)

        arcs = [
            genarc(t, top, right),
            genarc(t, right, bottom),
            genarc(t, bottom, left),
            genarc(t, left, top),
        ]
    elif extra == 1:
        top = (x - l1, y + h1 * 2)
        right = (x + l2, y + h2 * 2)
        left = (x - h3, y - l3 * 2)

        arcs = [
            genarc(t, top, right),
            genarc(t, right, left),
            genarc(t, left, top),
        ]
    elif extra == 2:
        left = (x - h4, y + l4 * 2)
        top = (x + h1, y + l1 * 2)
        right = (x + h5, y + l5 * 2)
        bottom_right = (x + l6, y - h6 * 2)
        bottom_left = (x - l7, y - h7 * 2)
        arcs = [
            genarc(t, left, top),
            genarc(t, top, right),
            genarc(t, right, bottom_right),
            genarc(t, bottom_right, bottom_left),
            genarc(t, bottom_left, left),
        ]
    else:
        arcs = []

    return arcs


def genframe(
        show_timing, hide_timing, radius, position, angle=0.0, extra_note_offset=0, extra=0
):
    """
    show_timing: 时间, ms, 此帧动画起始的时间
    hideTiming: 同上, 此帧动画消失的时间
    radius: 数字, 用于绘制菱形黑线函数的参数, 控制菱形黑线的半径
    position: 二元组, 被结构后用于绘制菱形黑线函数的参数, 用于确定菱形的中心坐标

    函数返回代表当前帧的一组指令, 其中包括 timing 和 arc, 用于被 timinggroup 指令包裹
    """
    show_timing = int(show_timing)
    hide_timing = int(hide_timing)
    _result = [
                  gentiming(0, BPM),
                  gentiming(show_timing - 1, -BPM * NOTE_OFFSET),
                  gentiming(show_timing, 0),
                  gentiming(hide_timing - 1, -BPM * NOTE_OFFSET),
                  gentiming(hide_timing, BPM),
              ] + genarcs(
        hide_timing + NOTE_OFFSET + extra_note_offset, radius, *position, angle, extra
    )
    return _result


def genfirstframe(hide_timing, radius, position):
    """
    三个参数同函数 genframe 中的解释

    此函数仅被调用一次, 用于
    """
    hide_timing = int(hide_timing)
    _result = [
                  gentiming(0, BPM),  # 这一条 gentiming 被注释, 参考 423 - 424 行的注解
                  gentiming(hide_timing - 1, -BPM * NOTE_OFFSET),
                  gentiming(hide_timing, BPM),
              ] + genarcs(hide_timing + NOTE_OFFSET, radius, *position, 0, 0)
    return _result


def genanim(
        timing,  # 时间
        duration,  # 过程
        start_radius,  # 起始时的动画半径
        end_radius,  # 结束时的动画半径
        start_position,  # 起始时的动画位置
        end_position,  # 结束时的动画位置
        easing_function,  # 缓动函数
        show_first_frame,  # 是否显示第一帧
        extra_note_offset,
        extra,
):
    """
    这个函数是整个程序的核心
    用于生成一次完整的动画
    """

    radius_diff = end_radius - start_radius  # 动画移动过程中的半径变化 Δr
    position_diff = calc_pos(
        end_position, start_position, "-"
    )  # 动画移动过程中变化的横纵坐标 (Δx, Δy)
    real_frame_count = int(FRAME_COUNT * (duration / 1000.0))  # 计算出需要处理多少帧后
    _result = []

    # 逐帧计算动画内容
    for i in range(real_frame_count):
        progress = i / (
                real_frame_count - 1.0
        )  # 区间 [0, 1] 的实数, 用于表示当前动画的过程
        radius = start_radius + radius_diff * ease_out_cubic(progress)
        _result.append("timinggroup(noinput){")  # 去掉了无效的 tg 参数
        position = calc_pos(
            start_position,
            calc_pos(
                position_diff,  # 原始 (Δx, Δy)
                easing_function(progress),
                "*",
                # 通过对过程应用缓动函数, 获取当前时间经过缓动函数计算后的 (Δx, Δy), 记作 (Δax, Δay), 缓动函数可以使动画更流畅, 符合美学, 这个 arc 指令中的 sosi,
                # sisi 概念类似但不完全一样
            ),
            "+",  # 使原始 (x, y) 两项分别加上经过缓动函数处理后的偏移量 (Δax, Δay) 的两项, 结果是为当前坐标 (cx, cy), 这个当前坐标在下一步用于生成当前帧动画内容
        )

        # 根据参数 showFirstFrame 判断是否显示第一帧, 此选项的作用稍后介绍
        if i == 0 and show_first_frame:
            _result += genfirstframe(timing, radius, position)
        else:
            nextprogress = (i + 1) / (real_frame_count - 1.0)
            _timing = timing + duration * progress
            _nextTiming = timing + duration * nextprogress
            _result += genframe(
                _timing,
                _nextTiming,
                radius,
                position,
                progress * 360,
                extra_note_offset,
                extra,
            )

        _result.append("};")
    return _result


result = []

# 开始时间, 结束时间, 开始半径, 结束半径, 开始坐标, 结束坐标, 缓动函数, 是否显示第一帧

t_st = list(range(700, 10000, 150))
t_dur = 1000

for _t in range(6):
    t_st[_t] += _t * 100
    eprint(t_st[_t])

args = [
    (t_st[0], t_dur, 0.0, 0.45, (0, 1), (1, 1), ease_out_sine, False, 10, 0),
    (t_st[1], t_dur, 0.0, 0.45, (0, 1), (1, 1), ease_out_sine, False, 20, 0),
    (t_st[2], t_dur, 0.0, 0.45, (0, 1), (1, 1), ease_out_sine, False, 30, 1),
    (t_st[3], t_dur, 0.0, 0.45, (0, 1), (1, 1), ease_out_sine, False, 40, 1),
    (t_st[4], t_dur, 0.0, 0.45, (0, 1), (1, 1), ease_out_sine, False, 50, 2),
    (t_st[5], t_dur, 0.0, 0.45, (0, 1), (1, 1), ease_out_sine, False, 60, 2),
    (t_st[0] + t_dur, 2000, 0.45, 0.3, (1, 1), (1, 1), ease_linear, False, 10, 0),
    (t_st[1] + t_dur, 2000, 0.45, 0.3, (1, 1), (1, 1), ease_linear, False, 20, 0),
    (t_st[2] + t_dur, 2000, 0.45, 0.3, (1, 1), (1, 1), ease_linear, False, 30, 1),
    (t_st[3] + t_dur, 2000, 0.45, 0.3, (1, 1), (1, 1), ease_linear, False, 40, 1),
    (t_st[4] + t_dur, 2000, 0.45, 0.3, (1, 1), (1, 1), ease_linear, False, 50, 2),
    (t_st[5] + t_dur, 2000, 0.45, 0.3, (1, 1), (1, 1), ease_linear, False, 60, 2),
]

PER_OFFSET = 5

for args in args:
    result += genanim(*args)

print("AudioOffset:0\n-")
print(gentiming(0, BPM).strip())

print("\n".join(result))
