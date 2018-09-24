import regex as re
import os
import itertools
import operator
import sys
from Cloud_Filler import convertclouds, graduallybecoming
from Temperature_Filler import converttemperature, fallingrising
from Weather_Filler import convertweather
from Time_Filler import converttime
from random import choice
from Wind_Filler import winddirection, windspeed
from Percent_Filler import convertpercentage

currentpath = os.getcwd()

def Get_Templates(filename):
    with open(os.path.dirname(currentpath) + '/Corpora/weather_new/' + filename + '.data', 'rb') as f:
        data = f.readlines()
    data = [t.decode('utf-8') for t in data]

    with open(os.path.dirname(currentpath) + '/Corpora/weather_new/' + filename + '_new2.data', 'rb') as f:
        templates = f.readlines()
    templates = [t.decode('utf-8') for t in templates]

    for idx, line in enumerate(templates):
        if not re.search(r"\w", data[idx]):
            templates[idx] = '\n'
            continue
        weathertemplates = []
        #Get a list of the templates in the line, to determine which script to use
        templatesline = re.findall('(<(.*?)>)', templates[idx])
        templatesline = [t[0] for t in templatesline]
        linetemplates = [''] * len(templatesline)
        for templateidx, templateval in enumerate(templatesline):
            if linetemplates[templateidx] != '':
                continue
            if templatesline[templateidx] == '<percentage>':
                linetemplates[templateidx] = convertpercentage(data[idx])
            if templatesline[templateidx] == '<cloud_data>':
                if (templateidx != len(templatesline)-1) and (templatesline[templateidx + 1] == '<cloud_data>'):
                    clouddata = graduallybecoming(data[idx])
                    linetemplates[templateidx] = clouddata[0]
                    # If there is a gradually becoming structure (a first cloud data template and after that a second cloud data)
                    # This combination of two is calculated by the graduallybecoming function
                    # So the next cloud data will be filled by the graduallybecoming function
                    linetemplates[templateidx+1] = clouddata[1]
                else:
                    linetemplates[templateidx] = convertclouds(data[idx])
            elif templatesline[templateidx] == '<min_mean_max>':
                temperaturedata = converttemperature(data[idx])
                linetemplates[templateidx] = temperaturedata[0]
                #The temperature template always follows the min/mean/max template and it is calculated within converttemperature
                #So the next temperature mention can be removed from the list
                linetemplates[templateidx+1] = temperaturedata[1]
            elif templatesline[templateidx] == '<temperature>':
                temperaturedata = fallingrising(data[idx])
                #Function that finds all indexes when searching for one or multiple items
                find = lambda searchList, elem: [[i for i, x in enumerate(searchList) if x == e] for e in elem]
                #Get the index of the second temperature mention
                secondtempfind = find(templatesline, ['<temperature>'])[0][1]
                linetemplates[templateidx] = temperaturedata[0]
                #If temperature is found that means a <falling/rising> construction in the text, meaning that a second temperature mention can be found somewhere
                linetemplates[secondtempfind] = temperaturedata[1]

            elif templatesline[templateidx] == '<day/night>':
                if re.search(r"rainChance.time:17-30", data[idx]):
                    linetemplates[templateidx] = 'night'
                else:
                    linetemplates[templateidx] = 'day'
            elif templatesline[templateidx] == '<weather>':
                weathertuple = convertweather(data[idx], linetemplates, templatesline[:templateidx], templatesline[templateidx+1:])
                linetemplates[templateidx] = weathertuple[0]
                linetemplates[templateidx+1] = weathertuple[1]
                weathertemplates.append(weathertuple[0])
            elif (templatesline[templateidx] == '<before_after_by>'):
                timedata = converttime(data[idx], weathertemplates, templatesline[:templateidx])
                linetemplates[templateidx] = timedata[0]
                linetemplates[templateidx + 1] = timedata[1]
            elif templatesline[templateidx] == '<wind_direction>':
                linetemplates[templateidx] = winddirection(data[idx])
            elif templatesline[templateidx] == '<wind_speed>':
                windspeeds = windspeed(data[idx], templatesline[templateidx+1:])
                find = lambda searchList, elem: [[i for i, x in enumerate(searchList) if x == e] for e in elem]
                # Get the index of the second temperature mention
                wsfind = find(templatesline, ['<wind_speed>'])[0]
                if len(wsfind) == 1:
                    linetemplates[templateidx] = windspeeds[0]
                else:
                    linetemplates[templateidx] = windspeeds[0]
                    linetemplates[wsfind[1]] = windspeeds[1]

        for templateidx, templateval in enumerate(templatesline):
            templates[idx] = re.sub(re.escape(templateval), linetemplates[templateidx], templates[idx], count=1)

    return templates

for file in ['All', 'Dev', 'Test', 'Train']:
    templates = Get_Templates(file)
    templatelines = ''.join(templates)

    with open(os.path.dirname(currentpath) + '/Corpora/weather_new/' + file + '_new2_filled.data', 'wb') as f:
        f.write(bytes(templatelines, 'UTF-8'))