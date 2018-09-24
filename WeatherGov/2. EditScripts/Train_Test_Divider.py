from sklearn.model_selection import train_test_split
import re

with open('Corpora/sportscasting/all.events') as f:
    events = f.readlines()

with open('Corpora/sportscasting/all.text') as f:
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

with open('Corpora/sportscasting/Train.data', 'wb') as f:
    f.write(bytes(data_train_text, 'UTF-8'))

with open('Corpora/sportscasting/Train.text', 'wb') as f:
    f.write(bytes(text_train_text, 'UTF-8'))

with open('Corpora/sportscasting/Dev.data', 'wb') as f:
    f.write(bytes(data_dev_text, 'UTF-8'))

with open('Corpora/sportscasting/Dev.text', 'wb') as f:
    f.write(bytes(text_dev_text, 'UTF-8'))

with open('Corpora/sportscasting/Test.data', 'wb') as f:
    f.write(bytes(data_test_text, 'UTF-8'))

with open('Corpora/sportscasting/Test.text', 'wb') as f:
    f.write(bytes(text_test_text, 'UTF-8'))