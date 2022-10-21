import pandas as pd
from tqdm import tqdm

from enum import Enum

BARCODE_PATH = "./Barcode_extracted/Barcode.csv"
VERBOSE_FILES = """
./Barcode_extracted/220830_Ctrl_1_HiSeq_Verbose.csv
./Barcode_extracted/220830_Ctrl_2_HiSeq_Verbose.csv
./Barcode_extracted/220830_NRCH_1_HiSeq_Verbose.csv
./Barcode_extracted/220830_NRCH_2_HiSeq_Verbose.csv
./Barcode_extracted/220830_PEmax_1_HiSeq_Verbose.csv
./Barcode_extracted/220830_PEmax_2_HiSeq_Verbose.csv
"""


class Flags(Enum):
    OTHERS = -2
    UNEDITED = -1
    EDITED = 1


VERBOSE_FILES = VERBOSE_FILES[1:-1]  # removed '\n' on the head and tail

barcode_table = pd.read_csv(BARCODE_PATH)
files_to_investigate = VERBOSE_FILES.split("\n")


def editing_efficiency(x):
    cnts = x.value_counts()

    # Prime editing efficiency = (edited read / (edited + unedited read) * 100)
    try:
        return cnts["EDITED"] / (cnts["EDITED"] + cnts["UNEDITED"]) * 100
    except Exception as e:
        return 0.0  # No prime edits


def edited_cnt(x):
    try:
        return x.value_counts()["EDITED"]
    except KeyError:
        return int(0)


def unedited_cnt(x):
    try:
        return x.value_counts()["UNEDITED"]
    except KeyError:
        return int(0)


def others_cnt(x):
    try:
        return x.value_counts()["OTHERS"]
    except KeyError:
        return int(0)


dfs = []  # Save (file_name, df)
for file in tqdm(files_to_investigate):
    df = pd.read_csv(file).merge(barcode_table, how="left", on="Barcode")

    flags = []
    flag_reprs = []
    for idx, row in df.iterrows():  # Classifying the sequence
        candidate = row["Sequence"]
        if row["Unedited"] in candidate:
            flag = Flags.UNEDITED
        elif row["Edited"] in candidate:
            flag = Flags.EDITED
        else:
            flag = Flags.OTHERS
        flags.append(flag.value)
        flag_reprs.append(Flags(flag).name)

    df = pd.concat(
        [df, pd.DataFrame({"FLAGS": flags, "FLAG_REPRS": flag_reprs})], axis=1
    )

    grouped = df.groupby("Index").FLAG_REPRS.agg(
        ["count", edited_cnt, unedited_cnt, others_cnt, editing_efficiency]
    )
    grouped.to_csv(f"{file}+Classified.csv")
