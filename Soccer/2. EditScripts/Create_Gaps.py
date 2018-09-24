import os
import regex as re
import sys

clubdict = {'PEC Zwolle': ['de zwollenaren', 'zwolle', 'pec', 'de equipe uit overijssel'], 'N.E.C.': ['nec nijmegen', 'n.e.c. nijmegen', 'nec', 'de nijmegenaren', 'nijmegen'], 'ADO Den Haag': ['ado', 'de hagenaars', 'den haag', 'de club uit den haag'],
     'Go Ahead Eagles': ['go ahead', 'de deventenaren', 'de eagles', 'eagles', 'the eagles'], 'FC Twente': ['Twente', 'de tukkers', 'de club uit enschede', 'de enschedeërs', 'de twentenaren'],
     'Excelsior': ['de kralingers', 'excelsior rotterdam', 'de rotterdammers'], 'FC Utrecht': ['utrecht', 'de utrechters', 'de domstedelingen'], 'PSV': ['de eindhovenaren', 'de club uit eindhoven', 'de ploeg uit eindhoven'],
     'Willem II': ['de tilburgers', 'de tricolores', 'de club uit tilburg'], 'Vitesse': ['de arnhemmers', 'de arnhemse equipe'], 'AZ': ['de club uit alkmaar', 'de alkmaarders'],
     'sc Heerenveen': ['heerenveen', 'de club uit heerenveen', 'de friezen'], 'FC Groningen': ['groningen', 'de groningers', 'de trots van het noorden'],
     'Feyenoord': ['de rotterdammers'], 'Roda JC Kerkrade': ['roda jc', 'roda', 'kerkrade', 'de club uit kerkrade', 'de ploeg uit kerkrade', 'de limburgers'],
     'Heracles Almelo': ['heracles', 'de almeloërs', 'de heraclieden', 'de club uit almelo'], 'Sparta Rotterdam': ['de kasteelheren', 'sparta', 'de rotterdammers', 'de spartanen'],
     'Ajax': ['de amsterdammers', 'de club uit amsterdam', 'de ajacieden'], 'De Graafschap': ['de superboeren', 'de doetinchemmers', 'de ploeg uit doetinchem', 'de achterhoekers', 'graafschap'],
     'SC Cambuur Leeuwarden': ['cambuur', 'sc cambuur', 'cambuur leeuwarden', 'de club uit leeuwarden', 'de leeuwarders', 'de friezen']}

clubadjectivedict = {'PEC Zwolle': ['zwols'], 'N.E.C.': ['nijmeegs'], 'ADO Den Haag': ['haags'], 'Go Ahead Eagles': ['deventer'], 'FC Twente': ['twents'],
     'Excelsior': ['kralings', 'rotterdams'], 'FC Utrecht': ['utrechts'], 'PSV': ['eindhovens'], 'Willem II': ['tilburgs'], 'Vitesse': ['arnhems'], 'AZ': ['alkmaars'],
     'sc Heerenveen': ['heerenveens', 'fries'], 'FC Groningen': ['gronings'], 'Feyenoord': ['rotterdams'], 'Roda JC Kerkrade': ['limburgs'],
     'Heracles Almelo': ['almelose', 'almeloos'], 'Sparta Rotterdam': ['rotterdams', 'spartaans'], 'Ajax': ['amsterdams'], 'De Graafschap': ['doetinchems', 'achterhoeks'],
     'SC Cambuur Leeuwarden': ['fries', 'leeuwardens']}

teamoflist = ['de ploeg van trainer rené hake', 'de ploeg van giovanni van bronckhorst', 'de ploeg van hans de koning',
              'de ploeg van trainer erik ten hag', 'de ploeg van trainer yannis anastasiou', 'de ploeg van phillip cocu',
              'de ploeg van coach alfons groenendijk', 'de ploeg van ten hag', 'de ploeg van ernest faber', 'de ploeg van john van den brom',
              'de ploeg van trainer ron jans', 'de ploeg van trainer phillip cocu', 'de ploeg van giovanni van bronckhorst', 'de ploeg van trainer john van den brom',
              'de ploeg van hake', 'de ploeg van cocu', 'het team van mitchell van der gaag']


currentpath = os.getcwd()

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

def add_text_gaps(file):
    with open(currentpath + '/Corpora/' + file + '.data', 'rb') as f:
        data = f.readlines()
    data = [x.decode('utf-8') for x in data]

    with open(currentpath + '/Corpora/' + file + '.text', 'rb') as f:
        text = f.readlines()
    text = [x.decode('utf-8') for x in text]

    combinedlist = convert_data(data)

    for lineidx, line in enumerate(combinedlist):
        for tagidx, tag in enumerate(line):
            if 'Surname' in tag[0]:
                if len(tag[1].split()) > 1: #Check if there is more than one word in the surname section (and if so, if this is due to interjections in the surname
                    if (tag[1].split()[0].lower() == 'van') or (tag[1].split()[0].lower() == 'de') or (tag[1].split()[0].lower() == 'el') or (tag[1].split()[0].lower() == 'te') or (tag[1].split()[0].lower() == 'ter') or (tag[1].split()[0].lower() == 'st.') or (tag[1].split()[0].lower() == 'bel'):
                        ''
                    else:
                        combinedlist[lineidx][tagidx][1] = combinedlist[lineidx][tagidx][1].split()
                        combinedlist[lineidx][tagidx][1] = ' '.join(combinedlist[lineidx][tagidx][1][1:]).strip() #Remove the fist name from the surname in cases where they mistakenly used the full name for the surname
            if tag[0] == 'GoalScorer_Name':
                text[lineidx] = re.sub(r'\b' + re.escape(tag[1].lower()) + r'\b', '<goal_scorer>', text[lineidx])
            elif tag[0] == 'GoalScorer_Surname':
                text[lineidx] = re.sub(r'\b' + re.escape(tag[1].lower()) + r'\b', '<goal_scorer>', text[lineidx])
            elif tag[0] == 'GoalScorer_Position':
                if tag[1] == 'Forward':
                    text[lineidx] = re.sub(r'\b((vleugel)|(rechter))?aanvaller\b', '<goal_scorer_position>', text[lineidx])
                if tag[1] == 'Midfielder':
                    text[lineidx] = re.sub(r'\bmiddenvelder\b', '<goal_scorer_position>', text[lineidx])
                if tag[1] == 'Defender':
                    text[lineidx] = re.sub(r'(\b((links)|(rechts))?back\b)|(\b((centrum)|(vleugel))?verdediger\b)', '<goal_scorer_position>', text[lineidx])
                if tag[1] == 'Goalkeeper':
                    text[lineidx] = re.sub(r'(\bdoelman\b)|(\bkeeper\b)|(\bgoalie\b)', '<goal_scorer_position>', text[lineidx])
            elif tag[0] == 'AssistGiver_Name':
                text[lineidx] = re.sub(r'\b' + re.escape(tag[1].lower()) + r'\b', '<assist_giver>', text[lineidx])
            elif tag[0] == 'AssistGiver_Surname':
                text[lineidx] = re.sub(r'\b' + re.escape(tag[1].lower()) + r'\b', '<assist_giver>', text[lineidx])
            elif tag[0] == 'AssistGiver_Position':
                if tag[1] == 'Forward':
                    text[lineidx] = re.sub(r'\b((vleugel)|(rechter))?aanvaller\b', '<assist_giver_position>', text[lineidx])
                if tag[1] == 'Midfielder':
                    text[lineidx] = re.sub(r'\bmiddenvelder\b', '<assist_giver_position>', text[lineidx])
                if tag[1] == 'Defender':
                    text[lineidx] = re.sub(r'(\b((links)|(rechts))?back\b)|(\b((centrum)|(vleugel))?verdediger\b)', '<assist_giver_position>', text[lineidx])
                if tag[1] == 'Goalkeeper':
                    text[lineidx] = re.sub(r'(\bdoelman\b)|(\bkeeper\b)|(\bgoalie\b)', '<assist_giver_position>', text[lineidx])
            elif tag[0] == 'Minute':
                minuteoptions = [str(int(tag[1])-2), str(int(tag[1])-1), tag[1], str(int(tag[1])+1), str(int(tag[1])+2)]
                for option in minuteoptions:
                    text[lineidx] = re.sub(r'\s' + re.escape(option) + r'([^\-])', r' <time>\g<1>', text[lineidx])
                text[lineidx] = re.sub(r'(\een half\s?uur\b)|(\been kwartier\b)|(\been uur\b)|(\bblessuretijd\b)|(\bhet slotkwartier\b)|(\bvlak voor tijd\b)|(\bde slotfase\b)', '<time>',
                                       text[lineidx])
                text[lineidx] = re.sub(r'(\brust\b)|(\bde thee(pauze)?\b)|(\bde pauze\b)|(\bde eerste helft\b)|(\bde tweede helft\b)', '<halftime>', text[lineidx])
                text[lineidx] = re.sub(r'(\b((eerste )|(tweede )|(derde )|(vierde )|(vijfde )|(zesde )|(zevende )|(achtste )|(negende )|(tiende )|(elfde )|(twaalfde )|(dertiende )|(veertiende )|(vijftiende )|(zestiende )|(zeventiende )|(achtiende )|(negentiende )|(twintigste )|(vijftigste ))(minuut\b))', '<time> minuut', text[lineidx])
                text[lineidx] = re.sub(r'\bna (.*?) minuten\b', 'na <time> minuten', text[lineidx])
                text[lineidx] = re.sub(r'\bbinnen (.*?) minuten\b', 'binnen <time> minuten', text[lineidx])
                text[lineidx] = re.sub(r'\been aantal minuten later\b', '<time> minuten later', text[lineidx])
                text[lineidx] = re.sub(r'(\w+) minuten later', '<time> minuten later', text[lineidx])
                text[lineidx] = re.sub(r'(\w+) minuten voor het einde', '<time> minuten voor het einde', text[lineidx])
                text[lineidx] = re.sub(r'de (\w+) minuut', 'de <time> minuut', text[lineidx])
            elif tag[0] == 'Score':
                text[lineidx] = re.sub(r'\b' + re.escape(tag[1].lower()) + r'\b', '<score>', text[lineidx])
                newscore = re.sub(r'(\d+)\-(\d+)', r'\g<2>-\g<1>', tag[1])
                text[lineidx] = re.sub(r'\b' + re.escape(newscore.lower()) + r'\b', '<score>', text[lineidx])
            elif tag[0] == 'Team':
                try:
                    teamname = re.search(r'^(.*?) \;', tag[1]).group(1)
                    homeaway = re.search(r'\; (.*?)$', tag[1]).group(1)
                except AttributeError:
                    teamname = tag[1]
                    homeaway = None
                for team in clubdict:
                    if team == teamname:
                        possibilities = clubdict[team] + [teamname.lower()] + teamoflist
                        if homeaway == 'home':
                            possibilities = possibilities + ['de thuisploeg']
                        elif homeaway == 'away':
                            possibilities = possibilities + ['de uitploeg', 'de bezoekers']

                        possibilities.sort(key=lambda s: len(s))
                        possibilities = possibilities[::-1]
                        break
                for adjectiveteam in clubadjectivedict:
                    if adjectiveteam == teamname:
                        adjectivepossibilities = clubadjectivedict[adjectiveteam]
                        break
                for clubname in possibilities:
                    text[lineidx] = re.sub(re.escape(clubname.lower()), '<team>', text[lineidx])
                for adjectiveclubname in adjectivepossibilities:
                    text[lineidx] = re.sub(re.escape(adjectiveclubname.lower()) + r'e?', '<team>', text[lineidx])
            elif tag[0] == 'OtherTeam':
                try:
                    teamname = re.search(r'^(.*?) \;', tag[1]).group(1)
                    homeaway = re.search(r'\; (.*?)$', tag[1]).group(1)
                except AttributeError:
                    teamname = tag[1]
                    homeaway = None

                for team in clubdict:
                    if team == teamname:
                        possibilities = clubdict[team] + [teamname.lower()]
                        if homeaway == 'home':
                            possibilities = possibilities + ['de thuisploeg']
                        elif homeaway == 'away':
                            possibilities = possibilities + ['de uitploeg', 'de bezoekers']
                        possibilities.sort(key=lambda s: len(s))
                        possibilities = possibilities[::-1]
                        break
                for adjectiveteam in clubadjectivedict:
                    if adjectiveteam == teamname:
                        adjectivepossibilities = clubadjectivedict[adjectiveteam]
                        break
                for clubname in possibilities:
                    text[lineidx] = re.sub(re.escape(clubname.lower()), '<other_team>', text[lineidx])
                for adjectiveclubname in adjectivepossibilities:
                    text[lineidx] = re.sub(re.escape(adjectiveclubname.lower()) + r'e?', '<other_team>', text[lineidx])
            elif (tag[0] == 'GoalKeeperTeamName') and (tag[1] != ''):
                text[lineidx] = re.sub(r'((\bdoelman )|(\bkeeper )|(\bgoalie ))?' +  re.escape(tag[1].lower()) + r'\b', '<goalkeeper>', text[lineidx])
            elif (tag[0] == 'GoalKeeperTeamSurname') and (tag[1] != ''):
                text[lineidx] = re.sub(r'((\bdoelman )|(\bkeeper )|(\bgoalie ))?' + re.escape(tag[1].lower()) + r'\b', '<goalkeeper>', text[lineidx])
            elif (tag[0] == 'GoalKeeperOtherTeamName') and (tag[1] != ''):
                text[lineidx] = re.sub(r'((\bdoelman )|(\bkeeper )|(\bgoalie ))?' + re.escape(tag[1].lower()) + r'\b', '<goalkeeper_other_team>', text[lineidx])
            elif (tag[0] == 'GoalKeeperOtherTeamSurname') and (tag[1] != ''):
                text[lineidx] = re.sub(r'((\bdoelman )|(\bkeeper )|(\bgoalie ))?' + re.escape(tag[1].lower()) + r'\b', '<goalkeeper_other_team>', text[lineidx])
            elif (tag[0] == 'FoulCommitted_Player_Name') and (tag[1] != ''):
                text[lineidx] = re.sub(r'((\bdoelman )|(\bkeeper )|(\bgoalie ))?' + re.escape(tag[1].lower()) + r'\b', '<foul_committed>', text[lineidx])
            elif (tag[0] == 'FoulCommitted_Player_Surname') and (tag[1] != ''):
                text[lineidx] = re.sub(r'((\bdoelman )|(\bkeeper )|(\bgoalie ))?' + re.escape(tag[1].lower()) + r'\b', '<foul_committed>', text[lineidx])
            elif tag[0] == 'FoulCommitted_Player_Position':
                if tag[1] == 'Forward':
                    text[lineidx] = re.sub(r'\b((vleugel)|(rechter))?aanvaller\b', '<foul_committed_position>', text[lineidx])
                if tag[1] == 'Midfielder':
                    text[lineidx] = re.sub(r'\bmiddenvelder\b', '<foul_committed_position>', text[lineidx])
                if tag[1] == 'Defender':
                    text[lineidx] = re.sub(r'(\b((links)|(rechts))?back\b)|(\b((centrum)|(vleugel))?verdediger\b)', '<foul_committed_position>', text[lineidx])
                if tag[1] == 'Goalkeeper':
                    text[lineidx] = re.sub(r'(\bdoelman\b)|(\bkeeper\b)|(\bgoalie\b)', '<foul_committed_position>', text[lineidx])
            elif (tag[0] == 'FoulSuffered_Player_Name') and (tag[1] != ''):
                text[lineidx] = re.sub(r'\b' + re.escape(tag[1].lower()) + r'\b', '<foul_suffered>', text[lineidx])
            elif (tag[0] == 'FoulSuffered_Player_Surname') and (tag[1] != ''):
                text[lineidx] = re.sub(r'\b' + re.escape(tag[1].lower()) + r'\b', '<foul_suffered>', text[lineidx])
            elif (tag[0] == 'FoulSuffered_Player_Position') and (tag[1] != ''):
                if tag[1] == 'Forward':
                    text[lineidx] = re.sub(r'\b((vleugel)|(rechter))?aanvaller\b', '<foul_suffered_position>', text[lineidx])
                if tag[1] == 'Midfielder':
                    text[lineidx] = re.sub(r'\bmiddenvelder\b', '<foul_suffered_position>', text[lineidx])
                if tag[1] == 'Defender':
                    text[lineidx] = re.sub(r'(\b((links)|(rechts))?back\b)|(\b((centrum)|(vleugel))?verdediger\b)', '<foul_suffered_position>', text[lineidx])
                if tag[1] == 'Goalkeeper':
                    text[lineidx] = re.sub(r'(\bdoelman\b)|(\bkeeper\b)|(\bgoalie\b)', '<foul_suffered_position>', text[lineidx])
            elif (tag[0] == 'CardPlayer_Name') and (tag[1] != ''):
                text[lineidx] = re.sub(r'\b' + re.escape(tag[1].lower()) + r'\b', '<card_player>', text[lineidx])
            elif (tag[0] == 'CardPlayer_Surname') and (tag[1] != ''):
                text[lineidx] = re.sub(r'\b' + re.escape(tag[1].lower()) + r'\b', '<card_player>', text[lineidx])
            elif (tag[0] == 'CardPlayer_Position') and (tag[1] != ''):
                if tag[1] == 'Forward':
                    text[lineidx] = re.sub(r'\b((vleugel)|(rechter))?aanvaller\b', '<card_player_position>', text[lineidx])
                if tag[1] == 'Midfielder':
                    text[lineidx] = re.sub(r'\bmiddenvelder\b', '<card_player_position>', text[lineidx])
                if tag[1] == 'Defender':
                    text[lineidx] = re.sub(r'(\b((links)|(rechts))?back\b)|(\b((centrum)|(vleugel))?verdediger\b)', '<card_player_position>', text[lineidx])
                if tag[1] == 'Goalkeeper':
                    text[lineidx] = re.sub(r'(\bdoelman\b)|(\bkeeper\b)|(\bgoalie\b)', '<card_player_position>', text[lineidx])
    return text

def add_data_gaps(file):
    with open(currentpath + '/Corpora/' + file + '.data', 'rb') as f:
        data = f.readlines()
    data = [x.decode('utf-8') for x in data]

    with open(currentpath + '/Corpora/' + file + '.text', 'rb') as f:
        text = f.readlines()
    text = [x.decode('utf-8') for x in text]

    combinedlist = convert_data(data)

    for lineidx, line in enumerate(combinedlist):
        for tagidx, tag in enumerate(line):
            if tag[0] == 'GoalScorer_Name':
                combinedlist[lineidx][tagidx][1] = '<goal_scorer>'
            elif tag[0] == 'GoalScorer_Surname':
                combinedlist[lineidx][tagidx][1] = '<goal_scorer>'
            elif tag[0] == 'GoalScorer_Position':
                combinedlist[lineidx][tagidx][1] = '<goal_scorer_position>'
            elif tag[0] == 'AssistGiver_Name':
                combinedlist[lineidx][tagidx][1] = '<assist_giver>'
            elif tag[0] == 'AssistGiver_Surname':
                combinedlist[lineidx][tagidx][1] = '<assist_giver>'
            elif tag[0] == 'AssistGiver_Position':
                combinedlist[lineidx][tagidx][1] = '<assist_giver_position>'
            elif tag[0] == 'Minute':
                combinedlist[lineidx][tagidx][1] = '<time>'
            elif tag[0] == 'TimeSinceGoal':
                combinedlist[lineidx][tagidx][1] = '<time>'
            elif tag[0] == 'Score':
                combinedlist[lineidx][tagidx][1] = '<score>'
            elif tag[0] == 'Team':
                combinedlist[lineidx][tagidx][1] = '<team>'
            elif tag[0] == 'OtherTeam':
                combinedlist[lineidx][tagidx][1] = '<other_team>'
            elif tag[0] == 'GoalKeeperTeamName':
                combinedlist[lineidx][tagidx][1] = '<goalkeeper>'
            elif tag[0] == 'GoalKeeperTeamSurname':
                combinedlist[lineidx][tagidx][1] = '<goalkeeper>'
            elif tag[0] == 'GoalKeeperOtherTeamName':
                combinedlist[lineidx][tagidx][1] = '<goalkeeper_other_team>'
            elif tag[0] == 'GoalKeeperOtherTeamSurname':
                combinedlist[lineidx][tagidx][1] = '<goalkeeper_other_team>'
            elif tag[0] == 'FoulCommitted_Player_Name':
                combinedlist[lineidx][tagidx][1] = '<foul_committed>'
            elif tag[0] == 'FoulCommitted_Player_Surname':
                combinedlist[lineidx][tagidx][1] = '<foul_committed>'
            elif tag[0] == 'FoulCommitted_Player_Position':
                combinedlist[lineidx][tagidx][1] = '<foul_committed_position>'
            elif tag[0] == 'FoulSuffered_Player_Name':
                combinedlist[lineidx][tagidx][1] = '<foul_suffered>'
            elif tag[0] == 'FoulSuffered_Player_Surname':
                combinedlist[lineidx][tagidx][1] = '<foul_suffered>'
            elif tag[0] == 'FoulSuffered_Player_Position':
                combinedlist[lineidx][tagidx][1] = '<foul_suffered_position>'
            elif tag[0] == 'CardPlayer_Name':
                combinedlist[lineidx][tagidx][1] = '<card_player>'
            elif tag[0] == 'CardPlayer_Surname':
                combinedlist[lineidx][tagidx][1] = '<card_player>'
            elif tag[0] == 'CardPlayer_Position':
                combinedlist[lineidx][tagidx][1] = '<card_player_position>'
            combinedlist[lineidx][tagidx] = ': '.join(tag)
        combinedlist[lineidx] = ' '.join(line)

    return combinedlist

for file in ['Goals', 'Cards']:
    text = add_text_gaps(file)
    text = ''.join(text)
    data = add_data_gaps(file)
    data = '\n'.join(data)
    with open(currentpath + '/Corpora/' + file + '_gaps.text', 'wb') as f:
        f.write(bytes(text, 'UTF-8'))
    with open(currentpath + '/Corpora/' + file + '_gaps.data', 'wb') as f:
        f.write(bytes(data, 'UTF-8'))