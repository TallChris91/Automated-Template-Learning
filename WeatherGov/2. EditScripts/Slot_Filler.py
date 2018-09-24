import regex as re
import os
import itertools
import operator
import sys
from Cloud_Filler import convertclouds, graduallybecoming
from Temperature_Filler import converttemperature, fallingrising, exceptiontemperature
from Weather_Filler import convertweather
from Time_Filler import converttime, twotimes
from random import choice
from Wind_Filler import winddirection, windspeed
from Percent_Filler import convertpercentage

currentpath = os.getcwd()

def Get_Templates(filename):
    with open(currentpath + '/Corpora/weather_new/Backup/' + filename + '.data', 'rb') as f:
        data = f.readlines()
    data = [t.decode('utf-8') for t in data]

    #with open(currentpath + '/Corpora/weather_new/' + filename + '_new2_UnoptimizedWeatherGov2_Gaps.text', 'rb') as f:
    with open('C:/Users/labuser.DESKTOP-5A8OFV4/Desktop/Run22.txt', 'rb') as f:
        templates = f.readlines()
    templates = [t.decode('utf-8') for t in templates]

    for idx, line in enumerate(templates):
        if not re.search(r"\w", data[idx]):
            continue
        linetemplates = []
        weathertemplates = []
        #Get a list of the templates in the line, to determine which script to use
        templatesline = re.findall('(<(.*?)>)', templates[idx])
        templatesline = [t[0] for t in templatesline]
        templateslinecopy = templatesline[:]
        templateidx = 0
        while templateidx < len(templatesline):
            if templatesline[templateidx] == '<percentage>':
                linetemplates.append(convertpercentage(data[idx]))
            if templatesline[templateidx] == '<cloud_data>':
                if '<gradual/gradually becoming>' in templatesline:
                    clouddata = graduallybecoming(data[idx])
                    if clouddata[1] == 'clearing':
                        linetemplates.extend([clouddata[0], 'gradual', clouddata[1]])
                    else:
                        linetemplates.extend([clouddata[0], 'gradually becoming', clouddata[1]])
                    # The gradual/gradually becoming template always follows the first cloud data template and after that always comes the second cloud data
                    # This combination of three is calculated by the graduallybecoming function
                    # So all the cloud_data templates and gradual/gradually becoming templates can be removed because they have been filled by the graduallybecoming function
                        templatesline[templateidx + 1:] = [t for t_idx, t in enumerate(templatesline[templateidx + 1:]) if
                                                           (t != '<cloud_data>') and (t != '<gradual/gradually becoming>')]
                else:
                    linetemplates.append(convertclouds(data[idx]))
            elif templatesline[templateidx] == '<high_near_low_around_steady_temperature>':
                temperaturedata = converttemperature(data[idx])
                linetemplates.extend(list(temperaturedata))
                #The temperature template always follows the high near/low around/steady temperature template and it is calculated within converttemperature
                #So the next temperature mention can be removed from the list
                if templatesline[templateidx + 1] == '<temperature>':
                    del (templatesline[templateidx + 1])
            elif templatesline[templateidx] == '<falling/rising>':
                if 'falling' in linetemplates:
                    temperaturedata = fallingrising(data[idx], 'rising')
                elif 'rising' in linetemplates:
                    temperaturedata = fallingrising(data[idx], 'falling')
                else:
                    temperaturedata = fallingrising(data[idx])
                linetemplates.extend(list(temperaturedata))
                # The temperature template always follows the falling/rising template and it is calculated within fallingrising
                # So the next temperature mention can be removed from the list
                if (len(templatesline[templateidx+1:]) > 0) and (templatesline[templateidx + 1] == '<temperature>'):
                    del (templatesline[templateidx + 1])
            elif templatesline[templateidx] == '<temperature>':
                linetemplates.extend(list(exceptiontemperature(data[idx], templatesline[:templateidx])))
            elif templatesline[templateidx] == '<day/night>':
                if re.search(r"rainChance.time:17-30", data[idx]):
                    linetemplates.append('night')
                else:
                    linetemplates.append('day')
            elif templatesline[templateidx] == '<weather_type_and_chance>':
                weathertuple = convertweather(data[idx], linetemplates, templatesline[:templateidx], templatesline[templateidx+1:])
                linetemplates.append(weathertuple[0])
                weathertemplates.append(weathertuple[1])
            elif (templatesline[templateidx] == '<time>') or (templatesline[templateidx] == '<time2>'):
                linetemplates.extend(converttime(data[idx], weathertemplates, templatesline[:templateidx]))
            elif templatesline[templateidx] == '<time1>':
                betweentimes = list(twotimes(data[idx], weathertemplates))
                linetemplates.extend(betweentimes)
                #We've already taken care of time 2, so that one can be removed from the list
                if templatesline[templateidx + 1] == '<time2>':
                    del (templatesline[templateidx + 1])
            elif templatesline[templateidx] == '<frequency>':
                frequencychoice = list(choice(['occasional', 'periods of']))[0]
                linetemplates.append(frequencychoice)
            elif templatesline[templateidx] == '<wind_direction>':
                linetemplates.append(winddirection(data[idx]))
            elif templatesline[templateidx] == '<wind_speed>':
                windspeeds = windspeed(data[idx], templatesline[templateidx+1:])
                linetemplates.extend(windspeeds)
                #If the next template was also a wind speed template, it is taken care of by the function so it can be removed
                if (len(templatesline[templateidx+1:]) > 0) and (templatesline[templateidx + 1] == '<wind_speed>'):
                    del (templatesline[templateidx + 1])
            templateidx += 1

        for templateidx, templateval in enumerate(templateslinecopy):
            try:
                templates[idx] = re.sub(re.escape(templateval), linetemplates[templateidx], templates[idx], count=1)
            except IndexError:
                print(idx)
                print(templates[idx])
                print(templateslinecopy)
                print(linetemplates)
                sys.exit(1)

    return templates

templates = Get_Templates('Test')
templatelines = ''.join(templates)

#with open(currentpath + '/Corpora/weather_new/Test_new2_UnoptimizedWeatherGov_Filled.text' + '', 'wb') as f:
with open(currentpath + '/Corpora/weather_new/Test_Moses_Gaps_Filled.txt', 'wb') as f:
    f.write(bytes(templatelines, 'UTF-8'))
