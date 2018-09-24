import regex as re
import os
import random
import numpy as np
from collections import Counter
from numpy.random import choice

currentpath = os.getcwd()

with open(currentpath + '/Corpora/All.text') as f:
    text = f.readlines()
# text = [x.decode('utf-8') for x in text]
text = [re.sub(r'\n', '', x) for x in text]

with open(currentpath + '/Corpora/All_gaps.text') as f:
    gaptext = f.readlines()
# text = [x.decode('utf-8') for x in text]
gaptext = [re.sub(r'\n', '', x) for x in gaptext]

with open('C:/Users/chris/Syncmap/Promotie/Automated_Template_Generation/Sumtime/Corpora/All2.data') as f:
    data = f.readlines()
#data = [x.decode('utf-8') for x in data]
data = [re.sub(r'\n', '', x) for x in data]
data = [re.sub(r': ', ':', x) for x in data]
data = [x.split(' ') for x in data]
newdata = []
for idx, val in enumerate(data):
    data[idx] = [x.split(':') for x in data[idx]]
    newdata.append(data[idx])

occurrencedict = {}
totalwinddirs = 0
totalwinddirslist = []
for idx, line in enumerate(newdata):
    timelist = []
    num = 0
    while num < len(line):
        if 'Time.' in line[num][0]:
            timelist.append(line[num][1])
        num += 1

    templatesline = re.findall('(<time>)', gaptext[idx])
    #templatesline = [t[0] for t in templatesline]
    if len(timelist) == len(templatesline):
        timeline = re.findall(r'((by late evening)|(by midday)|(by mid evening)|(this morning)|(by evening)|(by midnight)|(by late afternoon)|(by mid afternoon)|(mid period)|(by end of period)|(by early evening)|(by this evening)|(this evening)|(by early afternoon)|(by afternoon)|(by late morning)|(by 1200)|(by 1800)|(by end of day)|(during the morning)|(mid morning)|(morning)|(during the afternoon)|(this afternoon)|(through the afternoon)|(in the afternoon)|(in the evening)|(during the evening)|(through the evening)|(midnight)|(overnight)|(tonight)|(late evening)|(around midday)|(midday)|(mid evening)|(late afternoon)|(around mid afternoon)|(mid afternoon)|(around end of period)|(end of period)|(early evening)|(early afternoon)|(late in the afternoon)|(late in day)|(later))', text[idx])
        timeline = [t[0] for t in timeline]
        if (len(timelist) == len(timeline)) and (len(timelist) > 0):
            combine = list(zip(timelist, timeline))
            combine = [' '.join(x) for x in combine]
            for combination in combine:
                if combination not in occurrencedict:
                    occurrencedict[combination] = 1
                else:
                    occurrencedict[combination] += 1
    elif len(timelist) > len(templatesline):
        timelist = timelist[1:]
        if len(timelist) == len(templatesline):
            timeline = re.findall(
                r'((by late evening)|(by midday)|(by mid evening)|(this morning)|(by evening)|(by midnight)|(by late afternoon)|(by mid afternoon)|(mid period)|(by end of period)|(by early evening)|(by this evening)|(this evening)|(by early afternoon)|(by afternoon)|(by late morning)|(by 1200)|(by 1800)|(by end of day)|(during the morning)|(mid morning)|(morning)|(during the afternoon)|(this afternoon)|(through the afternoon)|(in the afternoon)|(in the evening)|(during the evening)|(through the evening)|(midnight)|(overnight)|(tonight)|(late evening)|(around midday)|(midday)|(mid evening)|(late afternoon)|(around mid afternoon)|(mid afternoon)|(around end of period)|(end of period)|(early evening)|(early afternoon)|(late in the afternoon)|(late in day)|(later))',
                text[idx])
            timeline = [t[0] for t in timeline]
            if (len(timelist) == len(timeline)) and (len(timelist) > 0):
                combine = list(zip(timelist, timeline))
                combine = [' '.join(x) for x in combine]
                for combination in combine:
                    if combination not in occurrencedict:
                        occurrencedict[combination] = 1
                    else:
                        occurrencedict[combination] += 1
        elif len(templatesline) == 0:
            pass
        else:
            timeline = re.findall(
                r'((by late evening)|(by midday)|(by mid evening)|(this morning)|(by evening)|(by midnight)|(by late afternoon)|(by mid afternoon)|(mid period)|(by end of period)|(by early evening)|(by this evening)|(this evening)|(by early afternoon)|(by afternoon)|(by late morning)|(by 1200)|(by 1800)|(by end of day)|(during the morning)|(mid morning)|(morning)|(during the afternoon)|(this afternoon)|(through the afternoon)|(in the afternoon)|(in the evening)|(during the evening)|(through the evening)|(midnight)|(overnight)|(tonight)|(late evening)|(around midday)|(midday)|(mid evening)|(late afternoon)|(around mid afternoon)|(mid afternoon)|(around end of period)|(end of period)|(early evening)|(early afternoon)|(late in the afternoon)|(late in day)|(later))',
                text[idx])
            timeline = [t[0] for t in timeline]
            #The time mention at the end is usually about the last time data
            if re.search(r'<time>$', gaptext[idx]):
                combine = list(zip(timelist[-1], timeline[-1]))
                combine = [' '.join(x) for x in combine]
                for combination in combine:
                    if combination not in occurrencedict:
                        occurrencedict[combination] = 1
                    else:
                        occurrencedict[combination] += 1
            #No time mention at the end, usually means the last time point isn't mentioned, so delete the last one and see if lists are equal now
            else:
                del timelist[-1]
                if len(timelist) == len(templatesline):
                    combine = list(zip(timelist, timeline))
                    combine = [' '.join(x) for x in combine]
                    for combination in combine:
                        if combination not in occurrencedict:
                            occurrencedict[combination] = 1
                        else:
                            occurrencedict[combination] += 1

    winddirs = re.findall(r'((\bN\b)|(\bM-N\b)|(\bN-NNE\b)|(\bNNE-N\b)|(\bN-NE\b)|(\bNNE\b)|(\bNNE-NE\b)|(\bNE-N\b)|(\bNE-NNE\b)|(\bM-NE\b)|(\bNE\b)|(\bNE-ENE\b)|(\bENE-NE\b)|(\bNE-E\b)|(\bENE\b)|(\bE-NE\b)|(\bE-ENE\b)|(\bE\b)|(\bE-ESE\b)|(\bESE-E\b)|(\bE-SE\b)|(\bESE\b)|(\bESE-SE\b)|(\bSE-E\b)|(\bSE-ESE\b)|(\bM-SE\b)|(\bORVAR-SE\b)|(\bMVAR-SE\b)|(\bSE\b)|(\bSE-SSE\b)|(\bSSE-SE\b)|(\bSE-S\b)|(\bSSE\b)|(\bS-SE\b)|(\bM-S-SE\b)|(\bS-SSE\b)|(\bSSE-S\b)|(\bS\b)|(\bS-SSW\b)|(\bSSW-S\b)|(\bS-SW\b)|(\bM-S-SW\b)|(\bSSW\b)|(\bSSW-SW\b)|(\bSW-S\b)|(\bSW-SSW\b)|(\bSW\b)|(\bSW-WSW\b)|(\bWSW-SW\b)|(\bSW-W\b)|(\bW-SW\b)|(\bWSW\b)|(\bWSW-W\b)|(\bW-WSW\b)|(\bWSW\b)|(\bW\b)|(\bW-WNW\b)|(\bWNW-W\b)|(\bW-NW\b)|(\bWNW\b)|(\bWNW-NW\b)|(\bNW-W\b)|(\bNW-WNW\b)|(\bNW\b)|(\bNW-NNW\b)|(\bNW-N\b)|(\bN-NW\b)|(\bNNW\b)|(\bNNW-N\b)|(\bN-NNW\b)|(\bw-nnw\b)|(\bwsw-wnw\b))', text[idx], flags=re.I)
    winddirs = [t[0] for t in winddirs]
    totalwinddirslist.extend(winddirs)
    totalwinddirs += len(winddirs)

totalwinddirslist = dict(Counter(totalwinddirslist))
directions, possibilities = zip(*totalwinddirslist.items())
directions = list(directions)
possibilities = list(possibilities)
possibilities = [float(i) / sum(possibilities) for i in possibilities]
print(list(choice(directions, 1, p=possibilities)))

#datachoice = list(choice(directions, 1, p=possibilities))[0]

'''
for key in occurrencedict:
    if '1500' in key:
        print(key, occurrencedict[key])
'''