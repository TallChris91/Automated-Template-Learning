import os
import regex as re
import sys
from numpy.random import choice

def Find_Argument(dataline, searchterm, new='y'):
    arguments = dataline.split(" ")
    for argument in arguments:
        if searchterm in argument:
            argument = argument.split(":")
            if new == 'y':
                return argument[0]
            elif new == 'n':
                return argument[1]

def Random_Player(dataline, previousplayers):
    possibleplayers = []
    arguments = dataline.split(" ")
    for argument in arguments:
        argument = argument.split(":")
        if (argument[1] not in possibleplayers) and (('purple' in argument[1]) or ('pink' in argument[1])):
            possibleplayers.append(argument[1])
    possibleplayers = [x for x in possibleplayers if x not in previousplayers]

    if len(possibleplayers) > 0:
        randompick = choice(possibleplayers)
    else:
        pinkchoices = ['pink' + str(num) for num in range(1, 12)]
        purplechoices = ['purple' + str(num) for num in range(1, 12)]
        allchoices = pinkchoices + purplechoices
        randompick = choice(allchoices)
    return randompick

def Get_Templates(filename):
    with open(currentpath + '/Corpora/sportscasting/' + filename + '_2.data', 'rb') as f:
        data = f.readlines()
    data = [t.decode('utf-8') for t in data]
    data = [re.sub(r": ", ':', x) for x in data]
    data = [re.sub(r"\n", '', x) for x in data]

    with open(currentpath + '/Corpora/sportscasting/' + filename + '_2_new.data', 'rb') as f:
        newdata = f.readlines()
    newdata = [t.decode('utf-8') for t in newdata]
    newdata = [re.sub(r": ", ':', x) for x in newdata]
    newdata = [re.sub(r"\n", '', x) for x in newdata]

    #with open(currentpath + '/Corpora/sportscasting/' + filename + '_2_new_Sportscasting_Unoptimized.text', 'rb') as f:
    with open(currentpath + '/Corpora/sportscasting/Test_Retrieval_Gaps.txt', 'rb') as f:
        templates = f.readlines()
    templates = [t.decode('utf-8') for t in templates]
    templates = [re.sub(r"\n", '', x) for x in templates]

    for idx, line in enumerate(templates):
        if not re.search(r"\w", newdata[idx]):
            continue
        fillers = []
        previousplayers = []
        # Get a list of the gaps in the line, and produce a filler for each gap
        gaps = re.findall('(<(.*?)>)', templates[idx])
        gaps = [t[0] for t in gaps]
        #Go over each gap
        for gap in gaps:
            #And first try to find the argument corresponding with the gap in the new data
            argument = Find_Argument(newdata[idx], gap, new='y')
            #If the gap is not represented in the data, we can just skip the next step and find a random player
            if argument == None:
                player = Random_Player(data[idx], previousplayers)
            #Else we can try to find the player the proper way by looking the player up in the old data using the argument
            else:
                player = Find_Argument(data[idx], argument, new='n')
                #If the argument does not exist in the old data, we'll bust out the random player finder again
                if player == None:
                    player = Random_Player(data[idx], previousplayers)
            previousplayers.append(player)
            #Modify the player if necessary
            if (gap == '<team_1>') or (gap == '<team_2>'):
                filler = re.sub(r'\d+', ' team', player)
            elif (player == 'pink1') or (player == 'purple1'):
                plist = [52, 848]
                plist = [float(i) / sum(plist) for i in plist]
                goaliechange = list(choice(['Yes', 'No'], 1, p=plist))[0]
                if goaliechange == 'Yes':
                    filler = re.sub(r'\d+', ' goalie', player)
            else:
                filler = player
            fillers.append(filler)

        for filleridx, fillerval in enumerate(fillers):
            templates[idx] = re.sub(re.escape(gaps[filleridx]), fillerval, templates[idx], count=1)

    return templates





filelist = ['Test']
currentpath = os.getcwd()
for file in filelist:
    templates = Get_Templates(file)
    templatelines = '\n'.join(templates)
    with open(currentpath + '/Corpora/sportscasting/Test_Retrieval_Gaps_Filled.txt', 'wb') as f:
        f.write(bytes(templatelines, 'UTF-8'))