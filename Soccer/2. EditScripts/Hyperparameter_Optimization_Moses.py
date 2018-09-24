import sys
sys.path.append('/home/cvdlee/.local/lib/python3.5/site-packages')
import os
import warnings
from bayes_opt import BayesianOptimization
import regex as re
import pickle
from Train_Test_and_Score_Moses import return_bleu, final_bleu
import csv

def myround(x, base=5):
    return int(base * round(float(x)/base))

def getbleu(distortion, lm, wordpenalty, phrasepenalty, translationmodel1, translationmodel2, translationmodel3, translationmodel4,  unknownwordpenalty):
    currentpath = os.getcwd()
    if not os.path.exists(currentpath + '/PredictionFiles'):
        os.mkdir(currentpath + '/PredictionFiles')
    currentpath = os.getcwd()
    if not os.path.isfile(currentpath + '/runnumber.p'):
        runnumber = 0
        with open(currentpath + '/runnumber.p', 'wb') as f:
            pickle.dump(runnumber, f)

    with open(currentpath + '/runnumber.p', 'rb') as f:
        runnumber = pickle.load(f)
    runnumber += 1
    with open(currentpath + '/runnumber.p', 'wb') as f:
        pickle.dump(runnumber, f)

    bleu = return_bleu(runnumber, distortion, lm, myround(wordpenalty, base=1), phrasepenalty, translationmodel1, translationmodel2, translationmodel3, translationmodel4, myround(unknownwordpenalty, base=1))

    if not os.path.isfile(currentpath + '/RunScores.csv'):
        print('Writing the first CSV file')
        with open(currentpath + '/RunScores.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';')
            #Legenda first
            csvwriter.writerow(['run', 'distortion', 'lm', 'wordpenalty', 'phrasepenalty', 'translationmodel1', 'translationmodel2', 'translationmodel3', 'translationmodel4', 'unknownwordpenalty', 'bleu'])
            #Then the row with information
            csvwriter.writerow([runnumber, distortion, lm, myround(wordpenalty, base=1), phrasepenalty, translationmodel1, translationmodel2, translationmodel3, translationmodel4, myround(unknownwordpenalty, base=1), bleu])
    else:
        with open(currentpath + '/RunScores.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';')
            csvwriter.writerow([runnumber, distortion, lm, myround(wordpenalty, base=1), phrasepenalty, translationmodel1, translationmodel2, translationmodel3, translationmodel4, myround(unknownwordpenalty, base=1), bleu])
    return bleu

def mosesoptimize():
    getbleu(0.3, 0.5, -1, 0.2, 0.2, 0.2, 0.2, 0.2, 1)
    mosesBO = BayesianOptimization(getbleu, {'distortion': (0.0001, 0.6),
                                       'lm': (0.0001, 0.8),
                                       'wordpenalty': (-3, 3),
                                       'phrasepenalty': (0.0001, 0.6),
                                       'translationmodel1': (0.0001, 0.6),
                                       'translationmodel2': (0.0001, 0.6),
                                       'translationmodel3': (0.0001, 0.6),
                                       'translationmodel4': (0.0001, 0.6),
                                       'unknownwordpenalty': (-3, 3)})

    mosesBO.maximize(init_points=15, n_iter=15)
    return mosesBO.res['max']['max_params']

optdict = mosesoptimize()
currentpath = os.getcwd()
with open(currentpath + '/OptdictParams.p', 'wb') as f:
    print('Saving the optimal parameters')
    pickle.dump(optdict, f)
'''
finalbleu = final_bleu()
with open(currentpath + 'Final_Bleu.txt', 'wb') as f:
    f.write(bytes(finalbleu, 'UTF-8'))
'''