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
        if mostfrequent == '0-25':
            datachoice = list(choice(['mostly clear', 'sunny', 'clear'], 1, p=[0.40498243372, 0.52698818268, 0.06802938358]))[0]
        if mostfrequent == '25-50':
            datachoice = list(choice(['mostly sunny', 'partly cloudy', 'increasing clouds'], 1, p=[0.47310320658, 0.41422814088, 0.11266865253]))[0]
        if mostfrequent == '50-75':
            datachoice = list(choice(['mostly cloudy', 'partly sunny'], 1, p=[0.7068303914, 0.29316960859]))[0]
        if mostfrequent == '75-100':
            datachoice = 'cloudy'
        return datachoice

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
        if cloudamount[0] == '50-75':
            datachoice1 = list(choice(['mostly cloudy', 'partly sunny'], 1, p=[0.96825396825, 0.03174603174]))[0]
        elif cloudamount[0] == '75-100':
            datachoice1 = 'cloudy'
        elif cloudamount[1] == '50-75':
            datachoice1 = list(choice(['mostly cloudy', 'partly sunny'], 1, p=[0.96825396825, 0.03174603174]))[0]
        elif cloudamount[1] == '75-100':
            datachoice1 = 'cloudy'
        else:
            datachoice1 = list(choice(['cloudy', 'mostly cloudy', 'partly sunny'], 1, p=[0.64804469273, 0.3407821229, 0.01117318435]))[0]
        # Second part is either 0-25 or 25-50
        # Let's look at the final time point to determine what the weather becomes
        if cloudamount[-1] == '0-25':
            datachoice2 = list(choice(['clearing', 'clear', 'sunny', 'mostly clear'], 1, p=[0.08695652173, 0.04347826086, 0.82608695652, 0.04347826086]))[0]
        elif cloudamount[-1] == '25-50':
            datachoice2 = list(choice(['mostly sunny', 'partly cloudy'], 1, p=[0.64545454545, 0.35454545454]))[0]
        # If the final point didn't give the desired results, let's look at the second to last part
        elif cloudamount[-2] == '0-25':
            datachoice2 = \
            list(choice(['clearing', 'clear', 'sunny', 'mostly clear'], 1, p=[0.08695652173, 0.04347826086, 0.82608695652, 0.04347826086]))[0]
        elif cloudamount[-2] == '25-50':
            datachoice2 = list(choice(['mostly sunny', 'partly cloudy'], 1, p=[0.64545454545, 0.35454545454]))
        else:
            datachoice2 = list(choice(['clearing', 'clear', 'sunny', 'mostly clear', 'mostly sunny', 'partly cloudy'], 1,
                                      p=[0.03351955307, 0.01675977653, 0.31843575419, 0.01675977653, 0.39664804469, 0.21787709497]))[0]

        return datachoice1, datachoice2