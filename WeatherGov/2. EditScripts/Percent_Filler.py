import regex as re

def round_school(x):
    i, f = divmod(x, 1)
    return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))

def convertpercentage(dataline):
    precip = re.search(r'precipPotential.max:(.*?) ', dataline)
    maxnumber = precip.group(1)
    maxnumber = (round_school(float(maxnumber) / 10)) * 10
    if maxnumber < 10:
        maxnumber = 10
    if maxnumber > 50:
        maxnumber = 50
    return str(maxnumber)