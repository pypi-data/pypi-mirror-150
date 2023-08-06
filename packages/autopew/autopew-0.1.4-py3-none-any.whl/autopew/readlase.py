import re
import numpy as np
import pandas as pd

file = open("20180925_snowy_lines.lase", encoding="cp1252").read()  # .readlines()

lines = [i for i in re.split("[\n\r]", file) if i]

data = {}
for l in lines:
    if re.match(r"^\[.*\]$", l):
        section = l.replace("[", "").replace("]", "")
        data[section] = {}
    else:
        var, value = re.split("=", l, maxsplit=1)
        data[section][var] = value


def split_settings(s):
    x = re.split(r";", s)
    d = {k: v for (k, v) in [i.split("=") for i in x]}
    return d


def get_scandata(scandict):

    headers = scans["Header"].split(",")
    scannames = [i for i in scans.keys() if not i == "Header"]
    no_scans = len(scannames)
    df = pd.DataFrame(columns=headers, index=scannames)
    for s in scannames:
        scandata = re.findall(r'".+?"|[\w-]+', scans[s])
        df.loc[s, headers] = scandata

    for c in [
        "Description",
        "Vertex List",
        "Preablation Settings",
        "Ablation Settings",
    ]:
        df[c] = df[c].str.replace('"', "")

    df["Vertex List"] = (
        df["Vertex List"]
        .str.split(";")
        .apply(lambda x: np.array([i.split(",") for i in x]))
    )
    df["Preablation Settings"] = df["Preablation Settings"].apply(split_settings)
    df["Ablation Settings"] = df["Ablation Settings"].apply(split_settings)
    df["Data"] = df["Data"].apply(split_settings)
    return df


df = get_scandata(data['Scans'])
df.loc['Scan0', "Preablation Settings"]

scanfile = open("Autosaved Scan (2018-09-25 13-28-49).scancsv", encoding="cp1252").read()  # .readlines()
scanfilelines = [i for i in re.split("[\n\r]", scanfile) if i]

scanfiledict = {}
section = 'Scans'

for l in scanfilelines:
    var, value = re.split(",", l, maxsplit=1)
    scanfiledict[var] = value
get_scandata(scanfiledict)
df.columns
df.loc["Scan0", "Data"]
df.columns
