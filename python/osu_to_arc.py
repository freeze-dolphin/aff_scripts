import math
import re
import sys

import utils


# --------------------------------------------------------------
# PARSING
# --------------------------------------------------------------

def extract_title(_s):
    pattern = r'\[(.*?)\]'

    match = re.search(pattern, _s)

    if match:
        return match.group(1)
    else:
        return None


def get_column_count(_line):
    pattern = r'CircleSize:\s*(\d+)'
    match = re.search(pattern, _line)
    if match:
        return match.group(1)
    else:
        return None


timingpoints = []
hitobjects = []

part_timingpoints = False
part_hitobjects = False
part_columncnt = False

fname = utils.prompt_to_stderr("path to .osu file: ")
with open(fname, "r") as f_osu:
    for line in f_osu:
        line = line.strip()
        if line == "":
            continue

        title = extract_title(line)

        if title is not None:
            if title == "TimingPoints":
                part_timingpoints = True
                part_hitobjects = False
            elif title == "HitObjects":
                part_hitobjects = True
                part_timingpoints = False
            else:
                part_timingpoints = False
                part_hitobjects = False
        else:
            if not part_columncnt:
                COLUMN_COUNT = get_column_count(line)
                if COLUMN_COUNT is not None:
                    part_columncnt = True
            else:
                if part_timingpoints:
                    timingpoints.append(line.split(","))
                elif part_hitobjects:
                    hitobjects.append(line.split(","))

# utils.eprint(timingpoints)
# utils.eprint(hitobjects)
# utils.eprint(COLUMN_COUNT)

COLUMN_COUNT = int(COLUMN_COUNT)

#if len(timingpoints) == 0 or len(hitobjects) == 0:
#    utils.eprint("[E] Unable to parse beatmap")
#    sys.exit(1)


# --------------------------------------------------------------
# GENERATING
# --------------------------------------------------------------

def gen_timing(_t: int, _bpm: float, _beats: float) -> str:
    return f"timing({_t:d},{_bpm:.2f},{_beats:.2f});"


def gen_note(_t: int, _lane: int) -> str:
    return f"({_t:d},{_lane:d});"


def gen_hold(_t1: int, _t2: int, _lane: int) -> str:
    return f"hold({_t1:d},{_t2:d},{_lane:d});"


def calc_bpm(_timingpoint) -> float:
    return 1 / float(_timingpoint[1]) * 1000 * 60


def calc_lane(_hitobject) -> int:
    _lane = math.floor(int(_hitobject[0]) * int(COLUMN_COUNT) / 512)
    if COLUMN_COUNT == 6:
        return _lane
    elif COLUMN_COUNT == 4:
        return _lane + 1
    else:
        utils.eprint(f"[E] Unsupported column count: {COLUMN_COUNT:d}")
        sys.exit(1)


def get_type(_hitobject) -> str:
    # hold - 9841:0:0:0:0:
    # note -      0:0:0:0:
    _tmp = _hitobject[5].split(":")
    if len(_tmp) == 5:
        return "note"
    elif len(_tmp) == 6:
        return "hold"
    else:
        return ""


def get_note_time(_hitobject) -> int:
    return int(float(_hitobject[2]))


def get_hold_time(_hitobject) -> (int, int):
    return int(float(_hitobject[2])), int(float(_hitobject[5].split(":")[0]))

base_timing = int(float(timingpoints[0][0]))

result = [f"AudioOffset:{base_timing}", "-"]

timingpoint_inherit = None

for timingpoint in timingpoints:
    if timingpoint[6] == "1":
        timingpoint_inherit = timingpoint
        result.append(gen_timing(
            int(float(timingpoint[0])) - base_timing,
            calc_bpm(timingpoint),
            float(timingpoint[2])
        ))
    else:
        result.append(gen_timing(
            int(timingpoint[0]) - base_timing,
            calc_bpm(timingpoint_inherit),
            float(timingpoint_inherit[2])
        ))

for hitobject in hitobjects:
    note_type = get_type(hitobject)

    if note_type == "note":
        result.append(
            gen_note(get_note_time(hitobject) - base_timing,
                     calc_lane(hitobject))
        )
    elif note_type == "hold":
        t1, t2 = get_hold_time(hitobject)
        result.append(
            gen_hold(t1 - base_timing,
                     t2,
                     calc_lane(hitobject))
        )

# --------------------------------------------------------------
# OUTPUTTING
# --------------------------------------------------------------

print("\n".join(result))
