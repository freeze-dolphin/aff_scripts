from utils import *


def swap_side(x):
    if x == "-1.00":
        return "2.00"
    else:
        return "-1.00"


start = int(prompt_to_stderr("特效总起始时间 (int, ms): "))
end = int(prompt_to_stderr("特效总结束时间 (int, ms): "))
bpm = float(prompt_to_stderr("BPM (number): "))
length = float(prompt_to_stderr("每个箭头黑线的基准长度 (number): "))
perframetime = float(prompt_to_stderr("每个箭头表演的时间 (number): ")) / 60
side = int(prompt_to_stderr("特效表演的位置 (0, 1, 2; 分别代表左边、右边、两边都有): "))

side_ctl_n = 1
if side == 0:
    x_axis = "-1.00"
elif side == 1:
    x_axis = "2.00"
else:
    x_axis = "-1.00"
    side_ctl_n = 2

print("AudioOffset:0")
print("-")
print("timing(0,{:.2f},4.00);".format(bpm * length / perframetime))
print("timinggroup(){")
print("  timing(0,{:.2f},4.00);".format(bpm * length / perframetime))

r = (end - start) // perframetime

for side_ctl in range(side_ctl_n):
    for i in range(int(r + 1)):
        time = start + i * perframetime

        # 上边界
        print(
            "  arc({:.0f},{:.0f},{},{},s,{:.2f},{:.2f},0,none,true);".format(
                time + i,
                time + i + perframetime / 3,
                x_axis,
                x_axis,
                0.5625 + (i / r) * 0.8125,
                0.5625 + (i / r) * 0.8125,
            )
        )

        # 下边界
        print(
            "  arc({:.0f},{:.0f},{},{},s,{:.2f},{:.2f},0,none,true);".format(
                time + i,
                time + i + perframetime / 3,
                x_axis,
                x_axis,
                0.4375 - (i / r) * 0.8125,
                0.4375 - (i / r) * 0.8125,
            )
        )

        # 前半上
        print(
            "  arc({:.0f},{:.0f},{},{},s,{:.2f},{:.2f},0,none,true);".format(
                time + i,
                time + i + perframetime / 3,
                x_axis,
                x_axis,
                0.5625 + (i / r) * 0.8125,
                0.5,
            )
        )

        # 前半下
        print(
            "  arc({:.0f},{:.0f},{},{},s,{:.2f},{:.2f},0,none,true);".format(
                time + i,
                time + i + perframetime / 3,
                x_axis,
                x_axis,
                0.4375 - (i / r) * 0.8125,
                0.5,
            )
        )

        # 后半上
        print(
            "  arc({:.0f},{:.0f},{},{},s,{:.2f},{:.2f},0,none,true);".format(
                time + i + perframetime / 3,
                time + i + perframetime / 3 * 2,
                x_axis,
                x_axis,
                0.5625 + (i / r) * 0.8125,
                0.5,
            )
        )

        # 后半下
        print(
            "  arc({:.0f},{:.0f},{},{},s,{:.2f},{:.2f},0,none,true);".format(
                time + i + perframetime / 3,
                time + i + perframetime / 3 * 2,
                x_axis,
                x_axis,
                0.4375 - (i / r) * 0.8125,
                0.5,
            )
        )
    x_axis = swap_side(x_axis)

print("};")
