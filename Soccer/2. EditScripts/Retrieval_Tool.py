import os
from collections import Counter
import random

def cosine_similarity(a, b):
    # count word occurrences
    a_vals = Counter(a)
    b_vals = Counter(b)

    # convert to word-vectors
    words = list(a_vals.keys() | b_vals.keys())
    a_vect = [a_vals.get(word, 0) for word in words]  # [0, 0, 1, 1, 2, 1]
    b_vect = [b_vals.get(word, 0) for word in words]  # [1, 1, 1, 0, 1, 0]

    # find cosine
    len_a = sum(av * av for av in a_vect) ** 0.5  # sqrt(7)
    len_b = sum(bv * bv for bv in b_vect) ** 0.5  # sqrt(4)
    dot = sum(av * bv for av, bv in zip(a_vect, b_vect))  # 3
    cosine = dot / (len_a * len_b)  # 0.5669467
    return cosine

currentpath = os.getcwd()

with open(currentpath + '/Corpora/Train_gaps.data', 'rb') as f:
    traindata = f.readlines()
traindata = [l.decode('utf-8') for l in traindata]

with open(currentpath + '/Corpora/Test_gaps.data', 'rb') as f:
    testdata = f.readlines()
testdata = [l.decode('utf-8') for l in testdata]

with open(currentpath + '/Corpora/Train_gaps.text', 'rb') as f:
    traintext = f.readlines()
traintext = [l.decode('utf-8') for l in traintext]

textmatch = []
for idx, val in enumerate(testdata):
    testline = testdata[idx].split() #Split line into bag of words
    testsimilarity = []
    for trainidx, trainval in enumerate(traindata): #Go over all lines in the traindata
        trainline = traindata[trainidx].split() #Also split these into bag of words
        testsimilarity.append(cosine_similarity(testline, trainline)) #And calculate the cosine similarity score of each testline compared to the trainline
    maxval = max(testsimilarity) #Get the highest score
    indices = [index for index, val in enumerate(testsimilarity) if val == maxval] #And all the indices that have the highest score
    random_index = random.choice(indices) #Randomly choose one of these indices
    textmatch.append(traintext[random_index]) #And find the corresponding text
    if idx % 100 == 0:
        print(idx)

textmatchstring = ''.join(textmatch)

#with open(currentpath + '/Corpora/weather_new/Test_new2_UnoptimizedWeatherGov_Filled.text' + '', 'wb') as f:
with open(currentpath + '/Corpora/Test_Retrieval_Gaps.txt', 'wb') as f:
    f.write(bytes(textmatchstring, 'UTF-8'))