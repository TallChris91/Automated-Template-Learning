import os
import regex as re

currentpath = os.getcwd()

def delexicalizer(file):
    with open(currentpath + '/Corpora/weather_new/' + file, 'rb') as f:
        text = f.readlines()

    text = [t.decode('utf-8') for t in text]
    for idx, val in enumerate(text):
        #Replace percentages ("a 30 percent chance")
        text[idx] = re.sub(r"a\s\d{1,3}\spercent\schance", "a <percentage> percent chance", text[idx])
        #Replace the terms mostly_clear/sunny, mostly_sunny/partly_cloudy, mostly_cloudy/partly sunny, cloudy
        text[idx] = re.sub(r"((\bmostly clear\b)|(\bsunny\b)|(\bmostly sunny\b)|(\bpartly cloudy\b)|(\bmostly cloudy\b)|(\bpartly sunny\b)|(\bcloudy\b)|(\bincreasing clouds\b)|(\bclear\b)|(\bclearing\b))", "<cloud_data>", text[idx])
        text[idx] = re.sub(r"((\bgradual\b)|(\bgradually becoming\b))", "<gradual/gradually_becoming>", text[idx])
        #Replace the numbers after high and low
        text[idx] = re.sub(r"(((high near)|(low)|(temperature)|(to around)|(to near))\s([a-zA-Z]+\s)?)[-]?\d+", r"\g<1><temperature>", text[idx])
        text[idx] = re.sub(r"((\bhigh near\b)|(\blow around\b)|(\bsteady temperature (around)?\b))", r"<high_near_low_around_steady_temperature>", text[idx])
        text[idx] = re.sub(r"(\bfalling\b)|(\brising\b)", "<falling/rising>", text[idx])
        text[idx] = re.sub(r"(\bday\b)|(\bnight\b)", "<day/night>", text[idx])

        #Replace the times (times are always structured like "before/after 1am/noon/2pm" or "between 9am and noon")
        text[idx] = re.sub(r"((\bbefore\b)|(\bafter\b)|(\bby\b))\s(\b([1-9][01]?((am)|(pm))\b)|(\bnoon\b)|(\bafternoon\b)|(\bmidnight\b))", '<before_after_by> <time>', text[idx])
        text[idx] = re.sub(r"between (([1-9][01]?((am)|(pm)))|(noon)|(afternoon)|(midnight)) and (([1-9][01]?((am)|(pm)))|(noon)|(afternoon)|(midnight))", 'between <time1> and <time2>', text[idx])

        #Look at the weather type and the chances (they are often combined) FOG! (o.a. line 8681)
        text[idx] = re.sub(r"((a (slight )?chance of )|(possibly ))?(light )?((\bfreezing drizzle\b)|(\bdrizzle\b)|(\bsprinkles\b)|(\bfreezing rain\b)|(\b((scattered )|(isolated ))?((rain )|(snow ))?showers\b)|(\b(scattered )?rain\b)|(\b(scattered )?thunderstorms\b)|(\ba thunderstorm\b)|(\b(scattered )?snow\b)|(\b(scattered )?flurries\b)|(\bsleet\b)|(\bareas of fog\b)|(\bpatchy fog\b)|(\bpatchy freezing fog\b)|(\bareas of freezing fog\b)|(\bfreezing fog\b)|(\bareas of frost\b)|(\bareas of blowing dust\b))( likely)?", '<weather_type_and_chance>', text[idx])
        #Look at the frequency of the weather occuring ("periods of" or "occasional")
        text[idx] = re.sub(r"((periods of)|(occasional))", "<frequency>", text[idx])

        #Sometimes they vary things up a bit and report on the wind
        text[idx] = re.sub(r"((\bn\b)|(\bne\b)|(\be\b)|(\bse\b)|(\bs\b)|(\bsw\b)|(\bw\b)|(\bnw\b)|(\bnne\b)|(\bene\b)|(\bese\b)|(\bsse\b)|(\bssw\b)|(\bwsw\b)|(\bwnw\b)|(\bnnw\b)|(\bcalm\b)|(\blight\b))", '<wind_direction>', text[idx])
        text[idx] = re.sub(r"((between )|(around ))?\d+(\s[a-zA-Z]+\s\d+)?\skt", "<wind_speed>", text[idx])
    return text

filelist = ['Train', 'Test', 'Dev', 'All']
for file in filelist:
    text = delexicalizer(file + '.text')

    text = ''.join(text)
    with open('Corpora/weather_new/' + file + '_new.text', 'wb') as f:
        f.write(bytes(text, 'UTF-8'))

