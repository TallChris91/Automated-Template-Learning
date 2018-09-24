import os
import regex as re
from numpy.random import choice

clubdict = {'PEC Zwolle': ['de zwollenaren', 'zwolle', 'pec', 'de equipe uit overijssel', 'de ploeg van trainer ron jans'], 'N.E.C.': ['nec', 'de nijmegenaren', 'nijmegen', 'de ploeg van ernest faber'], 'ADO Den Haag': ['ado', 'de hagenaars', 'den haag', 'de club uit den haag'],
     'Go Ahead Eagles': ['go ahead', 'de deventenaren', 'de eagles', 'eagles', 'de ploeg van hans de koning'], 'FC Twente': ['Twente', 'de tukkers', 'de enschedeërs', 'de ploeg van trainer rené hake', 'de ploeg van hake'],
     'Excelsior': ['de kralingers', 'de rotterdammers', 'de ploeg van coach alfons groenendijk', 'het team van mitchell van der gaag'], 'FC Utrecht': ['utrecht', 'de utrechters', 'de domstedelingen', 'de ploeg van trainer erik ten hag', 'de ploeg van ten hag'], 'PSV': ['de eindhovenaren', 'de ploeg uit eindhoven', 'de ploeg van phillip cocu', 'de ploeg van trainer phillip cocu', 'de ploeg van cocu'],
     'Willem II': ['de tilburgers', 'de tricolores'], 'Vitesse': ['de arnhemmers', 'de arnhemse equipe'], 'AZ': ['de alkmaarders', 'de ploeg van john van den brom', 'de ploeg van trainer john van den brom'],
     'sc Heerenveen': ['heerenveen', 'de club uit heerenveen', 'de friezen'], 'FC Groningen': ['groningen', 'de groningers'],
     'Feyenoord': ['de rotterdammers', 'de ploeg van giovanni van bronckhorst'], 'Roda JC Kerkrade': ['roda jc', 'roda', 'kerkrade', 'de ploeg uit kerkrade', 'de limburgers', 'de ploeg van trainer yannis anastasiou'],
     'Heracles Almelo': ['heracles', 'de almeloërs', 'de heraclieden', 'de club uit almelo'], 'Sparta Rotterdam': ['sparta', 'de rotterdammers'],
     'Ajax': ['de amsterdammers', 'de ajacieden'], 'De Graafschap': ['de superboeren', 'de ploeg uit doetinchem', 'graafschap'],
     'SC Cambuur Leeuwarden': ['cambuur', 'sc cambuur', 'cambuur leeuwarden', 'de leeuwarders', 'de friezen']}

clubadjectivedict = {'PEC Zwolle': ['zwols'], 'N.E.C.': ['nijmeegs'], 'ADO Den Haag': ['haags'], 'Go Ahead Eagles': ['deventer'], 'FC Twente': ['twents'],
     'Excelsior': ['kralings', 'rotterdams'], 'FC Utrecht': ['utrechts'], 'PSV': ['eindhovens'], 'Willem II': ['tilburgs'], 'Vitesse': ['arnhems'], 'AZ': ['alkmaars'],
     'sc Heerenveen': ['heerenveens', 'fries'], 'FC Groningen': ['gronings'], 'Feyenoord': ['rotterdams'], 'Roda JC Kerkrade': ['limburgs'],
     'Heracles Almelo': ['almeloos'], 'Sparta Rotterdam': ['rotterdams', 'spartaans'], 'Ajax': ['amsterdams'], 'De Graafschap': ['doetinchems'],
     'SC Cambuur Leeuwarden': ['fries']}

clubadjectiveprobs = {'PEC Zwolle': [0], 'N.E.C.': [0], 'ADO Den Haag': [0], 'Go Ahead Eagles': [0], 'FC Twente': [0],
     'Excelsior': [4, 10], 'FC Utrecht': [0], 'PSV': [0], 'Willem II': [0], 'Vitesse': [0], 'AZ': [0],
     'sc Heerenveen': [1, 40], 'FC Groningen': [0], 'Feyenoord': [0], 'Roda JC Kerkrade': [0],
     'Heracles Almelo': [0], 'Sparta Rotterdam': [2, 1], 'Ajax': [0], 'De Graafschap': [0],
     'SC Cambuur Leeuwarden': [0]}

clubdictprobs = {'PEC Zwolle': [2, 19, 58, 1, 1, 15], 'N.E.C.': [78, 9, 8, 1, 1], 'ADO Den Haag': [124, 4, 4, 1, 23],
     'Go Ahead Eagles': [34, 1, 6, 1, 1, 6], 'FC Twente': [67, 13, 1, 2, 1, 52], 'Excelsior': [6, 6, 1, 1, 97],
     'FC Utrecht': [71, 3, 3, 1, 1, 31], 'PSV': [7, 2, 1, 1, 2, 159], 'Willem II': [17, 4, 64], 'Vitesse': [6, 1, 101],
     'AZ': [9, 1, 1, 132], 'sc Heerenveen': [87, 1, 24, 12], 'FC Groningen': [66, 4, 30], 'Feyenoord': [9, 4, 114],
     'Roda JC Kerkrade': [22, 57, 5, 1, 6, 2, 0], 'Heracles Almelo': [56, 1, 3, 1, 4], 'Sparta Rotterdam': [51, 6, 2],
     'Ajax': [9, 1, 130], 'De Graafschap': [4, 1, 1, 49], 'SC Cambuur Leeuwarden': [61, 4, 1, 1, 2, 0]}

def convert_data(data):
    combinedlist = []

    for line in data:
        templist = []
        tags = re.findall(r'(\w+:)', line)
        data = []
        for idx, tag in enumerate(tags):
            if idx < len(tags) - 1:
                data.append(
                    re.search((re.escape(tags[idx])) + r'(.*?)' + (re.escape(tags[idx + 1])), line).group(1).strip())
            else:
                data.append(re.search((re.escape(tags[idx])) + r'(.*?)$', line).group(1).strip())

        tags = [re.sub(r':', '', x) for x in tags]
        for idx, tag in enumerate(tags):
            templist.append([tag, data[idx]])
        combinedlist.append(templist)
    return combinedlist

def fill_gaps(file, currentpath, clubdict, clubadjectivedict, clubadjectiveprobs, clubdictprobs):
    timeadjectivedict = {'1': 'een', '2': 'tweede', '3': 'derde', '4': 'vierde', '5': 'vijfde', '6': 'zesde', '7': 'zevende',
                         '8': 'achtste',
                         '9': 'negende', '10': 'tiende', '11': 'elfde', '12': 'twaalfde', '13': 'dertiende',
                         '14': 'veertiende',
                         '15': 'vijftiende', '16': 'zestiende', '17': 'zeventiende', '18': 'achtiende',
                         '19': 'negentiende',
                         '20': 'twintigste'}
    timeadverbdict = {'2': 'twee', '3': 'drie', '4': 'vier', '5': 'vijf', '6': 'zes', '7': 'zeven', '8': 'acht',
                      '9': 'negen', '10': 'tien', '11': 'elf', '12': 'twaalf', '13': 'dertien', '14': 'veertien',
                      '15': 'vijftien', '16': 'zestien', '17': 'zeventien', '18': 'achtien', '19': 'negentien',
                      '20': 'twintig'}

    with open(currentpath + '/Corpora/' + file + '.data', 'rb') as f:
        data = f.readlines()
    data = [x.decode('utf-8') for x in data]

    with open(currentpath + '/Corpora/Test_Retrieval_Gaps.txt', 'rb') as f:
        text = f.readlines()
    text = [x.decode('utf-8') for x in text]

    combinedlist = convert_data(data)
    for lineidx, line in enumerate(text):
        tempcombinedlist = []
        tempcombinedlistgaps = []
        text[lineidx] = text[lineidx].split()
        for wordidx, word in enumerate(text[lineidx]):
            if re.search(r'<(.*?)>', word):
                template = re.search(r'<(.*?)>', word).group(1)
                if template == 'goal_scorer':
                    plist = [3059, 2836]
                    plist = [float(i) / sum(plist) for i in plist]
                    datachoice = list(choice(['surname', 'fullname'], 1, p=plist))[0]
                    scorerfound = 'n'
                    if datachoice == 'surname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'GoalScorer_Surname':
                                scorerfound = 'y'
                                text[lineidx][wordidx] = tag[1]
                                break
                    elif datachoice == 'fullname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'GoalScorer_Name':
                                scorerfound = 'y'
                                text[lineidx][wordidx] = tag[1]
                                break
                    if scorerfound == 'n':
                        text[lineidx][wordidx] = 'de doelpuntenmaker'
                elif template == 'goal_scorer_position':
                    for tagidx, tag in enumerate(combinedlist[lineidx]):
                        if tag[0] == 'GoalScorer_Position':
                            position = tag[1]
                            break
                    if position == 'Forward':
                        plist = [4, 1, 62]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = list(choice(['vleugelaanvaller', 'rechteraanvaller', 'aanvaller'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                    elif position == 'Midfielder':
                        text[lineidx][wordidx] = 'middenvelder'
                    elif position == 'Defender':
                        plist = [18, 11, 2, 4, 1, 125]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = list(choice(['rechtsback', 'linksback', 'back', 'centrumverdediger', 'vleugelverdediger', 'verdediger'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                    elif position == 'Goalkeeper':
                        plist = [264, 96, 17]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = list(choice(['doelman', 'keeper', 'goalie'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                elif template == 'assist_giver':
                    plist = [360, 585]
                    plist = [float(i) / sum(plist) for i in plist]
                    datachoice = list(choice(['surname', 'fullname'], 1, p=plist))[0]
                    assistfound = 'n'
                    if datachoice == 'surname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'AssistGiver_Surname':
                                assistfound = 'y'
                                text[lineidx][wordidx] = tag[1]
                                break
                    elif datachoice == 'fullname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'AssistGiver_Name':
                                assistfound = 'y'
                                text[lineidx][wordidx] = tag[1]
                                break
                    if assistfound == 'n':
                        text[lineidx][wordidx] = 'zijn ploeggenoot'
                elif template == 'assist_giver_position':
                    for tagidx, tag in enumerate(combinedlist[lineidx]):
                        if tag[0] == 'AssistGiver_Position':
                            position = tag[1]
                            break
                    if position == 'Forward':
                        plist = [4, 1, 62]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = \
                        list(choice(['vleugelaanvaller', 'rechteraanvaller', 'aanvaller'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                    elif position == 'Midfielder':
                        text[lineidx][wordidx] = 'middenvelder'
                    elif position == 'Defender':
                        plist = [18, 11, 2, 4, 1, 125]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = list(choice(
                            ['rechtsback', 'linksback', 'back', 'centrumverdediger', 'vleugelverdediger',
                             'verdediger'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                    elif position == 'Goalkeeper':
                        plist = [264, 96, 17]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = list(choice(['doelman', 'keeper', 'goalie'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                elif template == 'time':
                    if (wordidx < len(text[lineidx]) - 2) and (text[lineidx][wordidx + 1] == 'minuten') and (text[lineidx][wordidx + 2] == 'later'):
                            for tagidx, tag in enumerate(combinedlist[lineidx]):
                                if tag[0] == 'TimeSinceGoal':
                                    if (int(tag[1]) <= 20) and (int(tag[1]) > 1):
                                        convertminute = timeadverbdict[tag[1]]
                                        text[lineidx][wordidx] = convertminute
                                    else:
                                        text[lineidx][wordidx] = tag[1]
                                    break
                                else:
                                    datachoice = choice(['twee', 'drie', 'vijf', 'tien'])
                                    text[lineidx][wordidx] = datachoice
                    elif ('minuut' not in line) and ('minuten' not in line):
                        quarterlist = [15, 30, 60, 75, 90]
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'Minute':
                                closest = min(quarterlist, key=lambda x: abs(x - int(tag[1])))
                                break
                        if closest == '15':
                            text[lineidx][wordidx] = 'een kwartier'
                        elif closest == '30':
                            plist = [28, 47]
                            plist = [float(i) / sum(plist) for i in plist]
                            datachoice = list(choice(['een halfuur', 'een half uur'], 1, p=plist))[0]
                            text[lineidx][wordidx] = datachoice
                        elif closest == '60':
                            text[lineidx][wordidx] = 'een uur'
                        elif closest == '75':
                            text[lineidx][wordidx] = 'het slotkwartier'
                        else:
                            if text[lineidx][wordidx-1] == 'in':
                                plist = [136, 156]
                                plist = [float(i) / sum(plist) for i in plist]
                                datachoice = list(choice(['blessuretijd', 'de slotfase'], 1, p=plist))[0]
                                text[lineidx][wordidx] = datachoice
                            else:
                                text[lineidx][wordidx] = 'vlak voor tijd'
                    elif 'minuut' in line:
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'Minute':
                                if (int(tag[1]) <= 20) and (int(tag[1]) > 0):
                                    newminute = timeadjectivedict[tag[1]]
                                    text[lineidx][wordidx] = str(newminute)
                                else:
                                    text[lineidx][wordidx] = tag[1]
                                break
                    elif 'minuten voor het einde' in line:
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'Minute':
                                resttime = 90 - int(tag[1])
                                if (resttime <= 20) and (resttime > 1):
                                    newminute = timeadverbdict[str(resttime)]
                                    text[lineidx][wordidx] = str(newminute)
                                else:
                                    text[lineidx][wordidx] = str(resttime)
                                break
                    elif 'minuten' in line:
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'Minute':
                                if (int(tag[1]) <= 20) and (int(tag[1]) > 1):
                                    newminute = timeadverbdict[tag[1]]
                                    text[lineidx][wordidx] = str(newminute)
                                else:
                                    text[lineidx][wordidx] = tag[1]
                                break
                    else:
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'Minute':
                                text[lineidx][wordidx] = tag[1]
                                break
                elif template == 'halftime':
                    if text[lineidx][wordidx - 1] == 'in':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if (tag[0] == 'Minute') and (int(tag[1]) <= 45):
                                text[lineidx][wordidx] = 'de eerste helft'
                                break
                            elif (tag[0] == 'Minute') and (int(tag[1]) > 45):
                                text[lineidx][wordidx] = 'de tweede helft'
                                break
                    else:
                        plist = [378, 8, 11, 44]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = list(choice(['rust', 'de thee', 'de theepauze', 'de pauze'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                elif template == 'score':
                    for tagidx, tag in enumerate(combinedlist[lineidx]):
                        if tag[0] == 'Score':
                            text[lineidx][wordidx] = tag[1]
                            break
                elif template == 'team':
                    if (text[lineidx][wordidx - 1] == 'een') or (text[lineidx][wordidx - 1] == 'de') or (text[lineidx][wordidx - 1] == 'het'):
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'Team':
                                teamname = re.search(r'^(.*?) \;', tag[1]).group(1)
                                clubadjective = clubadjectivedict[teamname]
                                if len(clubadjective) == 1:
                                    if (text[lineidx][wordidx - 1] == 'de') or (text[lineidx][wordidx - 1] == 'het'):
                                        if clubadjective[0] != 'almeloos':
                                            text[lineidx][wordidx] = clubadjective[0] + 'e'
                                        else:
                                            text[lineidx][wordidx] = 'almelose'
                                    else:
                                        text[lineidx][wordidx] = clubadjective[0]
                                else:
                                    cap = clubadjectiveprobs[teamname]
                                    for capidx, capval in enumerate(cap):
                                        if capval == 0:
                                            del cap[capidx]
                                            del clubadjective[capidx]
                                    plist = [float(i) / sum(cap) for i in cap]
                                    datachoice = list(choice(clubadjective, 1, p=plist))[0]
                                    if (text[lineidx][wordidx - 1] == 'de') or (text[lineidx][wordidx - 1] == 'het'):
                                        if clubadjective[0] != 'almeloos':
                                            text[lineidx][wordidx] = clubadjective[0] + 'e'
                                        else:
                                            text[lineidx][wordidx] = 'almelose'
                                    else:
                                        text[lineidx][wordidx] = datachoice
                                break
                    else:
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'Team':
                                teamname = re.search(r'^(.*?) \;', tag[1]).group(1)
                                club = clubdict[teamname] + [teamname.lower()]
                                clubprobs = clubdictprobs[teamname]
                                plist = [float(i) / sum(clubprobs) for i in clubprobs]
                                datachoice = list(choice(club, 1, p=plist))[0]
                                text[lineidx][wordidx] = datachoice
                                break
                elif template == 'other_team':
                    if (text[lineidx][wordidx - 1] == 'een') or (text[lineidx][wordidx - 1] == 'de') or (text[lineidx][wordidx - 1] == 'het'):
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'OtherTeam':
                                teamname = re.search(r'^(.*?) \;', tag[1]).group(1)
                                clubadjective = clubadjectivedict[teamname]
                                if len(clubadjective) == 1:
                                    if (text[lineidx][wordidx - 1] == 'de') or (text[lineidx][wordidx - 1] == 'het'):
                                        text[lineidx][wordidx] = clubadjective[0] + 'e'
                                    else:
                                        text[lineidx][wordidx] = clubadjective[0]
                                else:
                                    cap = clubadjectiveprobs[teamname]
                                    for capidx, capval in enumerate(cap):
                                        if capval == 0:
                                            del cap[capidx]
                                            del clubadjective[capidx]
                                    plist = [float(i) / sum(cap) for i in cap]
                                    datachoice = list(choice(clubadjective, 1, p=plist))[0]
                                    if (text[lineidx][wordidx - 1] == 'de') or (text[lineidx][wordidx - 1] == 'het'):
                                        text[lineidx][wordidx] = datachoice + 'e'
                                    else:
                                        text[lineidx][wordidx] = datachoice
                                break
                    else:
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'OtherTeam':
                                teamname = re.search(r'^(.*?) \;', tag[1]).group(1)
                                club = clubdict[teamname] + [teamname.lower()]
                                clubprobs = clubdictprobs[teamname]
                                plist = [float(i) / sum(clubprobs) for i in clubprobs]
                                datachoice = list(choice(club, 1, p=plist))[0]
                                text[lineidx][wordidx] = datachoice
                                break
                elif template == 'goalkeeper':
                    plist = [1313, 441]
                    plist = [float(i) / sum(plist) for i in plist]
                    datachoice = list(choice(['surname', 'fullname'], 1, p=plist))[0]
                    plist = [1, 1, 1, 3]
                    plist = [float(i) / sum(plist) for i in plist]
                    prefix = list(choice(['doelman ', 'keeper ', 'goalie ', ''], 1, p=plist))[0]
                    text[lineidx][wordidx] = datachoice
                    if datachoice == 'surname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'GoalKeeperTeamSurname':
                                text[lineidx][wordidx] = prefix + tag[1]
                                break
                    elif datachoice == 'fullname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'GoalKeeperTeamName':
                                text[lineidx][wordidx] = prefix + tag[1]
                                break
                elif template == 'goalkeeper_other_team':
                    plist = [1486, 742]
                    plist = [float(i) / sum(plist) for i in plist]
                    datachoice = list(choice(['surname', 'fullname'], 1, p=plist))[0]
                    plist = [1, 1, 1, 3]
                    plist = [float(i) / sum(plist) for i in plist]
                    prefix = list(choice(['doelman ', 'keeper ', 'goalie ', ''], 1, p=plist))[0]
                    text[lineidx][wordidx] = datachoice
                    if datachoice == 'surname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'GoalKeeperOtherTeamSurname':
                                text[lineidx][wordidx] = prefix + tag[1]
                                break
                    elif datachoice == 'fullname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'GoalKeeperOtherTeamName':
                                text[lineidx][wordidx] = prefix + tag[1]
                                break
                elif template == 'foul_committed':
                    plist = [30, 100]
                    plist = [float(i) / sum(plist) for i in plist]
                    datachoice = list(choice(['surname', 'fullname'], 1, p=plist))[0]
                    if datachoice == 'surname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'FoulCommitted_Player_Surname':
                                text[lineidx][wordidx] = tag[1]
                                break
                    elif datachoice == 'fullname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'FoulCommitted_Player_Name':
                                text[lineidx][wordidx] = tag[1]
                                break
                elif template == 'foul_committed_position':
                    for tagidx, tag in enumerate(combinedlist[lineidx]):
                        if tag[0] == 'FoulCommitted_Player_Position':
                            position = tag[1]
                            break
                    if position == 'Forward':
                        plist = [4, 1, 62]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = \
                        list(choice(['vleugelaanvaller', 'rechteraanvaller', 'aanvaller'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                    elif position == 'Midfielder':
                        text[lineidx][wordidx] = 'middenvelder'
                    elif position == 'Defender':
                        plist = [18, 11, 2, 4, 1, 125]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = list(choice(
                            ['rechtsback', 'linksback', 'back', 'centrumverdediger', 'vleugelverdediger',
                             'verdediger'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                    elif position == 'Goalkeeper':
                        plist = [264, 96, 17]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = list(choice(['doelman', 'keeper', 'goalie'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice

                elif template == 'foul_suffered':
                    plist = [30, 100]
                    plist = [float(i) / sum(plist) for i in plist]
                    datachoice = list(choice(['surname', 'fullname'], 1, p=plist))[0]
                    if datachoice == 'surname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'FoulSuffered_Player_Surname':
                                text[lineidx][wordidx] = tag[1]
                                break
                    elif datachoice == 'fullname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'FoulSuffered_Player_Name':
                                text[lineidx][wordidx] = tag[1]
                                break
                elif template == 'foul_suffered_position':
                    for tagidx, tag in enumerate(combinedlist[lineidx]):
                        if tag[0] == 'FoulSuffered_Player_Position':
                            position = tag[1]
                            break
                    if position == 'Forward':
                        plist = [4, 1, 62]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = \
                        list(choice(['vleugelaanvaller', 'rechteraanvaller', 'aanvaller'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                    elif position == 'Midfielder':
                        text[lineidx][wordidx] = 'middenvelder'
                    elif position == 'Defender':
                        plist = [18, 11, 2, 4, 1, 125]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = list(choice(
                            ['rechtsback', 'linksback', 'back', 'centrumverdediger', 'vleugelverdediger',
                             'verdediger'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                    elif position == 'Goalkeeper':
                        plist = [264, 96, 17]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = list(choice(['doelman', 'keeper', 'goalie'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice

                elif template == 'card_player':
                    plist = [30, 100]
                    plist = [float(i) / sum(plist) for i in plist]
                    datachoice = list(choice(['surname', 'fullname'], 1, p=plist))[0]
                    if datachoice == 'surname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'CardPlayer_Surname':
                                text[lineidx][wordidx] = tag[1]
                                break
                    elif datachoice == 'fullname':
                        for tagidx, tag in enumerate(combinedlist[lineidx]):
                            if tag[0] == 'CardPlayer_Name':
                                text[lineidx][wordidx] = tag[1]
                                break
                elif template == 'card_player_position':
                    for tagidx, tag in enumerate(combinedlist[lineidx]):
                        if tag[0] == 'CardPlayer_Position':
                            position = tag[1]
                            break
                    if position == 'Forward':
                        plist = [4, 1, 62]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = \
                        list(choice(['vleugelaanvaller', 'rechteraanvaller', 'aanvaller'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                    elif position == 'Midfielder':
                        text[lineidx][wordidx] = 'middenvelder'
                    elif position == 'Defender':
                        plist = [18, 11, 2, 4, 1, 125]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = list(choice(
                            ['rechtsback', 'linksback', 'back', 'centrumverdediger', 'vleugelverdediger',
                             'verdediger'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice
                    elif position == 'Goalkeeper':
                        plist = [264, 96, 17]
                        plist = [float(i) / sum(plist) for i in plist]
                        datachoice = list(choice(['doelman', 'keeper', 'goalie'], 1, p=plist))[0]
                        text[lineidx][wordidx] = datachoice

    for lineidx, line in enumerate(text):
        text[lineidx] = ' '.join(text[lineidx])

    return text


currentpath = os.getcwd()
for file in ['Test']:
    text = fill_gaps(file, currentpath, clubdict, clubadjectivedict, clubadjectiveprobs, clubdictprobs)
    text = '\n'.join(text)
    with open(currentpath + '/Corpora/' + file + '_gaps_filled_Retrieval.text', 'wb') as f:
        f.write(bytes(text, 'UTF-8'))