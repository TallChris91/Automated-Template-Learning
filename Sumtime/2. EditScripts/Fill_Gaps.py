import regex as re
import os
import random
import numpy as np
from numpy.random import choice
import sys

def find_around(startlist):
    aroundlist = startlist[-2:] #Pick the two previous wind directions
    aroundlist += startlist[2:4] #And the two next wind directions
    rand_int = random.randint(0,len(aroundlist)-1) #And pick one randomly
    if rand_int <= 2:
        pick = (aroundlist[rand_int], 'before')
    else:
        pick = (aroundlist[rand_int], 'after')
    return pick

def find_inbetween(directiontuple):
    directions = ['N', 'M-N', 'N-NNE', 'NNE-N', 'N-NE', 'NNE', 'NNE-NE', 'NE-N', 'NE-NNE', 'M-NE', 'NE', 'NE-ENE',
                  'ENE-NE', 'NE-E', 'ENE', 'E-NE',
                  'E-ENE',
                  'E', 'E-ESE', 'ESE-E', 'E-SE', 'ESE', 'ESE-SE', 'SE-E', 'SE-ESE', 'M-SE', 'ORVAR-SE', 'MVAR-SE', 'SE',
                  'SE-SSE', 'SSE-SE', 'SE-S',
                  'SSE', 'S-SE', 'M-S-SE', 'S-SSE', 'SSE-S',
                  'S', 'S-SSW', 'SSW-S', 'S-SW', 'M-S-SW', 'SSW', 'SSW-SW', 'SW-S', 'SW-SSW', 'SW', 'SW-WSW', 'WSW-SW',
                  'SW-W', 'W-SW', 'WSW',
                  'WSW-W', 'W-WSW', 'WSW',
                  'W', 'W-WNW', 'WNW-W', 'W-NW', 'WNW', 'WNW-NW', 'NW-W', 'NW-WNW', 'NW', 'NW-NNW', 'NW-N', 'N-NW',
                  'NNW', 'NNW-N', 'N-NNW', 'w-nnw', 'wsw-wnw']
    index1 = directions.index(directiontuple[0])
    #index2 = directions.index(directiontuple[1])

    startlist = directions[index1:] + directions[:index1] #Get a new list that starts with the first arg
    medianindex = np.argsort(startlist)[len(startlist) // 2]  # Get the index of the median
    index2 = startlist.index(directiontuple[1]) #Get the position of the second argument clockwise from the first one
    secondarg = index2
    if index2 > medianindex: #If the second argument is further away than the median, the wind moved counterclockwise
        index2 = directions.index(directiontuple[1]) #If so, calculate the clockwise distance from the second to the first arg
        startlist = directions[index2:] + directions[:index2]  # Get a new list that starts with the second arg
        secondarg = startlist.index(directiontuple[0])
    if secondarg > 1:
        betweenlist = startlist[1:secondarg]
        betweenpick = random.choice(betweenlist)
        betweenpick = (betweenpick, 'between')
    else:
        betweenpick = find_around(startlist)

    return betweenpick


def add_direction(directionlist, difference):
    combinations = list(zip(directionlist, directionlist[1:]))
    for dif in range(difference):
        try:
            rand_choice = random.choice(combinations)
            for idx, val in enumerate(directionlist): #Get the position of the chosen combination
                if (rand_choice[0] == directionlist[idx]) and (rand_choice[1] == directionlist[idx+1]):
                    choice_idx = idx
                    break
            randompick = find_inbetween(rand_choice)
            if randompick[1] == 'between':
                directionlist.insert(choice_idx + 1, randompick[0])
            if randompick[1] == 'before':
                directionlist.insert(choice_idx-1, randompick[0])
            if randompick[1] == 'after':
                directionlist.insert(choice_idx + 2, randompick[0])
        except IndexError:
            winddirs = ['e-ene', 'ne-nne', 'ssw', 'sw', 'wnw', 'nw', 'w', 'nnw', 'se', 'ene', 's', 's-se', 'nw-wnw', 'ne', 'sse', 'e', 'wsw', 'ese', 'sw-s', 'n',
             'nne', 'se-ese', 'nne-n', 'wnw-w', 'ene-ne', 'w-sw', 'ne-n', 'nw-w', 's-sse', 'ssw-s', 'ese-e', 'sse-se', 'e-ne', 'se-e', 'wsw-sw',
             'sw-ssw', 'w-wsw']
            possibilities = [2, 4, 113, 185, 45, 95, 81, 52, 75, 19, 166, 44, 1, 68, 94, 40, 59, 25, 7, 106, 49, 9, 1, 3, 1, 28, 9, 4, 10, 3, 2, 5, 8, 10, 3, 6, 5]
            possibilities = [float(i) / sum(possibilities) for i in possibilities]
            directionlist.extend(list(choice(winddirs, 1, p=possibilities)))
    return directionlist

def add_wind_gustspeed(occurrencelist, difference, windgust):
    windspeedoptions = ['8', '08-12', '02-06', '8-12', '38-43', '18-25', '6-10', '42-46', '16-22', '20-24', '5-10', '20-25', '40-45', '36-42', '45-50',
                        '22-28', '28-34', '22-26', '08-13', '38-44', '30-34', '02-04', '12-15', '25-28', '35-38', '24-28', '16-20', '25-30', '04-08',
                        '15-20', '12-16', '6-12', '15-18', '35-40', '34-38', '10', '12-18', '05-10', '35-45', '42-48', '08', '48-52', '40-48', '06-10',
                        '28-32', '32-36', '26-32', '10-15', '32-38', '14-18', '30-35', '38-42', '10-14', '26-30', '18-22', '20-26', '26', '36-40', '06-12']
    windspeedfrequencies = [27, 48, 15, 34, 1, 1, 1, 1, 3, 53, 5, 41, 12, 1, 7, 64, 1, 42, 1, 2, 34, 1, 2, 1, 1, 32, 71, 47, 30, 47, 50, 6, 4, 11, 13,
                            28, 85, 1, 1, 1, 11, 1, 1, 41, 75, 22, 12, 41, 16, 90, 21, 15, 77, 69, 114, 1, 1, 7, 1]
    windspeedfrequencies = [float(i) / sum(windspeedfrequencies) for i in windspeedfrequencies]
    gustspeedoptions = ['46', '28', '34', '38', '44', '65', '50', '35', '25', '60', '43', '30', '36', '55-60', '42', '45', '32', '58', '40', '26', '48', '55']
    gustspeedfrequencies = [6, 9, 6, 30, 1, 2, 21, 9, 3, 14, 1, 19, 22, 1, 23, 68, 17, 4, 52, 4, 12, 25]
    gustspeedfrequencies = [float(i) / sum(gustspeedfrequencies) for i in gustspeedfrequencies]
    winddirchangeoptions = ['veering', 'backing']
    winddirchangefrequencies = [210, 208]
    winddirchangefrequencies = [float(i) / sum(winddirchangefrequencies) for i in winddirchangefrequencies]
    windspeedchangeoptions = ['easing', 'decreasing', 'falling', 'increasing', 'rising', 'freshening']
    windspeedchangefrequencies = [150, 58, 19, 181, 46, 12]
    windspeedchangefrequencies = [float(i) / sum(windspeedchangefrequencies) for i in windspeedchangefrequencies]
    timeoptions = ['by late evening', 'by midday', 'by mid evening', 'this morning', 'by evening', 'by midnight', 'by late afternoon', 'by mid afternoon',
                   'mid period', 'by end of period', 'by early evening', 'by this evening', 'this evening', 'by early afternoon', 'by afternoon', 'by late morning', 'by 1200',
                   'by 1800', 'by end of day', 'during the morning', 'mid morning', 'morning', 'during the afternoon', 'this afternoon', 'through the afternoon',
                   'in the afternoon', 'in the evening', 'during the evening', 'through the evening', 'midnight', 'overnight', 'tonight', 'late evening',
                   'around midday', 'midday', 'mid evening', 'late afternoon', 'around mid afternoon', 'mid afternoon', 'around end of period', 'end of period',
                   'early evening', 'early afternoon', 'late in the afternoon', 'late in day', 'later']
    timefrequencies = [94, 81, 10, 10, 107, 23, 40, 29, 4, 22, 11, 8, 33, 5, 26, 2, 2, 2, 4, 1, 1, 1, 5, 20, 3, 2, 13, 9, 1, 4, 3, 1, 24, 6, 5, 1, 3, 1, 1,
                       2, 1, 8, 6, 1, 1, 91]
    timefrequencies = [float(i) / sum(timefrequencies) for i in timefrequencies]
    if windgust == 'wind':
        for dif in range(difference):
            position = random.randint(0, len(occurrencelist))
            occurrencelist.insert(position, 'test')
            while True:
                datachoice = list(choice(windspeedoptions, 1, p=windspeedfrequencies))[0] #Choose random stratified windspeedoption from the possibilities
                #We want the choice to be different than the ones next to it
                if position == 0: #If it will be inserted at the start, you only need to check if it is dissimilar from the next windspeed
                    if (len(occurrencelist) > 1) and (datachoice != occurrencelist[position+1]):
                        break
                    elif len(occurrencelist) == 1:
                        break
                elif position == len(occurrencelist)-1: #Only check the previous entry if it will be inserted last
                    if (len(occurrencelist) > 1) and (datachoice != occurrencelist[position-1]):
                        break
                    elif len(occurrencelist) == 1:
                        break
                elif(datachoice != occurrencelist[position-1]) and (datachoice != occurrencelist[position+1]): #Else check both sides of the insert
                        break
            occurrencelist[position] = datachoice
        return occurrencelist
    if windgust == 'gust':
        for dif in range(difference):
            position = random.randint(0, len(occurrencelist))
            occurrencelist.insert(position, 'test')
            while True:
                datachoice = list(choice(gustspeedoptions, 1, p=gustspeedfrequencies))[0]  # Choose random stratified gustspeedoption from the possibilities
                # We want the choice to be different than the ones next to it
                if position == 0:  # If it will be inserted at the start, you only need to check if it is dissimilar from the next gustspeed
                    if (len(occurrencelist) > 1) and (datachoice != occurrencelist[position + 1]):
                        break
                    elif len(occurrencelist) == 1:
                        break
                elif position == len(occurrencelist)-1:  # Only check the previous entry if it will be inserted last
                    if (len(occurrencelist) > 1) and (datachoice != occurrencelist[position - 1]):
                        break
                    elif len(occurrencelist) == 1:
                        break
                elif (datachoice != occurrencelist[position - 1]) and (datachoice != occurrencelist[position + 1]):  # Else check both sides of the insert
                    break
            occurrencelist[position] = datachoice
        return occurrencelist
    if windgust == 'winddirchange':
        for dif in range(difference):
            position = random.randint(0, len(occurrencelist))
            occurrencelist.insert(position, 'test')
            while True:
                datachoice = list(choice(winddirchangeoptions, 1, p=winddirchangefrequencies))[0]  # Choose random stratified gustspeedoption from the possibilities
                # We want the choice to be different than the ones next to it
                if position == 0:  # If it will be inserted at the start, you only need to check if it is dissimilar from the next gustspeed
                    if (len(occurrencelist) > 1) and (datachoice != occurrencelist[position + 1]):
                        break
                    elif len(occurrencelist) == 1:
                        break
                elif position == len(occurrencelist)-1:  # Only check the previous entry if it will be inserted last
                    if (len(occurrencelist) > 1) and (datachoice != occurrencelist[position - 1]):
                        break
                    elif len(occurrencelist) == 1:
                        break
                elif (datachoice != occurrencelist[position - 1]) and (datachoice != occurrencelist[position + 1]):  # Else check both sides of the insert
                    break
            occurrencelist[position] = datachoice
        return occurrencelist
    if windgust == 'windspeedchange':
        for dif in range(difference):
            position = random.randint(0, len(occurrencelist))
            occurrencelist.insert(position, 'test')
            while True:
                datachoice = list(choice(windspeedchangeoptions, 1, p=windspeedchangefrequencies))[0]  # Choose random stratified windspeedoption from the possibilities
                # We want the choice to be different than the ones next to it
                if position == 0:  # If it will be inserted at the start, you only need to check if it is dissimilar from the next gustspeed
                    if (len(occurrencelist) > 1) and (datachoice != occurrencelist[position + 1]):
                        break
                    elif len(occurrencelist) == 1:
                        break
                elif position == len(occurrencelist)-1:  # Only check the previous entry if it will be inserted last
                    if (len(occurrencelist) > 1) and (datachoice != occurrencelist[position - 1]):
                        break
                    elif len(occurrencelist) == 1:
                        break
                elif (datachoice != occurrencelist[position - 1]) and (datachoice != occurrencelist[position + 1]):  # Else check both sides of the insert
                    break
            occurrencelist[position] = datachoice
        return occurrencelist
    if windgust == 'time':
        timepossibilities = ['0600', '0900', '1200', '1500', '1800', '2100', '2400']
        for dif in range(difference):
            occurrencelist = [re.sub(r'0000', '2400', x) for x in occurrencelist]
            timepossibilities = [x for x in timepossibilities if x not in occurrencelist]
            timechoice = random.choice(timepossibilities)
            occurrencelist.append(timechoice)
            occurrencelist.sort(key=int)
            occurrencelist = [re.sub(r'2400', '0000', x) for x in occurrencelist]
        return occurrencelist

def gap_filler(file):
    currentpath = os.getcwd()
    with open(currentpath + '/Corpora/' + file + '.data') as f:
        data = f.readlines()
    #data = [x.decode('utf-8') for x in data]
    data = [re.sub(r'\n', '', x) for x in data]

    with open(currentpath + '/Corpora/' + file + '_gaps.data') as f:
        gapdata = f.readlines()
    #text = [x.decode('utf-8') for x in text]
    gapdata = [re.sub(r'\n', '', x) for x in gapdata]

    #with open(currentpath + '/Corpora/' + file + '_output_unoptimized_gaps.text') as f:
    with open(currentpath + '/Corpora/Test_Retrieval_Gaps.txt') as f:
        gaptext = f.readlines()
    #text = [x.decode('utf-8') for x in text]
    gaptext = [re.sub(r'\n', '', x) for x in gaptext]

    with open(currentpath + '/Corpora/' + file + '.text') as f:
        text = f.readlines()
    #text = [x.decode('utf-8') for x in text]
    text = [re.sub(r'\n', '', x) for x in text]

    data = [re.sub(r': ', ':', x) for x in data]
    data = [x.split(' ') for x in data]
    newdata = []
    for idx, val in enumerate(data):
        data[idx] = [x.split(':') for x in data[idx]]
        newdata.append(data[idx])

    for idx, line in enumerate(newdata):
        if text[idx] == '':
            continue
        winddirlist = []
        windspeedlist = []
        gustspeedlist = []
        timelist = []
        winddirchangelist = []
        windspeedchangelist = []
        num = 0
        while num < len(line):
            if 'WindDir.' in line[num][0]:
                winddirlist.append(line[num][1])
            if 'WindSpeedMin.' in line[num][0]:
                if (num != len(line)-1) and ('WindSpeedMax.' in line[num + 1][0]):
                    windspeedlist.append(line[num][1] + '-' + line[num+1][1])
                    del line[num+1]
                else:
                    windspeedlist.append(line[num][1])
            if 'WindSpeedMax.' in line[num][0]:
                windspeedlist.append(line[num][1])
            if 'GustSpeedMin.' in line[num][0]:
                if (num != len(line)-1) and ('GustSpeedMax.' in line[num + 1][0]):
                    gustspeedlist.append(line[num][1] + '-' + line[num+1][1])
                    del line[num+1]
                else:
                    gustspeedlist.append(line[num][1])
            if 'GustSpeedMax.' in line[num][0]:
                gustspeedlist.append(line[num][1])
            if 'Time.' in line[num][0]:
                timelist.append(line[num][1])
            if ('WindDirChange.' in line[num][0]) and (line[num][1] != 'same'): #Same wind directions aren't reported in the text, only changes
                winddirchangelist.append(line[num][1])
            if ('WindSpeedChange.' in line[num][0]) and (line[num][1] != 'same'): #Same wind speeds aren't reported in the text, only changes
                windspeedchangelist.append(line[num][1])
            num += 1

        templatewinddirlist = []
        templatewindspeedlist = []
        templategustspeedlist = []
        templatetimelist = []
        templatewinddirchangelist = []
        templatewindspeedchangelist = []
        templatesline = re.findall('(<(.*?)>)', gaptext[idx])
        templatesline = [t[0] for t in templatesline]
        for template in templatesline:
            if template == '<wind_direction>':
                templatewinddirlist.append(template)
            elif template == '<wind_speed>':
                templatewindspeedlist.append(template)
            elif template == '<gust_speed>':
                templategustspeedlist.append(template)
            elif template == '<time>':
                templatetimelist.append(template)
            elif template == '<wind_direction_change>':
                templatewinddirchangelist.append(template)
            elif template == '<wind_speed_change>':
                templatewindspeedchangelist.append(template)

        if len(templatewinddirlist) != len(winddirlist):
            if len(winddirlist) > len(templatewinddirlist): #If there are more wind directions in the data than winddir gaps in the line
                difference = len(winddirlist) - len(templatewinddirlist) #See how many more
                for dif in range(difference): #And delete as many ones randomly from the data
                    del winddirlist[random.randint(0, len(winddirlist) - 1)]
            if len(templatewinddirlist) > len(winddirlist): #If there are more gaps than directions, we need to add more random directions
                difference = len(templatewinddirlist) - len(winddirlist)  # See how many more
                winddirlist = add_direction(winddirlist, difference) #And add as many to the winddirlist, either in between two directions or a direction close by a direction
        if len(templatewindspeedlist) != len(windspeedlist):
            if len(windspeedlist) > len(templatewindspeedlist):
                difference = len(windspeedlist) - len(templatewindspeedlist)  # See how many more
                for dif in range(difference):  # And delete as many ones randomly from the data
                    del windspeedlist[random.randint(0, len(windspeedlist) - 1)]
            if len(templatewindspeedlist) > len(windspeedlist): #If there are more templates than speeds in the data
                difference = len(templatewindspeedlist) - len(windspeedlist) #See how many more
                windspeedlist = add_wind_gustspeed(windspeedlist, difference, 'wind') #And randomly add a speed to one of the gaps
        if len(templategustspeedlist) != len(gustspeedlist): #Gust works the same as wind
            if len(gustspeedlist) > len(templategustspeedlist):
                difference = len(gustspeedlist) - len(templategustspeedlist)
                for dif in range(difference):
                    del gustspeedlist[random.randint(0, len(gustspeedlist) - 1)]
            if len(templategustspeedlist) > len(gustspeedlist):
                difference = len(templategustspeedlist) - len(gustspeedlist)
                gustspeedlist = add_wind_gustspeed(gustspeedlist, difference, 'gust')
        if len(templatewinddirchangelist) != len(winddirchangelist): #Same for winddirchange
            if len(winddirchangelist) > len(templatewinddirchangelist):
                difference = len(winddirchangelist) - len(templatewinddirchangelist)
                for dif in range(difference):
                    del winddirchangelist[random.randint(0, len(winddirchangelist) - 1)]
            if len(templatewinddirchangelist) > len(winddirchangelist):
                difference = len(templatewinddirchangelist) - len(winddirchangelist)
                winddirchangelist = add_wind_gustspeed(winddirchangelist, difference, 'winddirchange')
        if len(templatewindspeedchangelist) != len(windspeedchangelist): #Same for windspeedchange
            if len(windspeedchangelist) > len(templatewindspeedchangelist):
                difference = len(windspeedchangelist) - len(templatewindspeedchangelist)
                for dif in range(difference):
                    del windspeedchangelist[random.randint(0, len(windspeedchangelist) - 1)]
            if len(templatewindspeedchangelist) > len(windspeedchangelist):
                difference = len(templatewindspeedchangelist) - len(windspeedchangelist)
                windspeedchangelist = add_wind_gustspeed(windspeedchangelist, difference, 'windspeedchange')
        if (len(templatetimelist) != len(timelist)) and (len(templatetimelist) > 0):
            if len(timelist) > len(templatetimelist):
                difference = len(timelist) - len(templatetimelist)
                if difference == 1: #Difference of one usually means the first time isn't mentioned
                    del timelist[0]
                else:
                    del timelist[0] #Same goes for bigger differences, delete the first mention first
                    difference -= 1
                    for dif in range(difference):
                        del timelist[random.randint(0, len(timelist) - 2)] #Keep the last mention there, that one is usually mentioned
            if len(templatetimelist) > len(timelist):
                difference = len(templatetimelist) - len(timelist)
                timelist = add_wind_gustspeed(timelist, difference, 'time')

        #ZELFDE VOOR TIJD TOEVOEGEN
        #WINDDIRCHANGE, WINDSPEEDCHANGE EN TIME INFO VERVANGEN DOOR WOORDEN
        #'LY RANDOM TOEWIJZEN AAN WINDDIRECTIONS

        for idx2, template in enumerate(timelist):
            if timelist[idx2] == '0600':
                timelist[idx2] = 'this morning'
            elif timelist[idx2] == '0900':
                if idx2 == len(timelist)-1: #Later can only be a possibility if this is the last template in the list
                    timelist[idx2] = list(choice(['later', 'this morning', 'by midday'], 1, p=[float(i) / sum([2, 4, 2]) for i in [2, 4, 2]]))[0]
                else:
                    timelist[idx2] = list(choice(['this morning', 'by midday'], 1, p=[float(i) / sum([4, 2]) for i in [4, 2]]))[0]
            elif timelist[idx2] == '1200':
                if idx2 == len(timelist)-1:
                    timelist[idx2] = list(choice(['by midday', 'by afternoon', 'this morning', 'by early afternoon', 'midday', 'around midday',
                                                         'early afternoon', 'by 1200', 'later', 'by late morning', 'during the morning'], 1,
                                                        p=[float(i) / sum([62, 12, 5, 2, 1, 2, 1, 2, 4, 1, 1]) for i in [62, 12, 5, 2, 1, 2, 1, 2, 4, 1, 1]]))[0]
                else:
                    timelist[idx2] = list(choice(['by midday', 'by afternoon', 'this morning', 'by early afternoon', 'midday', 'around midday',
                                                         'early afternoon', 'by 1200', 'by late morning', 'during the morning'], 1,
                                                        p=[float(i) / sum([62, 12, 5, 2, 1, 2, 1, 2, 1, 1]) for i in
                                                           [62, 12, 5, 2, 1, 2, 1, 2, 1, 1]]))[0]
            elif timelist[idx2] == '1500':
                if idx2 == len(timelist) - 1:
                    timelist[idx2] = list(choice(['this afternoon', 'by mid afternoon', 'by afternoon', 'mid period', 'by midday',
                                                         'by early afternoon', 'during the afternoon', 'later', 'around midday', 'by late afternoon',
                                                         'late afternoon', 'through the afternoon', 'around mid afternoon'], 1,
                                                        p=[float(i) / sum([10, 18, 10, 4, 2, 2, 4, 2, 1, 1, 1, 1, 1]) for i in [10, 18, 10, 4, 2, 2, 4, 2, 1, 1, 1, 1, 1]]))[0]
                else:
                    timelist[idx2] = list(choice(['this afternoon', 'by mid afternoon', 'by afternoon', 'mid period', 'by midday',
                                                         'by early afternoon', 'during the afternoon', 'around midday', 'by late afternoon',
                                                         'late afternoon', 'through the afternoon', 'around mid afternoon'], 1,
                                p=[float(i) / sum([10, 18, 10, 4, 2, 2, 4, 1, 1, 1, 1, 1]) for i in [10, 18, 10, 4, 2, 2, 4, 1, 1, 1, 1, 1]]))[0]
            elif timelist[idx2] == '1800':
                if idx2 == len(timelist) - 1:
                    timelist[idx2] = list(choice(['by late afternoon', 'by evening', 'by early evening', 'during the afternoon',
                                                         'this evening', 'this afternoon', 'by this evening', 'by end of period',
                                                         'early evening', 'by 1800', 'later'], 1,
                                                        p=[float(i) / sum([26, 60, 11, 1, 3, 4, 2, 4, 4, 2, 1]) for i in [26, 60, 11, 1, 3, 4, 2, 4, 4, 2, 1]]))[0]
                else:
                    timelist[idx2] = list(choice(['by late afternoon', 'by evening', 'by early evening', 'during the afternoon',
                                                         'this evening', 'this afternoon', 'by this evening',
                                                         'early evening', 'by 1800'], 1,
                                                        p=[float(i) / sum([26, 60, 11, 1, 3, 4, 2, 4, 2]) for i in
                                                           [26, 60, 11, 1, 3, 4, 2, 4, 2]]))[0]
            elif timelist[idx2] == '2100':
                if idx2 == len(timelist) - 1:
                    timelist[idx2] = list(choice(['by mid evening', 'by evening', 'by end of period', 'in the evening', 'by this evening', 'during the evening',
                                                         'this evening', 'by late evening', 'later', 'late in day'], 1,
                                                        p=[float(i) / sum([9, 23, 2, 11, 6, 4, 22, 1, 6, 1]) for i in
                                                           [9, 23, 2, 11, 6, 4, 22, 1, 6, 1]]))[0]
                else:
                    timelist[idx2] = list(choice(['by mid evening', 'by evening', 'in the evening', 'by this evening', 'during the evening',
                                 'this evening', 'by late evening', 'late in day'], 1,
                                p=[float(i) / sum([9, 23, 11, 6, 4, 22, 1, 1]) for i in
                                   [9, 23, 11, 6, 4, 22, 1, 1]]))[0]
            elif timelist[idx2] == '0000':
                if idx2 == len(timelist) - 1:
                    timelist[idx2] = list(choice(['by late evening', 'later', 'by midnight', 'late evening', 'by end of period', 'end of period',
                                                         'around end of period', 'by end of day', 'midnight', 'overnight', 'through the evening'], 1,
                                                        p=[float(i) / sum([82, 60, 11, 17, 12, 1, 1, 1, 2, 1, 1]) for i in
                                                           [82, 60, 11, 17, 12, 1, 1, 1, 2, 1, 1]]))[0]
                else:
                    timelist[idx2] = \
                    list(choice(['by late evening', 'by midnight', 'late evening', 'by end of day', 'midnight', 'overnight', 'through the evening'], 1,
                                p=[float(i) / sum([82, 11, 17, 1, 2, 1, 1]) for i in
                                   [82, 11, 17, 1, 2, 1, 1]]))[0]
        for idx2, template in enumerate(winddirlist):
            winddirchoice = list(choice(['no', 'ly'], 1, p=[float(i) / sum([1253, 184]) for i in [1253, 184]]))[0]
            if winddirchoice == 'ly':
                winddirlist[idx2] = winddirlist[idx2].lower() + "'ly"
            else:
                winddirlist[idx2] = winddirlist[idx2].lower()
        for idx2, template in enumerate(winddirchangelist):
            if winddirchangelist[idx2] == 'clock':
                winddirchangelist[idx2] = 'veering'
            elif winddirchangelist[idx2] == 'ctrclock':
                winddirchangelist[idx2] = 'backing'
        for idx2, template in enumerate(windspeedchangelist):
            if windspeedchangelist[idx2] == 'up':
                windspeedchangelist[idx2] = list(choice(['increasing', 'rising', 'freshening'], 1, p=[float(i) / sum([181, 46, 12]) for i in [181, 46, 12]]))[0]
            elif windspeedchangelist[idx2] == 'down':
                windspeedchangelist[idx2] = list(choice(['easing', 'decreasing', 'falling'], 1, p=[float(i) / sum([150, 58, 19]) for i in [150, 58, 19]]))[0]

        for winddir in winddirlist:
            gaptext[idx] = re.sub('<wind_direction>', winddir, gaptext[idx], count=1)
        for windspeed in windspeedlist:
            gaptext[idx] = re.sub('<wind_speed>', windspeed, gaptext[idx], count=1)
        for gustspeed in gustspeedlist:
            gaptext[idx] = re.sub('<gust_speed>', gustspeed, gaptext[idx], count=1)
        for time in timelist:
            gaptext[idx] = re.sub('<time>', time, gaptext[idx], count=1)
        for winddirchange in winddirchangelist:
            gaptext[idx] = re.sub('<wind_direction_change>', winddirchange, gaptext[idx], count=1)
        for windspeedchange in windspeedchangelist:
            gaptext[idx] = re.sub('<wind_speed_change>', windspeedchange, gaptext[idx], count=1)

    return gaptext




#for file in ['All', 'Dev', 'Test', 'Train']:
for file in ['Test']:
    currentpath = os.getcwd()
    filledgaps = gap_filler(file)

    filledgaps = '\n'.join(filledgaps)
    #with open(currentpath + '/Corpora/' + file + '_output_unoptimized_gaps_filled.text', 'wb') as f:
    with open(currentpath + '/Corpora/Test_Retrieval_Gaps_Filled.txt', 'wb') as f:
        print('Writing new file')
        f.write(bytes(filledgaps, 'UTF-8'))
