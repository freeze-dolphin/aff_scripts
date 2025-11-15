import sys
import pandas as pd
import re
from decimal import Decimal

# Configuration
 
LINE_SEPERATOR = "\r\n"
FLOAT_FORMATOR = "{:.2f}"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def to_type(_s: str, _dtype: str): 
    return eval(f"{_dtype}({_s})")


filepath = input("aff file path: ")

if not filepath.endswith(".aff"):
    print("\n\033[31mERROR: only aff files are accepted!\033[0m")
    sys.exit(-1)

with open(filepath, 'r') as f:
    lines = f.readlines()

trst = []

while not lines[0].rstrip().startswith("timing("):
    trst.append(lines.pop(0).rstrip())
else:
    trst.append(lines.pop(0).rstrip())

rdata = (list(map(lambda x: re.split(r'[(),]', x.strip()), lines)))

# validation
_r_validator_procedure = ""
_r_validator_length = -1
warn_validation_procedure = False
warn_validation_length = False
for i in range(len(rdata)):
    _r = rdata[i]
    # if _r[0] == "":
    #     rdata[i][0] = "note"
    if _r_validator_procedure == "":
        _r_validator_procedure = _r[0]
    else:
        if _r_validator_procedure != _r[0] and not warn_validation_procedure:
            warn_validation_procedure = True

    if _r_validator_length == -1:
        _r_validator_length = len(_r)
    else:
        if _r_validator_length != len(_r) and not warn_validation_length:
            warn_validation_length = True

df = pd.DataFrame(rdata)
df.rename(columns={0: "Procedure"}, inplace=True)
print(df)

print("\n\033[34m- You can use Python's slicing grammar in below\033[0m")
print("\033[34m- You can use COMMA to make multiple selection\033[0m\n")

if warn_validation_procedure:
    print("\033[33mWARNING: various procedures are found in this aff!\033[0m")

if warn_validation_procedure:
    print("\033[33mWARNING: parameters not aligned in this aff!\033[0m")

if warn_validation_procedure or warn_validation_length:
    print()

# Selection

total_selection = None

while True:
    try:
        col_selections = input("Select the column(s) you want to offset on: ").split(",")
        if "Procedure" in col_selections:
            print(f"\033[33mWARNING: the Procedure column cannot be selected\033[0m")
            continue
        total_selection = pd.DataFrame()
        for col_selection in col_selections:
            selection = eval(f"df.iloc[:, {col_selection}]")
            total_selection = pd.concat([total_selection, selection], axis=1, sort=False)
        print(total_selection)
        confirming = input("Ok? (Y/n): ").lower()
        if confirming == "y":
            break
    except Exception as e:
        print(f"\033[33mWARNING: invalid selector! {str(e)}\033[0m")
        continue

# Process

if total_selection is None:
    print("\n\033[31mERROR: nothing is selected!\033[0m")
    sys.exit(-2)

roffset = input(f"Offset (need {len(total_selection.columns)}): ").split(",")
if len(roffset) != len(total_selection.columns):
    print("\n\033[31mERROR: offset doesn't match your selection!\033[0m")
    sys.exit(-1)

for i in range(len(total_selection.columns)):
    col = total_selection.columns[i]
    sample = df.at[0, col]
    print(sample)
    if re.match(r'\d+\.\d+', sample):
        dtype = "float"
    else:
        dtype = "int"
    for j in range(len(df)):
        if dtype == "float":
            df.at[j, col] = FLOAT_FORMATOR.format(Decimal(df.at[j, col]) + Decimal(roffset[i]))
        else:
            df.at[j, col] = str(Decimal(df.at[j, col]) + Decimal(roffset[i]))

for j in range(len(df)):
    sline = df.iloc[j].to_list()
    tmp = ""
    need_comma = False
    for k in range(len(sline)):
        if k == 0:
            tmp += f"{sline[0]}("
        elif k != len(sline) - 1:
            if need_comma:
                tmp += ","
            tmp += sline[k]
            need_comma = True
        else:
            tmp += ");"
    trst.append(tmp)

rst = LINE_SEPERATOR.join(trst)

print(rst)

new_filepath = filepath.replace(".aff", ".offset.aff")

with open(new_filepath, "w") as f:
    f.write(rst)

print(f"\n\033[32mResult has been written to {new_filepath}\033[0m")
