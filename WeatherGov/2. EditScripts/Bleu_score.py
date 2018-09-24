from nltk.translate.bleu_score import corpus_bleu
import os
import regex as re
import warnings

def bleu_score(file1, file2):
    with open(file1, 'r') as f:
        references = f.readlines()
    with open(file2, 'r') as f:
        candidates = f.readlines()

    references = [x.split() for x in references]
    references = [[x] for x in references]
    candidates = [x.split() for x in candidates]
    print(len(references))
    print(len(candidates))
    score = corpus_bleu(references, candidates)
    return score

#Get the BLEU score
currentpath = os.getcwd()
warnings.filterwarnings(action='ignore', category=UserWarning)
bleu = bleu_score(currentpath + "/Corpora/weather_new/Test.text", currentpath + '/Corpora/weather_new/Test_Moses_Gaps_Filled.txt')
print(bleu)