import xlrd
import xlwt
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlwt import easyxf # http://pypi.python.org/pypi/xlwt
import regex as re
import os
import sys
from bs4 import BeautifulSoup
import nltk
from sklearn.model_selection import train_test_split
import ast

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def excelread(file):
    #Linklist contains lists of links, each list contains the squawka-file first and then the match reports
    linklist = []
    workbook = xlrd.open_workbook(file)
    worksheets = workbook.sheet_names()
    # Open the excel file
    worksheet = workbook.sheet_by_name(worksheets[0])
    num_rows = worksheet.nrows
    #Start at the first row
    for idx in range(1, num_rows):
        row = worksheet.row(idx)
        #If there is a corresponding data file, get that file and the texts
        if worksheet.cell_value(idx, 5) != '':
            currentlist = []
            #Add an entry that indicates which database is used (and make it so that you only get the filename without extension, that's easiest)
            currentlist.append(os.path.splitext(os.path.basename(file))[0])
            #First entry in the currentlist is always the squawka-file
            currentlist.append(worksheet.cell_value(idx, 5))
            #List with all the values of the columns where a text file link can be
            columnlist = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39]
            for column in columnlist:
                if worksheet.cell_value(idx, column) != '-':
                    currentlist.append(worksheet.cell_value(idx, column))
            linklist.append(currentlist)
    return linklist

def teaminfo(soup):
    #Return the information from the squawka file on the teams
    teams = soup.find('game').find_all('team')
    homeawaylist = []
    for team in teams:
        teamid = team['id']
        name = team.find('long_name').text
        name = re.sub(r'^\n\s+', '', name)
        name = re.sub(r'\n\s+$', '', name)
        homeaway = team.find('state').text
        homeaway = re.sub(r'^\n\s+', '', homeaway)
        homeaway = re.sub(r'\n\s+$', '', homeaway)
        homeawaylist.append((teamid, name, homeaway))
    return homeawaylist

def playerinfo(soup, teams):
    #Return a dictionary continaing all players' info
    players = soup.find('players').find_all('player')
    playerdict = {}
    for player in players:
        playerid = player['id']
        name = player.find('name').text
        name = re.sub(r'^\n\s+', '', name)
        name = re.sub(r'\n\s+$', '', name)
        teamid = player['team_id']
        for team in teams:  # Get the information about the team of the player
            if teamid == team[0]:
                team = team[1]
                break
        surname = player.find('surname').text
        surname = re.sub(r'^\n\s+', '', surname)
        surname = re.sub(r'\n\s+$', '', surname)
        position = player.find('position').text
        position = re.sub(r'^\n\s+', '', position)
        position = re.sub(r'\n\s+$', '', position)
        startingsub = player.find('state').text
        startingsub = re.sub(r'^\n\s+', '', startingsub)
        startingsub = re.sub(r'\n\s+$', '', startingsub)
        playerdict.update({playerid: [name, surname, team, position, startingsub]})
    return playerdict

def gettexts(textlinkcluster, database):
    #Load all the texts
    textslist = []
    #Textlinkcluster are the filenames, database is e.g. 'eredivisie16-17', a prefix for the folder
    for textlink in textlinkcluster:
        currentpath = os.getcwd()
        with open(os.path.dirname(os.path.dirname(currentpath)) + '/Newspaper Corpus/Corpus/' + database + '/' + textlink, encoding='utf-8') as f:
            text = f.read()
            textslist.append(text)
    return textslist

def squawkagoals(singlecluster):
    #Obtain the texts with the text filenames ([2:]) and the season information ([0], e.g. Eredivisie16-17)
    textslist = gettexts(singlecluster[2:], singlecluster[0])
    currentpath = os.getcwd()
    #Open the Squawka file containing the data
    soup = BeautifulSoup(open(os.path.dirname(os.path.dirname(currentpath)) + '/Newspaper Corpus/Squawka stats/' + singlecluster[0] + '/' + singlecluster[1], 'rb'), "xml")
    teams = teaminfo(soup) #Get the teams
    playerdict = playerinfo(soup, teams) #And the players
    goals = soup.find_all('event', {"type": "goal"}) #Find all goals in the data
    goals = sorted(goals, key=lambda goal: int(goal['mins']))
    homegoals = 0
    awaygoals = 0
    goalsentencelist = []
    corsentlist = []
    for idx, goal in enumerate(goals): #Obtain the data representation and corresponding sentences for goals
        if idx == 0:
            infosentencelist, homegoals, awaygoals, corresponding_sentences = goaltransform(idx, goal, homegoals, awaygoals, teams, playerdict, textslist, '')
        else:
            infosentencelist, homegoals, awaygoals, corresponding_sentences = goaltransform(idx, goal, homegoals,
                                                                                            awaygoals, teams,
                                                                                            playerdict, textslist, goals[idx-1])
        goalsentencelist.extend(infosentencelist)
        corsentlist.extend(corresponding_sentences)

    return goalsentencelist, corsentlist

def goaltransform(idx, goal, homegoals, awaygoals, teams, playerdict, textslist, previousgoal):
    playerid = goal['player_id']
    goalplayer = playerdict[playerid][0]
    goalsurname = playerdict[playerid][1]
    goalposition = playerdict[playerid][3]
    teamid = goal['team_id']
    for team in teams: #Get the score and the information which team scored the goal
        if teamid == team[0]:
            if team[2] == 'home':
                homegoals += 1
            elif team[2] == 'away':
                awaygoals += 1
            score = str(homegoals) + "-" + str(awaygoals)
            currentteam = team[1]
            currenthomeaway = team[2]
        else:
            otherteam = team[1]
            otherhomeaway = team[2]
    time = goal['mins']
    if previousgoal == '':
        timesincegoal = str(0)
    else:
        prevtime = previousgoal['mins']
        timesincegoal = str(int(time) - int(prevtime))
    id = str(idx + 1)

    goaltype = 'RegularGoal'
    assist = 'n'
    passlinks = goal.find('passlinks').text.strip()

    passlinkslist = [] #Convert the passlinks list manually to the list of dicts that it is (ast.literal_eval doesn't work all the time)
    passlinks = re.sub(r'((\[)|(\]))', '', passlinks)
    passlinks = passlinks.split('},{')
    passlinks = [re.sub(r'((\{)|(\}))', '', x) for x in passlinks]
    passlinks = [x.split(',"') for x in passlinks]
    for idx, val in enumerate(passlinks):
        partdict = {}
        passlinks[idx] = [x.split(':') for x in passlinks[idx]]
        for idx2, val2 in enumerate(passlinks[idx]):
            passlinks[idx][idx2] = [x.replace('"', '') for x in passlinks[idx][idx2]]
            partdict.update({passlinks[idx][idx2][0]: passlinks[idx][idx2][1]})
        passlinkslist.append(partdict)

    for passlinkdict in passlinkslist: #See if the goal is a regular goal or an own goal/penalty goal
        if (passlinkdict['type'] == 'goal') and (passlinkdict['is_own'] == "1"):
            goaltype = 'OwnGoal'
        elif (passlinkdict['type'] == 'goal') and (passlinkdict['penalty_goal'] == "1"): #If the goal is a penalty, also get the reason
            goaltype = 'PenaltyGoal'
            reason = passlinkdict['reason']
            foulcommittedplayername = passlinkdict['foulcommitted_player'] #And the players involved in the penalty
            foulcommittedplayersurname = foulcommittedplayername
            foulcommittedplayerposition = 'n'
            for posplayer in playerdict: #Try to find the players in the playerdict
                if re.search(r'\b' + re.escape(foulcommittedplayername) + r'\b', playerdict[posplayer][1]):
                    foulcommittedplayername = playerdict[posplayer][0]
                    foulcommittedplayersurname = playerdict[posplayer][1]
                    foulcommittedplayerposition = playerdict[posplayer][3]
                    break
                elif re.search(r'\b' + re.escape(foulcommittedplayername) + r'\b', playerdict[posplayer][0]):
                    foulcommittedplayername = playerdict[posplayer][0]
                    foulcommittedplayersurname = playerdict[posplayer][1]
                    foulcommittedplayerposition = playerdict[posplayer][3]
                    break
            foulsufferedplayername = passlinkdict['foulsuffered_player']
            foulsufferedplayersurname = foulsufferedplayername
            foulsufferedplayerposition = 'n'
            for posplayer in playerdict:
                if re.search(r'\b' + re.escape(foulsufferedplayername) + r'\b', playerdict[posplayer][1]):
                    foulsufferedplayername = playerdict[posplayer][0]
                    foulsufferedplayersurname = playerdict[posplayer][1]
                    foulsufferedplayerposition = playerdict[posplayer][3]
                    break
                elif re.search(r'\b' + re.escape(foulsufferedplayername) + r'\b', playerdict[posplayer][0]):
                    foulsufferedplayername = playerdict[posplayer][0]
                    foulsufferedplayersurname = playerdict[posplayer][1]
                    foulsufferedplayerposition = playerdict[posplayer][3]
                    break
        if (passlinkdict['type'] == 'assists_pass') and (passlinkdict['player_id'] != '0'):
            assist = 'y'
            assistid = passlinkdict['player_id']
            assistplayer = playerdict[assistid][0]
            assistsurname = playerdict[assistid][1]
            assistposition = playerdict[assistid][3]

    goalkeepercurrentname = ''
    goalkeepercurrentsurname = ''
    goalkeeperothername = ''
    goalkeeperothersurname = ''
    for player in playerdict:
        if (playerdict[player][2] == currentteam) and (playerdict[player][3] == 'Goalkeeper') and (playerdict[player][4] == 'playing'):
            goalkeepercurrentname = playerdict[player][0]
            goalkeepercurrentsurname = playerdict[player][1]
        elif (playerdict[player][2] == otherteam) and (playerdict[player][3] == 'Goalkeeper') and (playerdict[player][4] == 'playing'):
            goalkeeperothername = playerdict[player][0]
            goalkeeperothersurname = playerdict[player][1]

    #infosentence = 'goal <goal_scorer>' + ' time ' + time + ' team <team>' + ' id ' + id + ' score ' + score
    if assist == 'n':
        infosentence = 'GoalScorer_Name: ' + goalplayer + ' GoalScorer_Surname: ' + goalsurname + ' GoalScorer_Position: ' + goalposition + ' Minute: ' + time + ' TimeSinceGoal: ' + timesincegoal + ' GoalType: ' + goaltype + ' GoalID: ' + id + ' Score: ' + score + ' Team: ' + currentteam + ' ; ' + currenthomeaway + ' OtherTeam: ' + otherteam + ' ; ' + otherhomeaway + ' GoalKeeperTeamName: ' + goalkeepercurrentname + ' GoalKeeperTeamSurname: ' + goalkeepercurrentsurname + ' GoalKeeperOtherTeamName: ' + goalkeeperothername + ' GoalKeeperOtherTeamSurname: ' + goalkeeperothersurname
        corresponding_sentences = sentencefinder(textslist, goalplayer, goalsurname, '', '', '', goalkeepercurrentsurname, goalkeeperothersurname, currentteam, score, otherteam, playerdict, time)
    elif assist == 'y':
        infosentence = 'GoalScorer_Name: ' + goalplayer + ' GoalScorer_Surname: ' + goalsurname + ' GoalScorer_Position: ' + goalposition + ' AssistGiver_Name: ' + assistplayer + ' AssistGiver_Surname: ' + assistsurname + ' AssistGiver_Position: ' + assistposition + ' Minute: ' + time + ' TimeSinceGoal: ' + timesincegoal + ' GoalType: ' + goaltype + ' GoalID: ' + id + ' Score: ' + score + ' Team: ' + currentteam + ' ; ' + currenthomeaway + ' OtherTeam: ' + otherteam + ' ; ' + otherhomeaway + ' GoalKeeperTeamName: ' + goalkeepercurrentname + ' GoalKeeperTeamSurname: ' + goalkeepercurrentsurname + ' GoalKeeperOtherTeamName: ' + goalkeeperothername + ' GoalKeeperOtherTeamSurname: ' + goalkeeperothersurname
        corresponding_sentences = sentencefinder(textslist, goalplayer, goalsurname, assistsurname, '', '', goalkeepercurrentsurname, goalkeeperothersurname,
                                                 currentteam, score, otherteam, playerdict, time)
    if goaltype == 'PenaltyGoal':
        infosentence += ' PenaltyReason: ' + reason + ' FoulCommitted_Player_Name: ' + foulcommittedplayername + ' FoulCommitted_Player_Surname: ' + foulcommittedplayersurname + ' FoulCommitted_Player_Position: ' + foulcommittedplayerposition + ' FoulSuffered_Player_Name: ' + foulsufferedplayername + ' FoulSuffered_Player_Surname: ' + foulsufferedplayersurname + ' FoulSuffered_Player_Position: ' + foulsufferedplayerposition
        if assist == 'y':
            corresponding_sentences = sentencefinder(textslist, goalplayer, goalsurname, assistsurname, foulcommittedplayersurname, foulsufferedplayersurname, goalkeepercurrentsurname,
                                                 goalkeeperothersurname,
                                                 currentteam, score, otherteam, playerdict, time)
        else:
            corresponding_sentences = sentencefinder(textslist, goalplayer, goalsurname, '', foulcommittedplayersurname,
                                                     foulsufferedplayersurname, goalkeepercurrentsurname,
                                                     goalkeeperothersurname,
                                                     currentteam, score, otherteam, playerdict, time)
    #infosentence = time + ' ' + score
    #corresponding_sentences = sentencefinder(textslist, goalplayer, goalsurname, currentteam, score, otherteam, playerdict)
    infosentencelist = [infosentence] * len(corresponding_sentences)
    return infosentencelist, homegoals, awaygoals, corresponding_sentences

def sentencefinder(textslist, player, surname, assistsurname, foulcommittedplayersurname, foulsufferedplayersurname, goalkeepercurrentsurname, goalkeeperothersurname, team, score, otherteam, playerdict, time):
    goalsentences = []
    if len(surname.split()) > 1:
        surname = surname.split()[-1]
    if len(assistsurname.split()) > 1:
        assistsurname = assistsurname.split()[-1]
    if len(foulcommittedplayersurname.split()) > 1:
        foulcommittedplayersurname = foulcommittedplayersurname.split()[-1]
    if len(foulsufferedplayersurname.split()) > 1:
        foulsufferedplayersurname = foulsufferedplayersurname.split()[-1]
    if len(goalkeepercurrentsurname.split()) > 1:
        goalkeepercurrentsurname = goalkeepercurrentsurname.split()[-1]
    if len(goalkeeperothersurname.split()) > 1:
        goalkeeperothersurname = goalkeeperothersurname.split()[-1]

    playerlist = []
    for playerid in playerdict:
        otherplayer = playerdict[playerid][1]
        if len(otherplayer.split()) > 1:
            otherplayer = otherplayer.split()[-1]
        if (otherplayer != surname) and (otherplayer != assistsurname) and (otherplayer != foulcommittedplayersurname) \
                and (otherplayer != foulsufferedplayersurname) and (otherplayer != goalkeepercurrentsurname) and (
                otherplayer != goalkeeperothersurname):
            playerlist.append(otherplayer)

    newscore = re.sub(r'(\d+)\-(\d+)', r'\g<2>-\g<1>', score)

    for text in textslist:
        relevantsentences = []
        sentences = nltk.sent_tokenize(text)
        for idx, sentence in enumerate(sentences):
            if idx <= 1:
                continue
            words = nltk.word_tokenize(sentence)
            for idx, word in enumerate(words):
                words[idx] = word.lower()

            sentence = ' '.join(words)

            otherplayers = 'n'

            if (re.search(r'\b' + re.escape(surname) + r'\b', sentence, re.IGNORECASE)) and (re.search(r'(\bgoal\b)|(\btreffer\b)|(\braak\b)|(\bschoot\b)|(\bschiet\b)|(\bdoel\b)|(\bdoelpunt\b)|(\bnet(ten)?\b)|(\btouw(en)?\b)|(\bwinkelhaak\b)|(\b' + re.escape(score) + r'\b)|(\b' + re.escape(newscore) + r'\b)|(\bpenalty\b)|(\bpingel\b)|(\bstrafschop\b)|(stip\b)|(\bbuitenkans)|(elf\s?meter)', sentence, re.IGNORECASE)): #Goals
                for othersurname in playerlist:
                    if re.search(re.escape(othersurname), sentence, re.IGNORECASE):
                        otherplayers = 'y'
                        break
                allscores = re.findall(r'\d+\-\d+', sentence)
                otherscores = 'n'
                for goal in allscores:
                    if (goal != score) and (goal != newscore):
                        otherscores = 'y'
                alltimes = re.findall(r'\d\d', sentence)
                othertimes = 'n'
                timeoptions = [str(int(time) - 2), str(int(time) - 1), time, str(int(time) + 1),
                                 str(int(time) + 2)]
                for minute in alltimes:
                    if minute not in timeoptions:
                        othertimes = 'y'
                if (otherplayers == 'n') and (otherscores == 'n') and (othertimes == 'n') and (len(sentence.split()) <= 30) and (len(sentence.split()) >= 5):
                    relevantsentences.append(sentence)


                #sentence = sentence.replace(player.lower(), '<goal_scorer>')
                #sentence = sentence.replace(surname.lower(), '<goal_scorer>')
                #sentence = sentence.replace(team.lower(), '<team>')
                #sentence = sentence.replace(score, '<score>')
                #sentence = re.sub(r'\d+\-\d+', '<score>', sentence)
                #sentence = sentence.replace(otherteam.lower(), '<other_team>')



        goalsentences.extend(relevantsentences)
    #Remove sentences that are the same
    goalsentences = remove_duplicates(goalsentences)
    return goalsentences

currentpath = os.getcwd()

linklist = excelread(os.path.dirname(os.path.dirname(currentpath)) + '/Newspaper Corpus/Corpus/Metadata/Eredivisie16-17.xls')
linklist2 = excelread(os.path.dirname(os.path.dirname(currentpath)) + '/Newspaper Corpus//Corpus/Metadata/Eredivisie15-16.xls')
linklist.extend(linklist2)

fullgoalsentencelist = []
fullcorresponding_sentences = []

for idx, linkcluster in enumerate(linklist):
    if idx % 100 == 0:
        print(idx)
    goalsentencelist, corresponding_sentences = squawkagoals(linkcluster)
    fullgoalsentencelist.extend(goalsentencelist)
    fullcorresponding_sentences.extend(corresponding_sentences)
    #goaltext = goaltransform(goalinfo)

goalsentencetext = '\n'.join(fullgoalsentencelist)
corresponding_sentencestext = '\n'.join(fullcorresponding_sentences)
#print(goalsentencetext)


with open(currentpath + '/Corpora/Goals.data', 'wb') as f:
    f.write(bytes(goalsentencetext, 'UTF-8'))

with open(currentpath + '/Corpora/Goals.text', 'wb') as f:
    f.write(bytes(corresponding_sentencestext, 'UTF-8'))
'''
data_train, data_test, text_train, text_test = train_test_split(fullgoalsentencelist, fullcorresponding_sentences, test_size=0.2, random_state=42)
data_dev, data_test, text_dev, text_test = train_test_split(data_test, text_test, test_size=0.5, random_state=42)


data_train_text = '\n'.join(data_train)
text_train_text = '\n'.join(text_train)
data_dev_text = '\n'.join(data_dev)
text_dev_text = '\n'.join(text_dev)
data_test_text = '\n'.join(data_test)
text_test_text = '\n'.join(text_test)

with open('C:/Syncmap/Promotie/Newspaper Corpus/Moses training/Train.data', 'wb') as f:
    f.write(bytes(data_train_text, 'UTF-8'))

with open('C:/Syncmap/Promotie/Newspaper Corpus/Moses training/Train.text', 'wb') as f:
    f.write(bytes(text_train_text, 'UTF-8'))

with open('C:/Syncmap/Promotie/Newspaper Corpus/Moses training/Dev.data', 'wb') as f:
    f.write(bytes(data_dev_text, 'UTF-8'))

with open('C:/Syncmap/Promotie/Newspaper Corpus/Moses training/Dev.text', 'wb') as f:
    f.write(bytes(text_dev_text, 'UTF-8'))

with open('C:/Syncmap/Promotie/Newspaper Corpus/Moses training/Test.data', 'wb') as f:
    f.write(bytes(data_test_text, 'UTF-8'))

with open('C:/Syncmap/Promotie/Newspaper Corpus/Moses training/Test.text', 'wb') as f:
    f.write(bytes(text_test_text, 'UTF-8'))
'''