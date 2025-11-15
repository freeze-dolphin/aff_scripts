from pathlib import Path
from posixpath import pardir
from random import shuffle


def split_list_by_percent(list, param_str):
    """
    Split param examples:
    - "" ;              [100]
    - "15" ;            [15, 85]
    - "15,20" ;         [15, 20, 65]
    - "10,20,30" ;      [10, 20, 30, 40]
    - "10,20,30,40" ;   sum >= 100, [10, 20, 30, 40]
    """
    if not list:
        return []

    n = len(list)

    if not param_str or param_str.strip() == "":
        return [list.copy()]

    try:
        parts = [int(x.strip()) for x in param_str.split(",") if x.strip()]
    except ValueError:
        raise ValueError()

    if not parts:
        return [list.copy()]

    total = sum(parts)

    if total >= 100:
        ratios = parts
    else:
        ratios = parts + [100 - total]

    segments = []
    start = 0
    for ratio in ratios:
        length = round(n * ratio / 100.0)
        length = max(0, min(length, n - start))
        end = start + length

        segments.append(list[start:end])
        start = end

    if start < n:
        segments[-1] = segments[-1] + list[start:]

    return segments


def main():
    aff_input = Path(input("Path to input aff: "))
    aff_output = aff_input.parent / (aff_input.name.removesuffix(".aff") + "_split.aff")

    split_parameter = input("Split parameter: ")

    bpm = float(input("BPM: "))

    lines = [[]]

    with open(str(aff_input), "r") as aff_input_f:
        index = -1

        for line in aff_input_f:
            stripped = line.strip()
            if stripped.startswith("timinggroup"):
                index += 1

            if stripped.startswith("arc"):
                lines[index].append(stripped)

            if stripped.startswith("};"):
                shuffle(lines[index])
                lines.append([])

    lines = lines[:-1]

    with open(aff_output, "w") as aff_output_f:
        for section in lines:
            for tg in split_list_by_percent(section, split_parameter):
                aff_output_f.write(f"timinggroup(noinput){{\n  timing(0,{bpm},4.00);\n")
                for cmd in tg:
                    aff_output_f.write(f"  {cmd}\n")
                aff_output_f.write("};\n")


if __name__ == "__main__":
    main()
