import sys


def eprint(*_args, **kwargs):
    print(*_args, file=sys.stderr, **kwargs)


def prompt_to_stderr(prompt):
    print(prompt, file=sys.stderr, end="\n")
    return input()


def gen_trace(t, a, b):
    """
    t: 时间, ms
    a: 二元组, 分别表示起始和结束时的横坐标
    b: 二元组, 分别表示起始和结束时的纵坐标

    生成一条直线黑线
    """
    return f"  arc({t:.0f},{t:.0f},{a[0]:.2f},{b[0]:.2f},s,{a[1]:.2f},{b[1]:.2f},0,none,true);"


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
