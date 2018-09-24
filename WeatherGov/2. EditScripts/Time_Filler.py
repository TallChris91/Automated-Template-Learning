import regex as re
from numpy.random import choice

def converttime(dataline, weathertemplates, previoustemplates):
    if len(weathertemplates) > 0:
        weather = weathertemplates[-1]
    matchfound = 'n'
    if (len(weathertemplates)) > 0 and (weather != 'other'):
        # After 1 am
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'after 1 am'
        #Before 1 am (and rarer cases: before 2 am)
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            plist = [0.93388429752, 0.06611570247]
            plist = [float(i)/sum(plist) for i in plist]
            datachoice = list(
                choice(['before 1am', 'before 2am'], 1,
                       p=plist))[0]
        #After 2 am (and after 3 am, after 4 am)
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            plist = [0.05839416058, 0.56350364963, 0.37810218978]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['after 2am', 'after 3am', 'after 4am'], 1,
                       p=plist))[0]
        # Before 3 am (and before 4 am)
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            plist = [0.85483870967, 0.14516129032]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['before 3am', 'before 4am'], 1,
                       p=plist))[0]
        #After 9 am (and 10 am)
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:6-13 " + re.escape(weather) +  r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            plist = [0.39590443686, 0.60409556314]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['after 9am', 'after 10am'], 1,
                       p=plist))[0]
        # Before 9 am (and 10 am)
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-13 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            plist = [0.27692307692, 0.72307692307]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['before 9am', 'before 10am'], 1,
                       p=plist))[0]
        # After 11 am/noon/1pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:6-13 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            plist = [0.06445437141, 0.73580089342, 0.19974473516]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['after 11am', 'after noon', 'after 1pm'], 1,
                       p=plist))[0]
        # Before 11 am/noon/1pm/2pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:6-9 "
                           + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-13 " + re.escape(weather)
                           + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:-- "
                           + re.escape(weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            plist = [0.16053019145, 0.68483063328, 0.12567501227, 0.02896416298]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['before 11am', 'before noon', 'before 1pm', 'before 2pm'], 1,
                       p=plist))[0]
        #After 2pm/3pm/4pm/5pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather)
                           + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:6-13 "
                           + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather)
                           + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline   )
        if match:
            matchfound = 'y'
            plist = [0.12612612612, 0.61801801801, 0.25405405405, 0.0018018018]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['after 2pm', 'after 3pm', 'after 4pm', 'after 5pm'], 1,
                       p=plist))[0]
        # Before 3pm/4pm/5pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-13 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            plist = [0.93617021276, 0.06382978723]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['before 3pm', 'before 4pm'], 1,
                       p=plist))[0]
        #Before 8pm/9pm/10pm
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            plist = [0.00947867298, 0.18641390205, 0.80410742496]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['before 8pm', 'before 9pm', 'before 10pm'], 1,
                       p=plist))[0]
        #After 9pm/10pm
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            plist = [0.1554054054, 0.84459459459]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['after 9pm', 'after 10pm'], 1,
                       p=plist))[0]
        #After 11pm/midnight
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            plist = [0.08535825545, 0.91464174454]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['after 11pm', 'after midnight'], 1,
                       p=plist))[0]
        # Before 11pm/midnight
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            plist = [0.23770491803, 0.76229508196]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['before 11pm', 'before midnight'], 1,
                       p=plist))[0]

    #If a match is still not found, we will look if this is one of these rare cases where the time is about the temperature
    if matchfound == 'n':
        if (len(previoustemplates) > 2) and (previoustemplates[-2] == '<temperature>'):
            if re.search(r'temperature.time:6-21', dataline):
                datachoice = 'by 9am'
            else:
                datachoice = 'by midnight'

        else:
            # Just pick a random stratified one if we cannot extract the time with the above rules
            matchfound = 'y'
            plist = [0.0112808226, 0.0007986423, 0.00399321154, 0.03853449136, 0.02585604472, 0.01587301587, 0.00269541778, 0.0347409404,
                     0.05300988319,
                     0.01976639712, 0.05161225915, 0.01008285913, 0.11510432265, 0.0312468803, 0.03264450434, 0.13926325247, 0.02555655385,
                     0.00588998702,
                     0.00698812019, 0.03424178895, 0.01407607067, 0.00009983028, 0.00439253269, 0.00029949086, 0.00059898173, 0.01177997404,
                     0.05081361685,
                     0.0068882899, 0.03743635819, 0.01367674952, 0.14655086353, 0.0260557053, 0.08355795148]
            plist = [float(i) / sum(plist) for i in plist]
            datachoice = list(
                choice(['before 1am', 'before 2am', 'after 2am', 'after 3am', 'after 4am', 'before 3am', 'before 4am', 'after 9am', 'after 10am',
                        'before 9am',
                        'before 10am', 'after 11am', 'after noon', 'after 1pm', 'before 11am', 'before noon', 'before 1pm', 'before 2pm',
                        'after 2pm', 'after 3pm',
                        'after 4pm', 'after 5pm', 'before 3pm', 'before 4pm', 'before 8pm', 'before 9pm', 'before 10pm', 'after 9pm',
                        'after 10pm',
                        'after 11pm', 'after midnight', 'before 11pm', 'before midnight'], 1,
                       p=plist))[0]

    #If there is a before/after/by template before this one, return the time in two
    if (len(previoustemplates) > 0) and (previoustemplates[-1] == '<before_after_by>'):
        return datachoice.split(' ')
    #Else return the time as one part
    else:
        return [datachoice]

def twotimes(dataline, weathertemplates):
    weather = weathertemplates[-1]
    possibletimes = []
    if weather != 'other':
        #Between 10pm and 1am
        regex = re.compile(re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:([^-]*?) ")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('10pm', '1am'), 10])
        #Between 9pm and 3am
        #Between 11pm and 4am
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) +
                           r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-26 " +
                           re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) +
                           r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:([^-]*?)(\s|$)")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('9pm', '3am'), 5])
            possibletimes.append([('11pm', '4am'), 2])
            possibletimes.append([('10pm', 'midnight'), 1])
        #Between 11pm and 3am
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('11pm', '3am'), 1])
        #Between 10pm and 4am
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(
            weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('10pm', '4am'), 4])
        #Between 11pm and 3am
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('11pm', '3am'), 1])
        # Between midnight and 4am
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:([^-]*?)(\s|$)")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('midnight', '4am'), 1])
        # Between 1am and 4am
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(
            weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(
            weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:([^-]*?)(\s|$)")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('1am', '4am'), 9])
        # Between 2am and 4am
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('2am', '4am'), 3])
        # Between 3am and 4am
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('3am', '4am'), 2])
        # Between midnight and 5am
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(
            weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(
            weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:([^-]*?)(\s|$)")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('midnight', '5am'), 1])
        # Between 8am and 11am
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-13 " + re.escape(
            weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('8am', '11am'), 6])
        # Between 10am and 11am
        #Between 8am and noon
        #Between 9am and noon
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:6-13 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:([^-]*?)(\s|$)")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('10am', '11am'), 5])
            possibletimes.append([('8am', 'noon'), 3])
            possibletimes.append([('9am', 'noon'), 125])
        #Between 11am and 1pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:6-13 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('11am', '1pm'), 1])
        #Between 10am and 2pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-13 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('10am', '2pm'), 10])
        #Between 11am and 2pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-13 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('11am', '2pm'), 2])
        #Between noon and 2pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-13 " + re.escape(
            weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('noon', '2pm'), 13])
        #Between 9am and 3pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-13 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:([^-]*?)(\s|$)")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('9am', '3pm'), 1])
        #Between 8am and 4pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:6-13 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('8am', '4pm'), 3])
        #Between 9am and 4pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-13 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(
            weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('9am', '4pm'), 1])
        #Between 10am and 4pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:6-13 " + re.escape(
            weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(
            weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            possibletimes.append([('10am', '4pm'), 6])
    if (weather == 'other') or (len(possibletimes) == 0):
        if re.search(r"Chance.time:17-30 ", dataline):
            possibletimes.append([('8pm', '11pm'), 1])
            possibletimes.append([('9pm', 'midnight'), 21])
            possibletimes.append([('11pm', 'midnight'), 1])
            possibletimes.append([('11pm', '1am'), 4])
            possibletimes.append([('midnight', '1am'), 20])
            possibletimes.append([('1am', '2am'), 7])
            possibletimes.append([('midnight', '3am'), 5])
            possibletimes.append([('1am', '3am'), 2])
            possibletimes.append([('2am', '3am'), 1])
        elif re.search(r"Chance.time:6-21 ", dataline):
            possibletimes.append([('9am', '10am'), 9])
            possibletimes.append([('9am', '11am'), 11])
            possibletimes.append([('11am', 'noon'), 8])
            possibletimes.append([('9am', '1pm'), 1])
            possibletimes.append([('10am', '1pm'), 17])
            possibletimes.append([('noon', '1pm'), 10])
            possibletimes.append([('1pm', '2pm'), 12])
            possibletimes.append([('11am', '3pm'), 1])
            possibletimes.append([('noon', '3pm'), 19])
            possibletimes.append([('1pm', '3pm'), 6])
            possibletimes.append([('2pm', '3pm'), 12])
            possibletimes.append([('11am', '4pm'), 19])
            possibletimes.append([('noon', '4pm'), 222])
            possibletimes.append([('2pm', '4pm'), 3])
            possibletimes.append([('3pm', '4pm'), 1])

    # Normalize the probabilities
    elems = [i[0] for i in possibletimes]
    probs = [i[1] for i in possibletimes]
    norm = [float(i) / sum(probs) for i in probs]

    # And make a random weighted choice
    datachoiceidx = list(choice(len(elems), 1, p=norm))[0]
    datachoice = elems[datachoiceidx]
    return datachoice