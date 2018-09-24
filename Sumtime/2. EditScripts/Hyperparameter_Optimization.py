import sys
import os
import warnings
from bayes_opt import BayesianOptimization
import regex as re
import pickle
from Train_Test_and_Score import return_bleu
import csv

def myround(x, base=5):
    return int(base * round(float(x)/base))

def getbleu(layersnum, rnn_sizenum, word_vec_sizenum, dropoutnum, learning_ratenum, learning_rate_decaynum, batch_sizenum, beamsizenum):
    currentpath = os.getcwd()
    if not os.path.isfile(currentpath + '/runnumber.p'):
        runnumber = 0
        with open(currentpath + '/runnumber.p', 'wb') as f:
            pickle.dump(runnumber, f)

    with open(currentpath + '/runnumber.p', 'rb') as f:
        runnumber = pickle.load(f)
    runnumber += 1
    if not os.path.exists(currentpath + '/Corpora/NMT_Files/Run' + str(runnumber)):
        os.mkdir(currentpath + '/Corpora/NMT_Files/Run' + str(runnumber))
    with open(currentpath + '/runnumber.p', 'wb') as f:
        pickle.dump(runnumber, f)

    bleu = return_bleu(runnumber, myround(layersnum, base=1), myround(rnn_sizenum, base=10), myround(word_vec_sizenum, base=10), dropoutnum, learning_ratenum, learning_rate_decaynum, myround(batch_sizenum, base=1), myround(beamsizenum, base=1))

    if not os.path.isfile(currentpath + '/RunScores.csv'):
        print('Writing the first CSV file')
        with open(currentpath + '/RunScores.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';')
            #Legenda first
            csvwriter.writerow(['run', 'layers', 'rnn_size', 'word_vec_size', 'dropout', 'learning_rate', 'learning_rate_decay', 'batch_size', 'beamsize', 'bleu'])
            #Then the row with information
            csvwriter.writerow([runnumber, myround(layersnum, base=1), myround(rnn_sizenum, base=10), myround(word_vec_sizenum, base=10), max(dropoutnum, 0), max(min(learning_ratenum, 1), 0), max(min(learning_rate_decaynum, 1), 0), myround(batch_sizenum, base=1), myround(beamsizenum, base=1), bleu])
    else:
        with open(currentpath + '/RunScores.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';')
            csvwriter.writerow([runnumber, myround(layersnum, base=1), myround(rnn_sizenum, base=10), myround(word_vec_sizenum, base=10), max(dropoutnum, 0), max(min(learning_ratenum, 1), 0), max(min(learning_rate_decaynum, 1), 0), myround(batch_sizenum, base=1), myround(beamsizenum, base=1), bleu])
    return bleu

def onmtoptimize():
    onmtBO = BayesianOptimization(getbleu, {'layersnum': (1, 3),
                                       'rnn_sizenum': (300, 1500),
                                       'word_vec_sizenum': (300, 1000),
                                       'dropoutnum': (0.1, 0.6),
                                       'learning_ratenum': (0.4, 1),
                                       'learning_rate_decaynum': (0.4, 0.6),
                                       'batch_sizenum': (32, 128),
                                       'beamsizenum': (5, 15)})

    onmtBO.maximize(init_points=15, n_iter=15)
    return onmtBO.res['max']['max_params']

optdict = onmtoptimize()
currentpath = os.getcwd()
with open(currentpath + '/OptdictParams.p', 'wb') as f:
    print('Saving the optimal parameters')
    pickle.dump(optdict, f)