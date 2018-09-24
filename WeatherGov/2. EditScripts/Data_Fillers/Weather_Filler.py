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
            if (re.search(r"\bfreezingRain\b", previoustemplate)):
                try:
                    weatherdict.pop('freezingRain')
                except KeyError:
                    ''
            if (re.search(r"\brain\b", previoustemplate)):
                try:
                    weatherdict.pop('rain')
                except KeyError:
                    ''
            if (re.search(r"\bthunder\b", previoustemplate)):
                try:
                    weatherdict.pop('thunder')
                except KeyError:
                    ''
            if (re.search(r"\bsnow\b", previoustemplate)):
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
        if '<weather>' in previousgaps:
            #Look at the last two positions of the weatherdict
            weatherdict = {k:v[-2:] for (k,v) in weatherdict.items()}
        elif '<weather>' in nextgaps:
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
    return possibilities[0], possibilities[1]