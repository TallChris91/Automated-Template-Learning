import nltk
from nltk.translate.bleu_score import corpus_bleu
import os
import regex as re
import warnings

def tune_moses(distortion, lm, wordpenalty, phrasepenalty, translationmodel1, translationmodel2, translationmodel3, translationmodel4,  unknownwordpenalty):
    currentpath = os.getcwd()
    with open(currentpath + '/model/moses.ini', 'rb') as f:
        text = f.readlines()
    text = [x.decode('utf-8') for x in text]
    for lineidx, line in enumerate(text):
        if re.search(r'^Distortion0=', line):
            text[lineidx] = 'Distortion0= ' + str(distortion) + '\n'
        elif re.search(r'^LM0=', line):
            text[lineidx] = 'LM0= ' + str(lm) + '\n'
        elif re.search(r'^WordPenalty0=', line):
            text[lineidx] = 'WordPenalty0= ' + str(wordpenalty) + '\n'
        elif re.search(r'^PhrasePenalty0=', line):
            text[lineidx] = 'PhrasePenalty0= ' + str(phrasepenalty) + '\n'
        elif re.search(r'^TranslationModel0=', line):
            text[lineidx] = 'TranslationModel0= ' + str(translationmodel1) + ' ' + str(translationmodel2) + ' ' + str(translationmodel3) + ' ' + str(translationmodel4) + '\n'
        elif re.search(r'^UnknownWordPenalty0=', line):
            text[lineidx] = 'UnknownWordPenalty0= ' + str(unknownwordpenalty) + '\n'
    text = ''.join(text)
    with open(currentpath + '/model/moses.ini', 'wb') as f:
        f.write(bytes(text, 'UTF-8'))

def bleu_score(file1, file2):
    with open(file1, 'r') as f:
        references = f.readlines()
    with open(file2, 'r') as f:
        candidates = f.readlines()

    references = [x.split() for x in references]
    references = [[x] for x in references]
    candidates = [x.split() for x in candidates]
    score = corpus_bleu(references, candidates)
    return score

def return_bleu(runnumber, distortion, lm, wordpenalty, phrasepenalty, translationmodel1, translationmodel2, translationmodel3, translationmodel4,  unknownwordpenalty):
    currentpath = os.getcwd()
    #Tune the weights of the moses.ini file
    tune_moses(distortion, lm, wordpenalty, phrasepenalty, translationmodel1, translationmodel2, translationmodel3,
               translationmodel4, unknownwordpenalty)

    os.system('/vol/customopt/machine-translation/bin/moses -f ' + currentpath + '/model/moses.ini -i /vol/tensusers/cvdlee/MosesFiles/Corpora/sportscasting/Test_2_new.data > ' + currentpath + '/PredictionFiles/Run' + str(runnumber) + '.txt')



    #Get the BLEU score
    warnings.filterwarnings(action='ignore', category=UserWarning)
    bleu = bleu_score('/vol/tensusers/cvdlee/MosesFiles/Corpora/sportscasting/Test_2_new.text', currentpath + '/PredictionFiles/Run' + str(runnumber) + '.txt')
    return bleu

def final_bleu():
    currentpath = os.getcwd()
    with open(currentpath + '/OptdictParams.p', 'rb') as f:
        print('Loading the optimal parameters')
        optdict = pickle.load(f)

    #Tune the weights of the moses.ini file
    tune_moses(optdict['distortion'], optdict['lm'], optdict['wordpenalty'], optdict['phrasepenalty'], optdict['translationmodel1'], optdict['translationmodel2'], optdict['translationmodel3'],
               optdict['translationmodel4'], optdict['unknownwordpenalty'])

    os.system('/vol/customopt/machine-translation/bin/moses -f ' + currentpath + '/model/moses.ini -i /vol/tensusers/cvdlee/MosesFiles/Corpora/sportscasting/Test.data > ' + currentpath + '/PredictionFiles/Final.txt')

    #Get the BLEU score
    warnings.filterwarnings(action='ignore', category=UserWarning)
    bleu = bleu_score('/vol/tensusers/cvdlee/MosesFiles/Corpora/sportscasting/Test.text', currentpath + '/PredictionFiles/Final.txt')
    return bleu