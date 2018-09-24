import regex as re
import os

currentpath = os.getcwd()
with open(currentpath + '/Corpora/All2.data') as f:
    data = f.readlines()
#data = [x.decode('utf-8') for x in data]
data = [re.sub(r'\n', '', x) for x in data]

with open(currentpath + '/Corpora/All.text') as f:
    text = f.readlines()
#text = [x.decode('utf-8') for x in text]
text = [re.sub(r'\n', '', x) for x in text]

#Convert each data line into a dictionary {'DataType': 'data'}
data = [re.sub(r': ', ':', x) for x in data]
data = [x.split(' ') for x in data]
times = ['0600', '1200', '0000', '2100', '0900', '1800', '-1', '1500', '0300']
replacedict = {}
datadictlist = []
newdata = []
for idx, val in enumerate(data):
    datadict = {}
    data[idx] = [x.split(':') for x in data[idx]]
    newdata.append(data[idx])
    for infoidx, infoval in enumerate(data[idx]):
        if 'WindDir.' in data[idx][infoidx][0]:
            data[idx][infoidx][1] = data[idx][infoidx][1].lower()
    data[idx] = [dict([x]) for x in data[idx]]
    for d in data[idx]:
        datadict.update(d)
    datadictlist.append(datadict)

    #Obtain the numbers used in the data (e.g. the 2 in GustSpeedMin.2)
    numlist = []
    for d in datadict:
        dnum = re.search('\.(\d+)$', d).group(1)
        if dnum not in numlist:
            numlist.append(dnum)
    numlist.sort()
    for num in numlist:
        if 'WindDir.' + num in datadict:
            text[idx] = re.sub(r'(^|\s)' + re.escape(datadict['WindDir.' + num]) + r"((\s)|($)|('ly(\s|$)))", ' <wind_direction> ', text[idx], count=1)
        if ('WindSpeedMin.' + num in datadict) and ('WindSpeedMax.' + num in datadict):
            minmax = datadict['WindSpeedMin.' + num] + '-' + datadict['WindSpeedMax.' + num]
            text[idx] = re.sub(r'\b' + re.escape(minmax) + r'\b', '<wind_speed>', text[idx], count=1)
        elif ('WindSpeedMin.' + num in datadict) or ('WindSpeedMax.' + num in datadict):
            if 'WindSpeedMin.' + num in datadict:
                windspeed = datadict['WindSpeedMin.' + num]
            elif 'WindSpeedMax.' + num in datadict:
                windspeed = datadict['WindSpeedMax.' + num]
            text[idx] = re.sub(r'(^|\s)' + re.escape(windspeed) + r'(\s|$)', ' <wind_speed> ', text[idx], count=1)
        if ('GustSpeedMin.' + num in datadict) and ('GustSpeedMax.' + num in datadict):
            minmax = datadict['GustSpeedMin.' + num] + '-' + datadict['GustSpeedMax.' + num]
            text[idx] = re.sub(r'\b' + re.escape(minmax) + r'\b', '<gust_speed>', text[idx], count=1)
        elif ('GustSpeedMin.' + num in datadict) or ('GustSpeedMax.' + num in datadict):
            if 'GustSpeedMin.' + num in datadict:
                gustspeed = datadict['GustSpeedMin.' + num]
            elif 'GustSpeedMax.' + num in datadict:
                gustspeed = datadict['GustSpeedMax.' + num]
            text[idx] = re.sub(r'(^|\s)' + re.escape(gustspeed) + r'(\s|$)', ' <gust_speed> ', text[idx], count=1)
    #Veering is clockwise
    text[idx] = re.sub(r'\bveering\b', '<wind_direction_change>', text[idx])
    #Backing is counter clockwinse
    text[idx] = re.sub(r'\bbacking\b', '<wind_direction_change>', text[idx])
    #Easing, decreasing, falling (down), increasing, rising, freshening (up)
    text[idx] = re.sub(r'\beasing\b', '<wind_speed_change>', text[idx])
    text[idx] = re.sub(r'\bdecreasing\b', '<wind_speed_change>', text[idx])
    text[idx] = re.sub(r'\brising\b', '<wind_speed_change>', text[idx])
    text[idx] = re.sub(r'\bincreasing\b', '<wind_speed_change>', text[idx])
    text[idx] = re.sub(r'\bfalling\b', '<wind_speed_change>', text[idx])
    text[idx] = re.sub(r'\bfreshening\b', '<wind_speed_change>', text[idx])

    #by late evening = 0000
    #by midday = 1200
    #by mid evening = 2100
    #this morning = 0900/0600 (eerste tijd)
    #by evening = 1800/2100
    #by midnight = 2100/0000 (laatste tijd)
    #by late afternoon = 1800
    #by mid afternoon = 1500
    #mid period = 1500
    #by end of period = laatste tijd
    #by early evening = 1800
    #this evening = 2100
    #by early afternoon = 1200
    #by afternoon = 1200/1500
    #by late morning = 0600
    #by 1200 = 1200
    #by 1800 = 1800
    #by end of day = 0000
    #during the morning = 1200
    #mid morning = 0600
    #morning = 0600
    #during the afternoon = 1500
    #this afternoon = 1500
    #through the afternoon = 1500
    #in the afternoon = 1800
    #in the evening = 2100
    #through the evening = 0000
    #midnight = 0000
    #overnight = 0600/2100 (laatste)
    #tonight = 0000
    text[idx] = re.sub(r'\b(by )?late evening\b', '<time>', text[idx])
    text[idx] = re.sub(r'\b((by )|(around ))?midday\b', '<time>', text[idx])
    text[idx] = re.sub(r'\b(by )?mid evening\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bthis morning\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bby evening\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bby midnight\b', '<time>', text[idx])
    text[idx] = re.sub(r'\b(by )?late afternoon\b', '<time>', text[idx])
    text[idx] = re.sub(r'\b((by )|(around ))?mid afternoon\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bmid period\b', '<time>', text[idx])
    text[idx] = re.sub(r'\b((by )|(around ))?end of period\b', '<time>', text[idx])
    text[idx] = re.sub(r'\b(by )?early evening\b', '<time>', text[idx])
    text[idx] = re.sub(r'\b(by )?this evening\b', '<time>', text[idx])
    text[idx] = re.sub(r'\b(by )?early afternoon\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bby afternoon\b', '<time>', text[idx])
    text[idx] = re.sub(r'\b(by )?late morning\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bby 1200\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bby 1800\b', '<time>', text[idx])
    text[idx] = re.sub(r'\b(by )?end of day\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bduring the morning\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bmid morning\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bmorning\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bduring the afternoon\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bthis afternoon\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bthrough the afternoon\b', '<time>', text[idx])
    text[idx] = re.sub(r'\b(late )?in the afternoon\b', '<time>', text[idx])
    text[idx] = re.sub(r'\b((in )|(during )|(through ))the evening\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bevening\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bmidnight\b', '<time>', text[idx])
    text[idx] = re.sub(r'\bovernight\b', '<time>', text[idx])
    text[idx] = re.sub(r'\btonight\b', '<time>', text[idx])
    text[idx] = re.sub(r'\blate in day\b', '<time>', text[idx])
    text[idx] = re.sub(r'\blater$', '<time>', text[idx])


    #Get the rest of the wind directions that weren't found using the data
    directions = ['N', 'M-N', 'N-NNE', 'NNE-N', 'N-NE', 'NNE', 'NNE-NE', 'NE-N', 'NE-NNE', 'M-NE', 'NE', 'NE-ENE', 'ENE-NE', 'NE-E', 'ENE', 'E-NE',
                  'E-ENE',
                  'E', 'E-ESE', 'ESE-E', 'E-SE', 'ESE', 'ESE-SE', 'SE-E', 'SE-ESE', 'M-SE', 'ORVAR-SE', 'MVAR-SE', 'SE', 'SE-SSE', 'SSE-SE', 'SE-S',
                  'SSE', 'S-SE', 'M-S-SE', 'S-SSE', 'SSE-S',
                  'S', 'S-SSW', 'SSW-S', 'S-SW', 'M-S-SW', 'SSW', 'SSW-SW', 'SW-S', 'SW-SSW', 'SW', 'SW-WSW', 'WSW-SW', 'SW-W', 'W-SW', 'WSW',
                  'WSW-W', 'W-WSW', 'WSW',
                  'W', 'W-WNW', 'WNW-W', 'W-NW', 'WNW', 'WNW-NW', 'NW-W', 'NW-WNW', 'NW', 'NW-NNW', 'NW-N', 'N-NW', 'NNW', 'NNW-N', 'N-NNW', 'w-nnw', 'wsw-wnw']
    for direction in directions:
        text[idx] = re.sub(r'(^|\s)' + re.escape(direction.lower()) + r"((\s)|($)|('ly(\s|$)))", ' <wind_direction> ', text[idx])
    text[idx] = re.sub(r'gusts \d+(-\d+)?', 'gusts <gust_speed>', text[idx])
    text[idx] = re.sub(r'\d+(-\d+)?', '<wind_speed>', text[idx])

newdatastring = ''
for line in newdata:
    num = 0
    while num < len(line):
        if 'WindDir.' in line[num][0]:
            line[num][1] = '<wind_direction>'
        if 'WindSpeedMin.' in line[num][0]:
            line[num][0] = re.sub(r"WindSpeedMin", "WindSpeed", line[num][0])
            line[num][1] = '<wind_speed_min>'
            #if (num != len(line)-1) and ('WindSpeedMax.' in line[num + 1][0]):
                #del line[num+1]
        if 'WindSpeedMax.' in line[num][0]:
            line[num][0] = re.sub(r"WindSpeedMax", "WindSpeed", line[num][0])
            line[num][1] = '<wind_speed_max>'
        if 'GustSpeedMin.' in line[num][0]:
            line[num][0] = re.sub(r"GustSpeedMin", "GustSpeed", line[num][0])
            line[num][1] = '<gust_speed_min>'
            #if (num != len(line)-1) and ('GustSpeedMax.' in line[num + 1][0]):
                #del line[num+1]
        if 'GustSpeedMax.' in line[num][0]:
            line[num][0] = re.sub(r"GustSpeedMax", "GustSpeed", line[num][0])
            line[num][1] = '<gust_speed_max>'
        if 'Time.' in line[num][0]:
            line[num][1] = '<time>'
        if 'WindDirChange.' in line[num][0]:
            line[num][1] = '<wind_direction_change>'
        if 'WindSpeedChange.' in line[num][0]:
            line[num][1] = '<wind_speed_change>'
        if num == len(line) -1:
            newdatastring += line[num][0] + ': ' + line[num][1] + '\n'
        else:
            newdatastring += line[num][0] + ': ' + line[num][1] + ' '
        num += 1

text = [x.strip() for x in text]
text = '\n'.join(text)

with open(currentpath + '/Corpora/All_gaps.text', 'wb') as f:
    f.write(bytes(text, 'UTF-8'))

with open(currentpath + '/Corpora/All_gaps.data', 'wb') as f:
    f.write(bytes(newdatastring, 'UTF-8'))