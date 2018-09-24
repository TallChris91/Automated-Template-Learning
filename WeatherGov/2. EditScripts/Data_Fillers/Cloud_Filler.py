import regex as re
import os
import itertools
import operator
import sys
from collections import Counter
from numpy.random import choice

currentpath = os.getcwd()


def most_common(L):
    # get an iterable of (item, iterable) pairs
    SL = sorted((x, i) for i, x in enumerate(L))
    # print 'SL:', SL
    groups = itertools.groupby(SL, key=operator.itemgetter(0))

    # auxiliary function to get "quality" for an item
    def _auxfun(g):
        item, iterable = g
        count = 0
        min_index = len(L)
        for _, where in iterable:
            count += 1
            min_index = min(min_index, where)
        # print 'item %r, count %r, minind %r' % (item, count, min_index)
        return count, -min_index

    # pick the highest-count/earliest item
    return max(groups, key=_auxfun)[0]


def average(input):
    newinput = [x for x in (x.split("-") for x in input)]
    newinput = [int(item) for sublist in newinput for item in sublist]
    mean = sum(newinput) / float(len(newinput))
    return mean


def convertclouds(dataline):
    # Clee-eeeewd become a squeeeeeer sheep clewwwd https://www.youtube.com/watch?v=KNYo69XiDfA
    # Regex from the first 'skyCover' mention until the last skyCover mention, and the part after the last skyCover mention until the whitespace
    regex = re.compile(r"skyCover.mode-bucket(.*?):(.*?)\s")
    cloudamount = re.findall(regex, dataline)
    # Only retrieve the relevant part (the part after the colon)
    cloudamount = [v[1] for v in cloudamount]
    if len(cloudamount) > 0:
        # Use the most_common function to get the most frequent cloud value, which we will say determines the mentioned amount of clouds
        mostfrequent = most_common(cloudamount)
        return mostfrequent

def graduallybecoming(dataline):
    # Clee-eeeewd become a squeeeeeer sheep clewwwd https://www.youtube.com/watch?v=KNYo69XiDfA
    # Regex from the first 'skyCover' mention until the last skyCover mention, and the part after the last skyCover mention until the whitespace
    '''
    regex = re.compile(r"skyCover(?s:.*)skyCover(.*?)\s")
    match = re.search(regex, dataline)
    cloudpart = None
    try:
        cloudpart = match.group()
    except AttributeError:
        ''
    if cloudpart:
    '''
    # Get the values that indicate the amount of clouds
    regex = re.compile(r"skyCover.mode-bucket(.*?):(.*?)\s")
    cloudamount = re.findall(regex, dataline)
    # Only retrieve the relevant part (the part after the colon)
    cloudamount = [v[1] for v in cloudamount]
    if len(cloudamount) > 0:
        # First part always assumes high cloudiness (50-75 or 75-100)
        if (cloudamount[0] == '50-75') or (cloudamount[0] == '75-100'):
            datachoice1 = cloudamount[0]
        elif (cloudamount[1] == '50-75') or (cloudamount[1] == '75-100'):
            datachoice1 = cloudamount[1]
        else:
            datachoice1 = cloudamount[0]
        # Second part is either 0-25 or 25-50
        # Let's look at the final time point to determine what the weather becomes
        if (cloudamount[-1] == '0-25') or (cloudamount[-1] == '25-50'):
            datachoice2 = cloudamount[-1]
        # If the final point didn't give the desired results, let's look at the second to last part
        elif (cloudamount[-2] == '0-25') or (cloudamount[-2] == '25-50'):
            datachoice2 = cloudamount[-2]
        else:
            datachoice2 = cloudamount[-1]

        return datachoice1, datachoice2