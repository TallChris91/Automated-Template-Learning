from sklearn.model_selection import train_test_split
import re
import os

currentpath = os.getcwd()
with open(currentpath + '/Corpora/Goals_gaps.data', 'rb') as f:
    goalevents = f.readlines()
goalevents = [x.decode('utf-8') for x in goalevents]

with open(currentpath + '/Corpora/Goals_gaps.text', 'rb') as f:
    goaltext = f.readlines()
goaltext = [x.decode('utf-8') for x in goaltext]

with open(currentpath + '/Corpora/Cards_gaps.data', 'rb') as f:
    cardevents = f.readlines()
cardevents = [x.decode('utf-8') for x in cardevents]

with open(currentpath + '/Corpora/Cards_gaps.text', 'rb') as f:
    cardtext = f.readlines()
cardtext = [x.decode('utf-8') for x in cardtext]

events = goalevents + cardevents
text = goaltext + cardtext

eventsstring = '\n'.join(events)
textstring = '\n'.join(text)

with open(currentpath + '/Corpora/All2_gaps.data', 'wb') as f:
    f.write(bytes(eventsstring, 'UTF-8'))

with open(currentpath + '/Corpora/All2_gaps.text', 'wb') as f:
    f.write(bytes(textstring, 'UTF-8'))

num = len(events)-1
while num >= 0:
    text[num] = re.sub('\n', '', text[num])
    events[num] = re.sub('\n', '', events[num])
    if events[num] == '':
        del events[num]
        del text[num]
    if text[num] == '':
        del events[num]
        del text[num]
    num -= 1

data_train, data_test, text_train, text_test = train_test_split(events, text, test_size=0.2, random_state=42)
data_dev, data_test, text_dev, text_test = train_test_split(data_test, text_test, test_size=0.5, random_state=42)

data_train_text = '\n'.join(data_train)
text_train_text = '\n'.join(text_train)
data_dev_text = '\n'.join(data_dev)
text_dev_text = '\n'.join(text_dev)
data_test_text = '\n'.join(data_test)
text_test_text = '\n'.join(text_test)

with open(currentpath + '/Corpora/Train_gaps.data', 'wb') as f:
    f.write(bytes(data_train_text, 'UTF-8'))

with open(currentpath + '/Corpora/Train_gaps.text', 'wb') as f:
    f.write(bytes(text_train_text, 'UTF-8'))

with open(currentpath + '/Corpora/Dev_gaps.data', 'wb') as f:
    f.write(bytes(data_dev_text, 'UTF-8'))

with open(currentpath + '/Corpora/Dev_gaps.text', 'wb') as f:
    f.write(bytes(text_dev_text, 'UTF-8'))

with open(currentpath + '/Corpora/Test_gaps.data', 'wb') as f:
    f.write(bytes(data_test_text, 'UTF-8'))

with open(currentpath + '/Corpora/Test_gaps.text', 'wb') as f:
    f.write(bytes(text_test_text, 'UTF-8'))