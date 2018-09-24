import os
import regex as re
import numpy as np

def winddirchange(prevwind, currwind):
    # Sort winddirections going clockwise starting from north
    directions = ['N', 'M-N', 'N-NNE', 'NNE-N', 'N-NE', 'NNE', 'NNE-NE', 'NE-N', 'NE-NNE', 'M-NE', 'NE', 'NE-ENE', 'ENE-NE', 'NE-E', 'ENE', 'E-NE', 'E-ENE',
                  'E', 'E-ESE', 'ESE-E', 'E-SE', 'ESE', 'ESE-SE', 'SE-E', 'SE-ESE', 'M-SE', 'ORVAR-SE', 'MVAR-SE', 'SE', 'SE-SSE', 'SSE-SE', 'SE-S', 'SSE', 'S-SE', 'M-S-SE', 'S-SSE', 'SSE-S',
                  'S', 'S-SSW', 'SSW-S', 'S-SW', 'M-S-SW', 'SSW', 'SSW-SW', 'SW-S', 'SW-SSW', 'SW', 'SW-WSW', 'WSW-SW', 'SW-W', 'W-SW', 'WSW', 'WSW-W', 'W-WSW', 'WSW',
                  'W', 'W-WNW', 'WNW-W', 'W-NW', 'WNW', 'WNW-NW', 'NW-W', 'NW-WNW', 'NW', 'NW-NNW', 'NW-N', 'N-NW', 'NNW', 'NNW-N', 'N-NNW']

    unknowns = ['-', 'VAR', 'CVAR'] # Unknown values

    if currwind == '-':
        return 'same'

    previndex = directions.index(prevwind)  # Get the previous winddirection
    prevlist = directions[previndex:] + directions[:previndex]  # Convert the directionslist so that the previous winddirection is the first one in the list
    medianindex = np.argsort(prevlist)[len(prevlist) // 2]  # Get the index of the median
    currindex = prevlist.index(currwind)  # Index of the current winddirection

    if currindex <= medianindex:  # If the current index is closer to the previous one in the list (less or equal to the median), the wind has changed clockwise
        return 'clock'
    else:  # Else the wind has changed counter clockwise
        return 'ctrclock'

def windspeedchange(prevwind, currwind):
    prevwind = [x for x in prevwind if x.isdigit()]
    currwind = [x for x in currwind if x.isdigit()]
    prevwind = [int(x) for x in prevwind]
    currwind = [int(x) for x in currwind]

    prevwind = np.mean(prevwind)
    currwind = np.mean(currwind)
    if currwind < prevwind:
        return 'down'
    else:
        return 'up'

def return_list(windlist):
    if (windlist[0].isdigit()) and (windlist[1].isdigit()):
        return windlist
    elif windlist[0].isdigit():
        return [windlist[0]]
    elif windlist[1].isdigit():
        return [windlist[1]]
    else:
        return None

def convert_data(file):
    currentpath = os.getcwd()
    with open(currentpath + '/Corpora/' + file + '.data', 'rb') as f:
        text = f.readlines()
    text = [x.decode('utf-8') for x in text]
    print(text)

    linestringlist = []

    text = [re.findall(r"\[(.*?)\]", line) for line in text]
    for idx, line in enumerate(text):
        text[idx] = [re.sub(r"\[", "", x) for x in text[idx]]
        text[idx] = [x.split(',') for x in text[idx]]
        text[idx] = [[x[0]] + [x[1].replace('_', '')] + x[2:] for x in text[idx]]

        previouswinddir = []
        previouswindspeed = []
        previousgustspeed = []
        linestring = ''
        for timepointidx, timepoint in enumerate(text[idx]):
            if timepointidx == 0:
                #If the winddirection part for the first timepoint is actually a wind direction, append it to the list keeping track of wind directions
                #And also add information in the dataline if there is wind direction info
                if (timepoint[1] != '-') and (timepoint[1] != 'VAR') and (timepoint[1] != 'CVAR'):
                    previouswinddir.append(timepoint[1])
                    linestring += 'WindDir.1: ' + timepoint[1] + ' '
                #Add windspeed and gustspeed info to the datastring if there is any
                if timepoint[2].isdigit():
                    linestring += 'WindSpeedMin.1: ' + timepoint[2] + ' '
                if timepoint[3].isdigit():
                    linestring += 'WindSpeedMax.1: ' + timepoint[3] + ' '
                if timepoint[4].isdigit():
                    linestring += 'GustSpeedMin.1: ' + timepoint[4] + ' '
                if timepoint[5].isdigit():
                    linestring += 'GustSpeedMax.1: ' + timepoint[5] + ' '
                #Add the time info to the datastring (unedited)
                if timepoint[6] != '-1':
                    linestring += 'Time.1: ' + timepoint[6] + ' '

                #Use the function to determine if there is any wind or gust information and if so, append it to the lists keeping track of that
                if return_list(timepoint[2:4]) != None:
                    previouswindspeed.append(timepoint[2:4])
                if return_list(timepoint[4:6]) != None:
                    previousgustspeed.append(timepoint[4:6])
            else:
                if (timepoint[1] != 'VAR') and (timepoint[1] != 'CVAR'): #If the wind direction is known
                    if len(previouswinddir) > 0: #And there is previous winddir information, use the function to find the direction of the change
                        linestring += 'WindDirChange.' + str(timepointidx+1) + ': ' + winddirchange(previouswinddir[-1], timepoint[1]) + ' '
                    if timepoint[1] != '-': #And append to the winddirlist if this is a new wind direction
                        previouswinddir.append(timepoint[1])
                        linestring += 'WindDir.' + str(timepointidx+1) + ': ' + timepoint[1] + ' '
                if len(previouswindspeed) > 0:
                    if (timepoint[2] == '-') and (timepoint[3] == '-'): #If both windspeeds are a dash, they are the same as the previous one
                        linestring += 'WindSpeedChange.' + str(timepointidx+1) + ': same '
                    elif (timepoint[2] == '-') and (timepoint[3].isdigit()): #If one of them is a dash, use the information from the previous windspeed
                        newtimepoint = previouswindspeed[-1][0]
                        wschange = windspeedchange(previouswindspeed[-1], [newtimepoint, timepoint[3]])
                        linestring += 'WindSpeedChange.' + str(timepointidx+1) + ': ' + wschange + ' '
                        previouswindspeed.append(timepoint[2:4])
                    elif (timepoint[3] == '-') and (timepoint[2].isdigit()):
                        newtimepoint = previouswindspeed[-1][1]
                        wschange = windspeedchange(previouswindspeed[-1], [timepoint[2], newtimepoint])
                        linestring += 'WindSpeedChange.' + str(timepointidx+1) + ': ' + wschange + ' '
                        previouswindspeed.append(timepoint[2:4])
                    elif (timepoint[2].isdigit()) and (timepoint[3].isdigit()):
                        wschange = windspeedchange(previouswindspeed[-1], [timepoint[2], timepoint[3]])
                        linestring += 'WindSpeedChange.' + str(timepointidx+1) + ': ' + wschange + ' '
                        previouswindspeed.append(timepoint[2:4])
                # Add windspeed and gustspeed info to the datastring if there is any
                if timepoint[2].isdigit():
                    linestring += 'WindSpeedMin.' + str(timepointidx+1) + ': ' + timepoint[2] + ' '
                if timepoint[3].isdigit():
                    linestring += 'WindSpeedMax.' + str(timepointidx+1) + ': ' + timepoint[3] + ' '
                if len(previousgustspeed) > 0:
                    if (timepoint[2] == '-') and (timepoint[3] == '-'): #If both gustspeeds are a dash, they are the same as the previous one
                        linestring += 'GustSpeedChange.' + str(timepointidx+1) + ': same '
                    elif (timepoint[2] == '-') and (timepoint[3].isdigit()): #If one of them is a dash, use the information from the previous gustspeed
                        newtimepoint = previousgustspeed[-1][0]
                        wschange = windspeedchange(previousgustspeed[-1], [newtimepoint, timepoint[3]])
                        linestring += 'GustSpeedChange.' + str(timepointidx+1) + ': ' + wschange  + ' '
                        previousgustspeed.append(timepoint[2:4])
                    elif (timepoint[3] == '-') and (timepoint[2].isdigit()):
                        newtimepoint = previousgustspeed[-1][1]
                        wschange = windspeedchange(previousgustspeed[-1], [timepoint[2], newtimepoint])
                        linestring += 'GustSpeedChange.' + str(timepointidx+1) + ': ' + wschange  + ' '
                        previousgustspeed.append(timepoint[2:4])
                    elif (timepoint[2].isdigit()) and (timepoint[3].isdigit()):
                        wschange = windspeedchange(previousgustspeed[-1], [timepoint[2], timepoint[3]])
                        linestring += 'GustSpeedChange.' + str(timepointidx+1) + ': ' + wschange  + ' '
                        previousgustspeed.append(timepoint[2:4])
                if timepoint[4].isdigit():
                    linestring += 'GustSpeedMin.' + str(timepointidx+1) + ': ' + timepoint[4] + ' '
                if timepoint[5].isdigit():
                    linestring += 'GustSpeedMax.' + str(timepointidx+1) + ': ' + timepoint[5] + ' '
                #Add the time info to the datastring (unedited)
                if timepoint[6] != '-1':
                    linestring += 'Time.' + str(timepointidx+1) + ': ' + timepoint[6] + ' '
        linestring = linestring.strip()
        linestringlist.append(linestring)

    liststring = '\n'.join(linestringlist)
    return liststring

for file in ['All', 'Dev', 'Test', 'Train']:
    currentpath = os.getcwd()
    liststring = convert_data(file)
    with open(currentpath + '/Corpora/' + file + '2.data', 'wb') as f:
        print('Writing new file')
        f.write(bytes(liststring, 'UTF-8'))



