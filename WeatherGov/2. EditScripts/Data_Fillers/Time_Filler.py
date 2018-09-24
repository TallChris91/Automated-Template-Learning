import regex as re

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
            datachoice = 'after 1am'
        #Before 1 am (and rarer cases: before 2 am)
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'before 1am-2am'
        #After 2 am (and after 3 am, after 4 am)
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'after 2am-3am-4am'
        # Before 3 am (and before 4 am)
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'before 3am-4am'
        #After 9 am (and 10 am)
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:6-13 " + re.escape(weather) +  r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'after 9am-10am'
        # Before 9 am (and 10 am)
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-13 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'before 9am-10am'
        # After 11 am/noon/1pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:6-13 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'after 11am-noon-1pm'
        # Before 11 am/noon/1pm/2pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:6-9 "
                           + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-13 " + re.escape(weather)
                           + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:-- "
                           + re.escape(weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'before 11am-noon-1pm-2pm'
        #After 2pm/3pm/4pm/5pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather)
                           + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:6-13 "
                           + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather)
                           + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline   )
        if match:
            matchfound = 'y'
            datachoice = 'after 2pm-3pm-4pm-5pm'
        # Before 3pm/4pm/5pm
        regex = re.compile(re.escape(weather) + r"Chance.time:6-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-9 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:6-13 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:9-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:13-21 " + re.escape(weather) + r"Chance.mode:--\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'before 3pm-4pm'
        #Before 8pm/9pm/10pm
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'before 8pm-9pm-10pm'
        #After 9pm/10pm
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'after 9pm-10pm'
        #After 11pm/midnight
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:([^-]*?)\s")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'after 11pm-midnight'
        # Before 11pm/midnight
        regex = re.compile(re.escape(weather) + r"Chance.time:17-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:17-21 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:17-26 " + re.escape(weather) + r"Chance.mode:([^-]*?) " + re.escape(weather) + r"Chance.time:21-30 " + re.escape(weather) + r"Chance.mode:-- " + re.escape(weather) + r"Chance.time:26-30 " + re.escape(weather) + r"Chance.mode:--")
        match = re.search(regex, dataline)
        if match:
            matchfound = 'y'
            datachoice = 'before 11pm-midnight'

    #If a match is still not found, we will look if this is one of these rare cases where the time is about the temperature
    if matchfound == 'n':
        if (len(previoustemplates) > 1) and (previoustemplates[-1] == '<temperature>'):
            if re.search(r'temperature.time:6-21', dataline):
                datachoice = 'by 9am'
            else:
                datachoice = 'by midnight'

        else:
            # If no specific time is found, let's use the data to determine night and day (which may filter something...
            matchfound = 'y'
            if re.search(r"rainChance.time:17-30", dataline):
                datachoice = 'at night'
            else:
                datachoice = 'at day'
    datachoice = datachoice.split(' ')
    return datachoice