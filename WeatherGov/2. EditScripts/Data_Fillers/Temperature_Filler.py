import regex as re
import os
import itertools
import operator
import sys
from collections import Counter
from numpy.random import choice

def converttemperature(dataline):
    temperaturemax = re.search(r"temperature\.max\:(.*?)\s", dataline).group(1)
    temperaturemin = re.search(r"temperature\.min\:(.*?)\s", dataline).group(1)
    temperaturemean = re.search(r"temperature\.mean\:(.*?)\s", dataline).group(1)
    return ('minmeanmax', temperaturemin + '-' + temperaturemean + '-' + temperaturemax)

def fallingrising(dataline):
    temperature1 = re.search(r"temperature\.min\:(.*?)\s", dataline).group(1)
    temperature2 = re.search(r"temperature\.max\:(.*?)\s", dataline).group(1)
    return temperature1, temperature2
