import os
import regex as re
from numpy.random import choice

currentpath = os.getcwd()

def datamatching(file):
    with open(currentpath + '/Corpora/weather_new/' + file + '_new.text', 'rb') as f:
        text = f.readlines()

    text = [t.decode('utf-8') for t in text]
    datastringlist = []
    for line in text:
        templates = re.findall('<(.*?)>', line)
        datalist = []

        for idx, template in enumerate(templates):
            if template == 'percentage':
                datalist.append('precipPotential_chance: <percentage>')
            elif template == 'cloud_data':
                datalist.append('skyCover_mode: <cloud_data>')
            elif template == 'high_near_low_around_steady_temperature':
                datachoice = choice(['high near', 'low around', 'steady temperature around'], 1, p=[0.4633248159, 0.5329174808, 0.0037577033])
                if datachoice[0] == 'high near':
                    datalist.append('temperature_max')
                elif datachoice[0] == 'low around':
                    datalist.append('temperature_min')
                elif datachoice[0] == 'steady temperature around':
                    datalist.append('temperature_mean')
            elif template == 'temperature':
                datalist.append('temperature_mode: <temperature>')
            elif (template == 'time') or (template == 'time1') or (template == 'time2'):
                datalist.append('Chance_time: <before_after_by> <time>')
            #elif template == 'time1':
                #datalist.append('Chance_time: <time1> <time2>')
            elif template == 'weather_type_and_chance':
                datalist.append('<weather>Chance_mode: <chance>')
            elif template == 'wind_direction':
                datalist.append('windDir_mode: <wind_direction>')
            elif template == 'wind_speed':
                datalist.append('windSpeed_mode: <wind_speed>')
        datastringlist.append(' '.join(datalist))

    newtext = '\n'.join(datastringlist)
    with open('Corpora/weather_new/' + file + '_new.data', 'wb') as f:
        f.write(bytes(newtext, 'UTF-8'))

filelist = ['Train', 'Test', 'Dev', 'All']
for file in filelist:
    text = datamatching(file)