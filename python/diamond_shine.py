GLOBAL_OFFSET = 219720
DURATION = 1400


def do_shine(indent, n, timing_offset):
    t = int(n * DURATION) + timing_offset
    if t > GLOBAL_OFFSET:
        return
    alpha = 255 if n % 2 == 0 else 0
    print(indent + f"scenecontrol({t},bgshow,{t + DURATION},\"diamond-shine.png\",{alpha},0);")


if __name__ == "__main__":
    print("timinggroup(noinput){")
    offset = 0

    for i in range(0, GLOBAL_OFFSET, DURATION):
        do_shine("  ", i / DURATION, offset)
        offset += 1

    print("};")
