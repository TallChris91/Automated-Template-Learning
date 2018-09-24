import regex as re
from numpy.random import choice

s = 'temperature.time:6-21 temperature.min:26 temperature.mean:33 temperature.max:40 windChill.time:6-21 windChill.min:14 windChill.mean:24 windChill.max:32 windSpeed.time:6-21 windSpeed.min:11 windSpeed.mean:14 windSpeed.max:16 windSpeed.mode-bucket-0-20-2:10-20 windDir.time:6-21 windDir.mode:SE gust.time:6-21 gust.min:0 gust.mean:0 gust.max:0 skyCover.time:6-21 skyCover.mode-bucket-0-100-4:75-100 skyCover.time:6-9 skyCover.mode-bucket-0-100-4:75-100 skyCover.time:6-13 skyCover.mode-bucket-0-100-4:75-100 skyCover.time:9-21 skyCover.mode-bucket-0-100-4:75-100 skyCover.time:13-21 skyCover.mode-bucket-0-100-4:75-100 precipPotential.time:6-21 precipPotential.min:26 precipPotential.mean:39 precipPotential.max:58 thunderChance.time:6-21 thunderChance.mode:-- thunderChance.time:6-9 thunderChance.mode:-- thunderChance.time:6-13 thunderChance.mode:-- thunderChance.time:9-21 thunderChance.mode:-- thunderChance.time:13-21 thunderChance.mode:-- rainChance.time:6-21 rainChance.mode:-- rainChance.time:6-9 rainChance.mode:-- rainChance.time:6-13 rainChance.mode:-- rainChance.time:9-21 rainChance.mode:-- rainChance.time:13-21 rainChance.mode:-- snowChance.time:6-21 snowChance.mode:Chc snowChance.time:6-9 snowChance.mode:SChc snowChance.time:6-13 snowChance.mode:SChc snowChance.time:9-21 snowChance.mode:Chc snowChance.time:13-21 snowChance.mode:Lkly freezingRainChance.time:6-21 freezingRainChance.mode:-- freezingRainChance.time:6-9 freezingRainChance.mode:-- freezingRainChance.time:6-13 freezingRainChance.mode:-- freezingRainChance.time:9-21 freezingRainChance.mode:-- freezingRainChance.time:13-21 freezingRainChance.mode:-- sleetChance.time:6-21 sleetChance.mode:-- sleetChance.time:6-9 sleetChance.mode:-- sleetChance.time:6-13 sleetChance.mode:-- sleetChance.time:9-21 sleetChance.mode:-- sleetChance.time:13-21 sleetChance.mode:--'

def convertweather(dataline, previoustemplates, previousgaps, nextgaps):
    weathertype = ['thunder', 'rain', 'snow', 'freezingRain', 'sleet']
    weatherdict = {}
    possibilities = {}
    for weather in weathertype:
        matchlist = re.findall(re.escape(weather) + r"Chance\.mode:([^-]*?)(\s|$)", dataline)
        matchlist = [i[0] for i in matchlist]
        if len(matchlist) > 0:
            weatherdict.update({weather: matchlist})
    # If there is a chance of several weather types occuring, we will look which weather type was used for the previous gap and use a different one
    if len(weatherdict) > 1:
        for previoustemplate in previoustemplates:
            if (re.search(r"\bfreezing drizzle\b", previoustemplate)) or (re.search(r"\bfreezing drizzle\b", previoustemplate)) or (re.search(r"\bfreezing rain\b", previoustemplate)):
                try:
                    weatherdict.pop('freezingRain')
                except KeyError:
                    ''
            if (re.search(r"\bdrizzle\b", previoustemplate)) or (re.search(r"\bsprinkles\b", previoustemplate)) or (re.search(r"\brain\b", previoustemplate)) or (re.search(r"\brain\b", previoustemplate)) or (re.search(r"\bshowers\b", previoustemplate)):
                try:
                    weatherdict.pop('rain')
                except KeyError:
                    ''
            if (re.search(r"\bthunderstorms\b", previoustemplate)) or (re.search(r"\bthunderstorm\b", previoustemplate)):
                try:
                    weatherdict.pop('thunder')
                except KeyError:
                    ''
            if (re.search(r"\bsnow\b", previoustemplate)) or (re.search(r"\bflurries\b", previoustemplate)):
                try:
                    weatherdict.pop('snow')
                except KeyError:
                    ''
            if (re.search(r"\bsleet\b", previoustemplate)):
                try:
                    weatherdict.pop('sleet')
                except KeyError:
                    ''
    #Now let's see if there is a previous or future gap about the weather type
    else:
        if '<weather_type_and_chance>' in previousgaps:
            #Look at the last two positions of the weatherdict
            weatherdict = {k:v[-2:] for (k,v) in weatherdict.items()}
        elif '<weather_type_and_chance>' in nextgaps:
            #Look at the first two positions of the weatherdict
            weatherdict = {k:v[:2] for (k,v) in weatherdict.items()}

    #Now let's go over the dictionary from the most certain to the least certain chance (Def, Lkly, Chc, SChc)
    likeliness = ['Def', 'Lkly', 'Chc', 'SChc']
    for chance in likeliness:
        #Go over every key in the dict
        for key in weatherdict:
            #And every possible value of the dict key
            for value in weatherdict[key]:
                #If a value in the dictionary is the chance
                if value == chance:
                    #Add it to the list of possibilities
                    possibilities.update({key: chance})
        #If there are already possibilities found, we don't have to look for a less certain possibility
        if len(possibilities) > 0:
            break
    #Let's just pick a random possibility if there is more than one possibilities
    if len(possibilities) > 1:
        #Randomly pick a key
        randomchoice = choice(list(possibilities))
        #And add the corresponding value
        possibilities = (randomchoice, possibilities[randomchoice])
    elif len(possibilities) == 1:
        #Convert the one-item dictionary to a tuple
        possibilities = list(possibilities.items())[0]
    else:
        # If in the end, no possibility of weather was found, then we'll just gamble and random stratified pick one of the options
        possibilities = ('other', 'Unk')
    if possibilities[0] == 'other':
        plist = [76, 461, 1, 7, 28, 12, 68, 142, 8, 17, 32, 22, 3, 697, 83, 22, 1, 1369, 2072, 15, 5, 222, 1316, 37, 378, 131, 356, 30, 234, 179, 358,
                 26, 2, 6996, 5204, 920]
        plist = [float(i) / sum(plist) for i in plist]
        datachoice = list(choice(['areas of fog', 'patchy fog', 'patchy freezing fog', 'areas of freezing fog', 'areas of frost', 'areas of blowing dust',
                                  'freezing rain and sleet', 'rain and sleet', 'showers and sleet', 'snow and sleet', 'sleet', 'scattered snow showers',
                                  'scattered snow', 'snow showers', 'scattered flurries', 'flurries', 'light snow', 'snow', 'showers and thunderstorms',
                                  'rain and thunderstorms', 'scattered thunderstorms', 'thunderstorms', 'a thunderstorm', 'freezing drizzle', 'freezing rain',
                                  'rain or freezing rain', 'drizzle', 'sprinkles', 'isolated showers', 'scattered showers', 'rain showers', 'scattered rain showers',
                                  'scattered rain', 'showers', 'rain', 'rain or drizzle'], 1, p=plist))[0]
    elif possibilities[0] == 'sleet':
        plist = [0.25468164794, 0.53183520599, 0.02996254681, 0.06367041198, 0.11985018726]
        plist = [float(i) / sum(plist) for i in plist]
        datachoice = list(
            choice(['freezing rain and sleet', 'rain and sleet', 'showers and sleet', 'snow and sleet', 'sleet'], 1,
                   p=plist))[0]
    elif possibilities[0] == 'snow':
        plist = [0.01001365498, 0.0013654984, 0.31725079654, 0.03777878925, 0.01001365498, 0.00045516613, 0.62312243969]
        plist = [float(i) / sum(plist) for i in plist]
        datachoice = list(
            choice(['scattered snow showers', 'scattered snow', 'snow showers', 'scattered flurries', 'flurries', 'light snow', 'snow'], 1,
                   p=plist))[0]
    elif possibilities[0] == 'thunder':
        plist = [0.00137551581, 0.57001375515, 0.00412654745, 0.00137551581, 0.06107290233, 0.36203576341]
        plist = [float(i) / sum(plist) for i in plist]
        datachoice = list(
            choice(['scattered thunderstorms', 'showers and thunderstorms', 'rain and thunderstorms', 'scattered thunderstorms', 'thunderstorms', 'a thunderstorm'], 1,
                   p=plist))[0]
    elif possibilities[0] == 'freezingRain':
        plist = [0.06776556776, 0.93223443223]
        plist = [float(i) / sum(plist) for i in plist]
        datachoice = list(
            choice(['freezing drizzle', 'freezing rain'], 1,
                   p=plist))[0]
    elif possibilities[0] == 'rain':
        plist = [0.02419135634, 0.00203859744, 0.01590106007, 0.01216363142, 0.02432726284, 0.00176678445, 0.00013590649, 0.47540092416,
                 0.35362870345, 0.06251698831]
        plist = [float(i) / sum(plist) for i in plist]
        datachoice = list(
            choice(['drizzle', 'sprinkles', 'isolated showers', 'scattered showers', 'rain showers', 'scattered rain showers', 'scattered rain', 'showers', 'rain', 'rain or drizzle'], 1,
                   p=plist))[0]
    #For the unknown and definitive values, we don't need to add anything to our selected weather term
    if (possibilities[1] == 'Unk') or (possibilities[1] == 'Def'):
        pass
    #Add 'likely' behind the weather term if the possibility is 'Lkly'
    elif possibilities == 'Lkly':
        datachoice = datachoice + ' likely'
    elif possibilities == 'Chc':
        plist = [0.21106005387, 0.78893994612]
        plist = [float(i) / sum(plist) for i in plist]
        secondchoice = list(choice(['possibly ', 'a chance of '], 1, p=plist))[0]
        datachoice = secondchoice + datachoice
    elif possibilities == 'SChc':
        datachoice = 'a slight chance of ' + datachoice
    return datachoice, possibilities[0]