import os
from nltk.translate.bleu_score import corpus_bleu

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

currentpath = os.getcwd()
bleu = bleu_score(currentpath + "/Corpora/Test.text", currentpath + '/Corpora/Test_gaps_filled_Retrieval.text')
print(bleu)