from random import choice
import regex as re

def winddirection(dataline):
    #The wind direction data is often not accurate and they usually give two wind directions one of which might be the direction in the data
    #Let's just choose the wind direction from the data. Yolo.
    datachoice = re.search(r"windDir.mode:(.*?) ", dataline)
    if datachoice:
        datachoice = datachoice.group(1).lower()
    #If this doesn't work for some reason, return a random option
    else:
        datachoice = list(choice(['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'nne', 'ene', 'ese', 'sse', 'ssw', 'wsw', 'wnw', 'nnw', 'calm', 'light']))[0]
    return datachoice

def windspeed(dataline, futuretemplates):
    #If there are two wind speeds
    if (len(futuretemplates) > 0) and (futuretemplates[0] == '<wind_speed>'):
        #Use the min and max for wind speeds (they are, again, not very accurately aligned)
        #Sometimes windSpeed isn't in the information, so then you need to look at gusts
        minspeed = re.search(r'windSpeed.min:(.*?)(\s|$)', dataline)
        maxspeed = re.search(r'windSpeed.max:(.*?)(\s|$)', dataline)
        if minspeed:
            minspeed = minspeed.group(1)
            maxspeed = maxspeed.group(1)
        else:
            #Use mean because min is always 0
            minspeed = re.search(r'gust.mean:(.*?)(\s|$)', dataline)
            maxspeed = re.search(r'gust.max:(.*?)(\s|$)', dataline)
            minspeed = minspeed.group(1)
            maxspeed = maxspeed.group(1)
        return [minspeed, maxspeed]
    else:
        #Go for the maximum which seems to be the default in most cases
        maxspeed = re.search(r'windSpeed.max:(.*?)(\s|$)', dataline)
        if maxspeed:
            maxspeed = maxspeed.group(1)
        else:
            maxspeed = re.search(r'gust.max:(.*?)(/s|$)', dataline)
            maxspeed = maxspeed.group(1)
        return [maxspeed]