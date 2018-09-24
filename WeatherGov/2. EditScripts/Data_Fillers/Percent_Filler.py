import regex as re

def convertpercentage(dataline):
    precipmin = re.search(r'precipPotential.min:(.*?) ', dataline).group(1)
    precipmean = re.search(r'precipPotential.mean:(.*?) ', dataline).group(1)
    precipmax = re.search(r'precipPotential.max:(.*?) ', dataline).group(1)
    return str(precipmin + '-' + precipmean + '-' + precipmax)