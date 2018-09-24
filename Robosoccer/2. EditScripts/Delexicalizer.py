import os
import regex as re
import sys

currentpath = os.getcwd()

def delexicalizer(file):
    with open(currentpath + '/Corpora/sportscasting/' + file + '.text', 'rb') as f:
        text = f.readlines()

    with open(currentpath + '/Corpora/sportscasting/' + file + '.data', 'rb') as f:
        data = f.readlines()

    text = [t.decode('utf-8') for t in text]
    oldtext = text[:]
    data = [d.decode('utf-8') for d in data]
    idx = 0
    while idx < len(text):
        text[idx] = re.sub(r'\n', '', text[idx])
        #If there is a pink and a purple player in the line
        if (re.search(r'(pink\d+)|(pink goalie)|(pink team)', text[idx])) and (re.search(r'(purple\d+)|(purple goalie)|(purple team)', text[idx])):
            teams = re.findall(r"((pink\d+)|(purple\d+)|(pink goalie)|(purple goalie))", text[idx])
            teams = [x[0] for x in teams]
            if len(teams) == 2:
                # First pink or purple player becomes <player_1_team_1>
                text[idx] = re.sub(r"((pink\d+)|(purple\d+)|(pink goalie)|(purple goalie))", '<player_1_team_1>', text[idx], count=1)
                # Second pink or purple player becomes <player_1_team_2>
                text[idx] = re.sub(r"((pink\d+)|(purple\d+)|(pink goalie)|(purple goalie))", '<player_1_team_2>', text[idx], count=1)
            if len(teams) == 3:
                if 'pink' in teams[0]:
                    team1 = 'pink'
                else:
                    team1 = 'purple'
                if 'pink' in teams[1]:
                    team2 = 'pink'
                else:
                    team2 = 'purple'
                if 'pink' in teams[2]:
                    team3 = 'pink'
                else:
                    team3 = 'purple'
                # First pink or purple player becomes <player_1_team_1>
                text[idx] = re.sub(r"((pink\d+)|(purple\d+)|(pink goalie)|(purple goalie))", '<player_1_team_1>', text[idx], count=1)

                # If the team of the second player is different from the first, make it <player_1_team_2>
                if team2 != team1:
                    text[idx] = re.sub(r"((pink\d+)|(purple\d+)|(pink goalie)|(purple goalie))", '<player_1_team_2>', text[idx], count=1)
                # Else the teams are the same and it should be <player_2_team_1>
                else:
                    text[idx] = re.sub(r"((pink\d+)|(purple\d+)|(pink goalie)|(purple goalie))", '<player_2_team_1>', text[idx], count=1)

                if (team3 == team1) and (team3 != team2):
                    text[idx] = re.sub(r"((pink\d+)|(purple\d+)|(pink goalie)|(purple goalie))", '<player_2_team_1>', text[idx], count=1)
                if (team3 != team1) and (team3 == team2):
                    text[idx] = re.sub(r"((pink\d+)|(purple\d+)|(pink goalie)|(purple goalie))", '<player_2_team_2>', text[idx], count=1)
                if (team3 != team1) and (team3 != team2):
                    text[idx] = re.sub(r"((pink\d+)|(purple\d+)|(pink goalie)|(purple goalie))", '<player_1_team_2>', text[idx], count=1)

            #Same for teams
            text[idx] = re.sub(r"((pink team)|(purple team))", '<team_1>', text[idx], count=1)
            text[idx] = re.sub(r"((pink team)|(purple team))", '<team_2>', text[idx], count=1)
        #Else they talk about one or two players from the same team
        else:
            #First pink or purple player/team becomes <player_1>
            text[idx] = re.sub(r"((pink\d+)|(purple\d+)|(pink goalie)|(purple goalie)|(the goalie))", '<player_1>', text[idx], count=1)
            text[idx] = re.sub(r"((pink team)|(purple team))", '<team_1>', text[idx], count=1)
            #Second player/team in the line becomes <player_2>
            text[idx] = re.sub(r"((pink\d+)|(purple\d+)|(pink goalie)|(purple goalie)|(the goalie))", '<player_2>', text[idx], count=1)
            text[idx] = re.sub(r"((pink team)|(purple team))", '<team_2>', text[idx], count=1)
        if not re.search(r'\w', data[idx]):
            del data[idx]
            del text[idx]
            del oldtext[idx]
        elif not re.search(r'<', text[idx]):
            del data[idx]
            del text[idx]
            del oldtext[idx]
        else:
            idx += 1
    return data, text, oldtext

def datamatching(text, olddata, oldtext):
    data = [''] * len(text)
    idx = 0
    while idx < len(text):
        if (re.search(r'<player_1>', text[idx])) and (re.search(r'pass', text[idx])) and (re.search(r'<player_2>', text[idx])):
            data[idx] = 'pass.arg1: <player_1> pass.arg2: <player_2>'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'picked ((\boff\b)|(\bup\b)) by', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'takes possession', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg2: <player_1> badPass'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'turns(.*?)over', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'kicks(.*?)to', text[idx])) and (re.search(r'<player_2>', text[idx])):
            data[idx] = 'pass.arg1: <player_1> pass.arg2: <player_2>'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'bad(.*?)pass', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> badPass'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'steals(.*?)from', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_2> turnover.arg2: <player_1_team_1> steal'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'defended(.*?)by', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> defense'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'blocked(.*?)by', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> block'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'shoots', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'kick.arg1: <player_1>'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'intercepted(.*?)by', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> badPass'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'turns(.*?)back to', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'pick((s)|(ed)) ((off)|(up))', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg2: <player_1> badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'los((es)|(t)) control', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1> badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'block', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg2: <player_1> block'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'bad(.*?)pass', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1> badPass'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'loses(.*?)to', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> badPass'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'turned(.*?)over', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> badPass'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'kicks(.*?)to', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'intercepts', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg2: <player_1>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'steals', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg2: <player_1>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'kick(.*?)out of bound(s)?', text[idx])) and not (re.search(r'<player_2>', text[idx])) and not (re.search(r'almost', text[idx])):
            data[idx] = 'turnover.arg1: <player_1> playmode.arg1: kick_in badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'has the ball', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'pass.arg2: <player_1>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'takes(.*?)back', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg2: <player_1>'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'turned(.*?)back to', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'inbound', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg2: <player_1> playmode.arg1: kick_in badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'dribbl((es)|(ing))', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'kick.arg1: <player_1>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'has the ball', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'pass.arg2: <player_1>'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'lost(.*?)to', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'will kick in', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg2: <player_1> playmode.arg1: kick_in badPass'
        elif (re.search(r'<team_1>', text[idx])) and (re.search(r'will kick in', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg2: <team_1> playmode.arg1: kick_in badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'defens', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg2: <player_1> defense'
        elif (re.search(r'<team_1>', text[idx])) and (re.search(r'score((d)|(s))', text[idx])) and not (re.search(r'<team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <team_1> playmode.arg1: goal'
        elif (re.search(r'<team_1>', text[idx])) and (re.search(r'offside', text[idx])) and not (re.search(r'<team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <team_1> playmode.arg1: offside'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'coming down', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'kick.arg1: <player_1>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'kick(s)? off', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'pass.arg1: <player_1> playmode.arg1: kick_off'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'(re)?gains possession', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg2: <player_1> badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'gets to the ball', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'kick.arg1: <player_1>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'gets close(r)? to', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'kick.arg1: <player_1>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'chance to score', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'kick.arg1: <player_1>'
        elif (re.search(r'<team_1>', text[idx])) and (re.search(r'corner kick', text[idx])) and not (re.search(r'<team_2>', text[idx])):
            data[idx] = 'turnover.arg2: <team_1> playmode.arg1: corner_kick'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'is going toward the goal', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'kick.arg1: <player_1>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'picked(.*?)up', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'pass.arg2: <player_1>'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'fighting ((for)|(over)) the ball', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_2> turnover.arg2: <player_1_team_1> badPass'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'loses the ball', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1> badPass'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'stolen', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_2> turnover.arg2: <player_1_team_1> steal'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'hold((s)|(ing)) (.*?) the ball', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'kick.arg1: <player_1>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'moving the ball', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'kick.arg1: <player_1>'
        elif (re.search(r'<team_1>', text[idx])) and (re.search(r'inbound', text[idx])) and not (re.search(r'<team_2>', text[idx])):
            data[idx] = 'turnover.arg2: <team_1> playmode.arg1: kick_in badPass'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'defended', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_2> turnover.arg2: <player_1_team_1> defense'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'stolen', text[idx])) and not (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> steal'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'tries to pass', text[idx])) and (re.search(r'<player_2_team_1>', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'badPass.arg1: <player_1_team_1> badPass.arg2: <player_2_team_1> turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'scored', text[idx])) and (re.search(r'<team_1>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1> playmode.arg1: goal turnover.arg1: <team_1>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'scored', text[idx])):
            data[idx] = 'turnover.arg1: <player_1> playmode.arg1: goal'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'gets inside', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'kick.arg1: <player_1>'
        elif (re.search(r'free(\s)?kick', text[idx])) and (re.search(r'<team_1>', text[idx])):
            data[idx] = 'playmode.arg1: free_kick turnover.arg2: <team_1>'
        elif (re.search(r'<team_1>', text[idx])) and (re.search(r'kick(s)? off', text[idx])) and not (re.search(r'<team_2>', text[idx])):
            data[idx] = 'pass.arg1: <team_1> playmode.arg1: kick_off'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'pass', text[idx])) and (re.search(r'<player_2_team_1>', text[idx])):
            data[idx] = 'pass.arg1: <player_1_team_1> pass.arg2: <player_2_team_1>'
        elif (re.search(r'a goal', text[idx])) and (re.search(r'<team_1>', text[idx])):
            data[idx] = 'turnover.arg1: <team_1> playmode.arg1: goal'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'is nearing', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'kick.arg1: <player_1>'
        elif (re.search(r'<team_1>', text[idx])) and (re.search(r'will take', text[idx])) and not (re.search(r'<team_1>', text[idx])):
            data[idx] = 'pass.arg1: <team_1> playmode.arg1: kick_off'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'takes the ball(.*?)from', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_2> turnover.arg2: <player_1_team_1> steal'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'returns', text[idx])) and (re.search(r'<player_2>', text[idx])):
            data[idx] = 'pass.arg1: <player_1> pass.arg2: <player_2>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'lost', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1> badPass'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'lost', text[idx])) and not (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_2> turnover.arg2: <player_1_team_1> badPass'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'stole(.*?)from', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_2> turnover.arg2: <player_1_team_1> steal'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'turning over(.*?)to', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_1> turnover.arg2: <player_1_team_2> badPass'
        elif (re.search(r'<player_1_team_1>', text[idx])) and (re.search(r'strips(.*?)from', text[idx])) and (re.search(r'<player_1_team_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1_team_2> turnover.arg2: <player_1_team_1> steal'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'scores', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1> playmode.arg1: goal'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'kicks', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'kick.arg1: <player_1>'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'controls', text[idx])) and not (re.search(r'<player_2>', text[idx])):
            data[idx] = 'turnover.arg1: <player_1> defense'
        elif (re.search(r'<player_1>', text[idx])) and (re.search(r'shoots to', text[idx])) and (re.search(r'<player_2>', text[idx])):
            data[idx] = 'pass.arg1: <player_1> pass.arg2: <player_2>'


        if data[idx] == '':
            del text[idx]
            del data[idx]
            del olddata[idx]
            del oldtext[idx]
        else:
            idx += 1


    return data, olddata, text, oldtext

filelist = ['All', 'Train', 'Test', 'Dev']
currentpath = os.getcwd()
for file in filelist:
    data, text, oldtext = delexicalizer(file)
    newdata, olddata, newtext, oldtext = datamatching(text, data, oldtext)
    oldtext = ''.join(oldtext)
    newtext = '\n'.join(newtext) + '\n'
    olddata = ''.join(olddata)
    newdata = '\n'.join(newdata) + '\n'
    with open(currentpath + '/Corpora/sportscasting/' + file + '_2.text', 'wb') as f:
        print('Writing new file')
        f.write(bytes(oldtext, 'UTF-8'))
    with open(currentpath + '/Corpora/sportscasting/' + file + '_2_new.text', 'wb') as f:
        print('Writing new file')
        f.write(bytes(newtext, 'UTF-8'))
    with open(currentpath + '/Corpora/sportscasting/' + file + '_2.data', 'wb') as f:
        print('Writing new file')
        f.write(bytes(olddata, 'UTF-8'))
    with open(currentpath + '/Corpora/sportscasting/' + file + '_2_new.data', 'wb') as f:
        print('Writing new file')
        f.write(bytes(newdata, 'UTF-8'))

