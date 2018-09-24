import os
import regex as re
import sys
from numpy.random import choice

datalist = []
filelist = []

def get_file(filepath):
    with open(filepath, 'rb') as f:
        text = f.read()
    text = text.decode('utf-8')
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", ' ', text)
    text = text.strip()
    return text

datapath = 'C:/Users/Chris/Desktop/Prodigy-METEO_pre-alpha/data/inputs'
onlyfiles = [f for f in os.listdir(datapath) if os.path.isfile(os.path.join(datapath, f))]
for file in onlyfiles:
    #Open the datafile, decode and strip from enters
    newdata = get_file(datapath + '/' + file)
    datalist.append(newdata)
    #Add the first part of the filename (until the period) to the filelist
    filelist.append(re.search(r"^(.*?)\.", file).group(1))

textlist = [''] * len(datalist)
textpath = 'C:/Users/Chris/Desktop/Prodigy-METEO_pre-alpha/data/outputs/human-authored'
for (dirpath, dirnames, filenames) in os.walk(textpath):
    # If there are filenames in the folder, access them
    if len(filenames) > 0:
        for filename in filenames:
            #Get the first part (until the period) of the filename
            filenamefind = re.search(r"^(.*?)\.", filename).group(1)
            try:
                #And try to find a match in the data
                index = filelist.index(filenamefind)
            except ValueError:
                continue
            #Get the content from the textfile
            newtext = get_file(dirpath + '/' + filename)
            newtext = newtext.lower()
            #If the aligned textpart of the corresponding data is still empty, put the text in that entry
            if textlist[index] == '':
                textlist[index] = newtext
            #Else, give the datafile and textfile a new line with the aligned data and text
            else:
                datalist.append(datalist[index])
                textlist.append(newtext)

def savefile(listvalue, extension):
    currentpath = os.getcwd()
    liststring = '\n'.join(listvalue)
    with open(currentpath + '/Corpora/All' + extension, 'wb') as f:
        print('Writing new file')
        f.write(bytes(liststring, 'UTF-8'))

savefile(datalist, '.data')
savefile(textlist, '.text')
