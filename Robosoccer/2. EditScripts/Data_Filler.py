import os
import regex as re
import sys
from numpy.random import choice

def Find_Argument(dataline, searchterm):
    arguments = dataline.split(" ")
    for argument in arguments:
        if searchterm in argument:
            argument = argument.split(":")
            return argument[1]

def Return_Arguments(dataline):
    dataline = re.sub(r": ", ":", dataline)
    arguments = dataline.split(" ")
    arguments = [x.split(":") for x in arguments]
    return arguments

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

    with open(currentpath + '/Corpora/sportscasting/' + filename + '_2.text', 'rb') as f:
        text = f.readlines()
    text = [t.decode('utf-8') for t in text]
    text = [re.sub(r": ", ':', x) for x in text]
    text = [re.sub(r"\n", '', x) for x in text]

    for idx, line in enumerate(newdata):
        if not re.search(r"\w", newdata[idx]):
            continue
        datatype = []
        previousplayers = []
        # Get a list of the gaps in the line, and produce a filler for each gap
        #And first try to find the argument corresponding with the gap in the new data
        arguments = Return_Arguments(newdata[idx])
        datatype = [x[0] for x in arguments if len(x) > 1]
        templateplayers = [x[1] for x in arguments if len(x) > 1]
        filledplayers = []
        #player = Random_Player(data[idx], previousplayers)
        #Else we can try to find the player the proper way by looking the player up in the old data using the argument
        for idx2, player in enumerate(templateplayers):
            player = Find_Argument(data[idx], datatype[idx2])
            #If the argument does not exist in the old data, we'll keep it an empty template (to see which ones go wrong
            if player == None:
                filledplayers.append(templateplayers[idx2])
            elif (templateplayers[idx2] == '<player_1_team_1>') or (templateplayers[idx2] == '<player_1_team_2>') or (templateplayers[idx2] == '<player_2_team_1>')\
                    or (templateplayers[idx2] == '<player_2_team_2>') or (templateplayers[idx2] == '<player_1>') or (templateplayers[idx2] == '<player_2>'):
                filledplayers.append(player)
            #Modify the player if necessary
            elif (templateplayers[idx2] == '<team_1>') or (templateplayers[idx2] == '<team_2>'):
                team = re.sub(r'\d+', ' team', player)
                filledplayers.append(team)
            else:
                filledplayers.append(templateplayers[idx2])

        for filleridx, fillerval in enumerate(datatype):
            newdata[idx] = re.sub(re.escape(templateplayers[filleridx]), filledplayers[filleridx], newdata[idx], count=1)

        newdata[idx] = re.sub(r':', ': ', newdata[idx])

    for idx, line in enumerate(newdata):
        if re.search('<(.*?)>', newdata[idx]): #If there's still open gaps in the data
            gaps = re.findall('(<(.*?)>)', newdata[idx])
            gaps = [t[0] for t in gaps]
            playerstext = re.findall(r'((pink\d+)|(pink\sgoalie)|(pink\steam)|(purple\d+)|(purple\sgoalie)|(purple\steam))', text[idx]) #Look in the text if you can find the players or teams there
            playerstext = [t[0] for t in playerstext]
            if len(gaps) == len(playerstext):
                for filleridx, fillerval in enumerate(gaps):
                    newdata[idx] = re.sub(re.escape(gaps[filleridx]), playerstext[filleridx], newdata[idx], count=1)
            else:
                del playerstext[1]
                for filleridx, fillerval in enumerate(gaps):
                    newdata[idx] = re.sub(re.escape(gaps[filleridx]), playerstext[filleridx], newdata[idx], count=1)


    return newdata





filelist = ['All', 'Train', 'Test', 'Dev']
currentpath = os.getcwd()
for file in filelist:
    templates = Get_Templates(file)
    templatelines = '\n'.join(templates)
    templatelines += '\n'
    with open(currentpath + '/Corpora/sportscasting/' + file + '_2_new_filled.data', 'wb') as f:
        f.write(bytes(templatelines, 'UTF-8'))