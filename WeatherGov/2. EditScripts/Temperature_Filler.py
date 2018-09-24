import regex as re
import os
import itertools
import operator
import sys
from collections import Counter
from numpy.random import choice

def converttemperature(dataline):
    datachoice = choice(['high near', 'low around', 'steady temperature around'], 1, p=[0.4633248159, 0.5329174808, 0.0037577033])[0]
    if datachoice == 'high near':
        temperature = re.search(r"temperature\.max\:(.*?)\s", dataline).group(1)
    elif datachoice == 'low around':
        temperature = re.search(r"temperature\.min\:(.*?)\s", dataline).group(1)
    elif datachoice == 'steady temperature around':
        temperature = re.search(r"temperature\.mean\:(.*?)\s", dataline).group(1)
    return (datachoice, temperature)

def fallingrising(dataline, datachoice=None):
    if datachoice == None:
        datachoice = choice(['falling', 'rising'], 1, p=[0.75, 0.25])[0]
    if datachoice == 'falling':
        temperature = re.search(r"temperature\.min\:(.*?)\s", dataline).group(1)
        return ('falling', temperature)
    elif datachoice == 'rising':
        temperature = re.search(r"temperature\.max\:(.*?)\s", dataline).group(1)
        return ('rising', temperature)

def exceptiontemperature(dataline, previoustemplates):
    if 'high near' in previoustemplates:
        plist = [0.5329174808, 0.0037577033]
        plist = [float(i) / sum(plist) for i in plist]
        datachoice = choice(['low around', 'steady temperature around'], 1,
                            p=plist)[0]
    elif 'low around' in previoustemplates:
        plist = [0.4633248159, 0.0037577033]
        plist = [float(i) / sum(plist) for i in plist]
        datachoice = choice(['high near', 'steady temperature around'], 1,
                            p=plist)[0]
    else:
        plist = [0.4633248159, 0.5329174808]
        plist = [float(i) / sum(plist) for i in plist]
        datachoice = choice(['high near', 'low around'], 1,
                            p=plist)[0]
    if datachoice == 'high near':
        temperature = re.search(r"temperature\.max\:(.*?)\s", dataline).group(1)
    elif datachoice == 'low around':
        temperature = re.search(r"temperature\.min\:(.*?)\s", dataline).group(1)
    elif datachoice == 'steady temperature around':
        temperature = re.search(r"temperature\.mean\:(.*?)\s", dataline).group(1)
    return temperature