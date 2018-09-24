from sklearn.model_selection import train_test_split
import re
import os

currentpath = os.getcwd()
with open(currentpath + '/Corpora/All_gaps.data') as f:
    events = f.readlines()

with open(currentpath + '/Corpora/All_gaps.text') as f:
    text = f.readlines()

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