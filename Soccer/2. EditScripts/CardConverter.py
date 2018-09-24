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
    cards = soup.find('cards').find_all('event') #Find all cards in the data
    cards = sorted(cards, key=lambda goal: int(goal['mins']))

    previousplayers = []
    newcards = []
    for idx, card in enumerate(cards): #If a player got a yellow and then a second one (or a direct red card), the sentence is highly likely to be about the 2nd yellow or red, not the first yellow, so remove the first yellow from the events.
        newcards.append(card) #Add the event to the new list
        try:
            cardplayer = playerdict[card['player_id']][0] #Find the carded player
        except KeyError:
            cardplayer = ''
        if ((card.find('card').text.strip() == 'red') or (card.find('card').text.strip() == '2nd yellow')) and (cardplayer in previousplayers): #If the card is a 2nd yellow or red and the cardplayer has previously received a yellow
            previousplayers_index = previousplayers.index(cardplayer) #Find which event describes his first yellow
            del newcards[previousplayers_index] #And delete this event from the list
            del previousplayers[previousplayers_index]
        previousplayers.append(cardplayer)


    cardsentencelist = []
    corsentlist = []
    for idx, card in enumerate(newcards): #Obtain the data representation and corresponding sentences for cards
        infosentencelist, corresponding_sentences = cardtransform(idx, card, teams, playerdict, textslist)
        cardsentencelist.extend(infosentencelist)
        corsentlist.extend(corresponding_sentences)

    return cardsentencelist, corsentlist

def cardtransform(idx, card, teams, playerdict, textslist):
    playerid = card['player_id']
    try:
        cardplayer = playerdict[playerid][0]
        cardsurname = playerdict[playerid][1]
        cardposition = playerdict[playerid][3]
    except KeyError:
        return [], []
    teamid = card['team']
    for team in teams: #Get information on the current team and the other team
        if teamid == team[0]:
            currentteam = team[1]
            currenthomeaway = team[2]
        else:
            otherteam = team[1]
            otherhomeaway = team[2]
    time = card['mins']
    id = str(idx + 1)

    cardtype = card.find('card').text.strip()
    infosentence = 'CardPlayer_Name: ' + cardplayer + ' CardPlayer_Surname: ' + cardsurname + ' CardPlayer_Position: ' + cardposition + ' Minute: ' + time + ' CardType: ' + cardtype + ' CardID: ' + id + ' Team: ' + currentteam + ' ; ' + currenthomeaway + ' OtherTeam: ' + otherteam + ' ; ' + otherhomeaway
    corresponding_sentences = sentencefinder(textslist, cardplayer, cardsurname, currentteam, otherteam, playerdict, time)
    infosentencelist = [infosentence] * len(corresponding_sentences)
    return infosentencelist, corresponding_sentences

def sentencefinder(textslist, player, surname, team, otherteam, playerdict, time):
    goalsentences = []
    if len(surname.split()) > 1:
        surname = surname.split()[-1]

    playerlist = []
    for playerid in playerdict:
        otherplayer = playerdict[playerid][1]
        if len(otherplayer.split()) > 1:
            otherplayer = otherplayer.split()[-1]
        if otherplayer != surname:
            playerlist.append(otherplayer)

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
            if (re.search(r'\b' + re.escape(surname) + r'\b', sentence, re.IGNORECASE)) and (re.search(r'(\bkaart\b)|(\bprent\b)|(\bgeel\b)|(\bgele\b)|(\brood\b)|(\brode\b)', sentence, re.IGNORECASE)) and not (re.search(r'\d+\-\d+', sentence, re.IGNORECASE)): #Cards
                for othersurname in playerlist:
                    if re.search(re.escape(othersurname), sentence, re.IGNORECASE):
                        otherplayers = 'y'
                        break

                if (otherplayers == 'n') and (len(sentence.split()) <= 30) and (len(sentence.split()) >= 5):
                    relevantsentences.append(sentence)
                #sentence = sentence.replace(player.lower(), '<goal_scorer>')
                #sentence = sentence.replace(surname.lower(), '<goal_scorer>')
                #sentence = sentence.replace(team.lower(), '<team>')
                #sentence = sentence.replace(score, '<score>')
                #sentence = re.sub(r'\d+\-\d+', '<score>', sentence)
                #sentence = sentence.replace(otherteam.lower(), '<other_team>')

        goalsentences.extend(relevantsentences)

    # Remove sentences that are the same
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


with open(currentpath + '/Corpora/Cards.data', 'wb') as f:
    f.write(bytes(goalsentencetext, 'UTF-8'))

with open(currentpath + '/Corpora/Cards.text', 'wb') as f:
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