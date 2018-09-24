import nltk
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
    score = corpus_bleu(references, candidates)
    return score

def best_file(runnumber, currentpath):
    def grp(pat, txt):
        r = re.search(pat, txt)
        if r:
            digit = int(re.search(r'\d+' , r.group(0)).group(0))
        return digit if r else '&'

    if runnumber == 'Test':
        mypath = currentpath + '/Corpora/NMT_Files/UnfilledRun'
    else:
        mypath = currentpath + '/Corpora/NMT_Files/Run' + str(runnumber)
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

    # Sort the files by epoch (the number after _e)
    if '.DS_Store' in onlyfiles:
        onlyfiles.remove('.DS_Store')
    if 'Sumtime.train.1.pt' in onlyfiles:
        onlyfiles.remove('Sumtime.train.1.pt')
    if 'Sumtime.valid.1.pt' in onlyfiles:
        onlyfiles.remove('Sumtime.valid.1.pt')
    if 'Sumtime.vocab.pt' in onlyfiles:
        onlyfiles.remove('Sumtime.vocab.pt')
    if 'pred.txt' in onlyfiles:
        onlyfiles.remove('pred.txt')
    onlyfiles.sort(key=lambda l: grp("_e\d+\.", l))

    lowestfile = ''

    for file in onlyfiles:
        perplexity = float(re.search(r"ppl_(.*?)_", file).group(1))
        if lowestfile == '':
            lowestfile = (file, perplexity)
        elif perplexity < lowestfile[1]:
            lowestfile = (file, perplexity)

    return mypath + '/' + lowestfile[0]

def return_bleu(runnumber, layersnum, rnn_sizenum, word_vec_sizenum, dropoutnum, learning_ratenum, learning_rate_decaynum, batch_sizenum, beamsizenum):
    currentpath = os.getcwd()
    #Generate the right format of the preprocessing (this one is pretty optional)
    if not os.path.isfile(currentpath + '/Corpora/NMT_Files/Run' + str(runnumber) + '/Sumtime.vocab.pt'):
        preprocessing_command = 'python3 "' + os.path.dirname(os.path.dirname(currentpath)) + '/OpenNMT-py-master/preprocess.py" -train_src "' + currentpath + '/Corpora/Train.data" -train_tgt "' + currentpath + '/Corpora/Train.text" -valid_src "' + currentpath + '/Corpora/Dev.data" -valid_tgt "' + currentpath + '/Corpora/Dev.text" -save_data "' + currentpath + '/Corpora/NMT_Files/Run' + str(runnumber) + '/Sumtime"'
        os.system(preprocessing_command)

    #Train the data
    training_command = 'python3 "' + os.path.dirname(os.path.dirname(currentpath)) + '/OpenNMT-py-master/train.py" -data "' + currentpath + '/Corpora/NMT_Files/Run' + str(runnumber) + '/Sumtime" -save_model "' + currentpath + '/Corpora/NMT_Files/Run' + str(runnumber) + '/Sumtime-model" -layers ' + str(layersnum) + ' -rnn_size ' + str(rnn_sizenum) + ' -src_word_vec_size ' + str(word_vec_sizenum) + ' -tgt_word_vec_size ' + str(word_vec_sizenum) + ' -dropout ' + str(dropoutnum) + ' -learning_rate ' + str(learning_ratenum) + ' -learning_rate_decay ' + str(learning_rate_decaynum)  + ' -batch_size ' + str(batch_sizenum) + ' -epochs 20' + ' -gpuid 1'
    os.system(training_command)

    #Get the best epoch
    model = best_file(runnumber, currentpath)
    #Translate files based on the epoch
    translate_command = 'python3 "' + os.path.dirname(os.path.dirname(currentpath)) + '/OpenNMT-py-master/translate.py" -model "' + model + '" -src "' + currentpath + '/Corpora/Test.data" -output "' + currentpath + '/Corpora/NMT_Files/Run' + str(runnumber) + '/pred.txt" -replace_unk -verbose -beam_size ' + str(beamsizenum) + ' -gpu 1'
    os.system(translate_command)

    #Get the BLEU score
    warnings.filterwarnings(action='ignore', category=UserWarning)
    bleu = bleu_score(currentpath + "/Corpora/Test.text", currentpath + '/Corpora/NMT_Files/Run' + str(runnumber) + '/pred.txt')
    return bleu

def UnfilledRun():
    currentpath = os.getcwd()
    #Generate the right format of the preprocessing (this one is pretty optional)
    if not os.path.exists(currentpath + '/Corpora/NMT_Files/UnfilledRun/'):
        os.makedirs(currentpath + '/Corpora/NMT_Files/UnfilledRun/')
    if not os.path.isfile(currentpath + '/Corpora/NMT_Files/UnfilledRun/Sumtime.vocab.pt'):
        preprocessing_command = 'python3 "' + os.path.dirname(os.path.dirname(currentpath)) + '/OpenNMT-py-master/preprocess.py" -train_src "' + currentpath + '/Corpora/Train_gaps.data" -train_tgt "' + currentpath + '/Corpora/Train_gaps.text" -valid_src "' + currentpath + '/Corpora/Dev_gaps.data" -valid_tgt "' + currentpath + '/Corpora/Dev_gaps.text" -save_data "' + currentpath + '/Corpora/NMT_Files/UnfilledRun/Sumtime"'
        os.system(preprocessing_command)
        #os.system('python "/Users/Chris/Google Drive/Promotie/Automated_Template_Generation/OpenNMT-py-master/preprocess.py" -train_src "/Users/Chris/Google Drive/Promotie/Automated_Template_Generation/Sumtime/Corpora/Train_gaps.data" -train_tgt "/Users/Chris/Google Drive/Promotie/Automated_Template_Generation/Sumtime/Corpora/Train_gaps.text" -valid_src "/Users/Chris/Google Drive/Promotie/Automated_Template_Generation/Sumtime/Corpora/Dev_gaps.data" -valid_tgt "/Users/Chris/Google Drive/Promotie/Automated_Template_Generation/Sumtime/Corpora/Dev_gaps.text" -save_data "/Users/Chris/Google Drive/Promotie/Automated_Template_Generation/Sumtime/Corpora/NMT_Files/Sumtime"')

    #Train the data
    training_command = 'python3 "' + os.path.dirname(os.path.dirname(currentpath)) + '/OpenNMT-py-master/train.py" -data "' + currentpath + '/Corpora/NMT_Files/UnfilledRun/Sumtime" -save_model "' + currentpath + '/Corpora/NMT_Files/UnfilledRun/Sumtime-model" -layers 1 -rnn_size 1170 -src_word_vec_size 860 -tgt_word_vec_size 860 -dropout 0.238831369844743 -learning_rate 0.595668890305279 -learning_rate_decay 0.489211293789462 -batch_size 47 -epochs 20 -gpuid 1'
    os.system(training_command)
    #os.system('python "/Users/Chris/Google Drive/Promotie/Automated_Template_Generation/OpenNMT-py-master/train.py" -data "/Users/Chris/Google Drive/Promotie/Automated_Template_Generation/Sumtime/Corpora/NMT_Files/Sumtime" -save_model "/Users/Chris/Google Drive/Promotie/Automated_Template_Generation/Sumtime/Corpora/NMT_Files/Sumtime-model" -layers 1 -rnn_size 450 -src_word_vec_size 300 -tgt_word_vec_size 300 -dropout 0.3 -lambda_coverage 1 -learning_rate 1.0 -learning_rate_decay 0.5 -epochs 20')

    #Get the best epoch
    model = best_file('Test', currentpath)
    #Translate files based on the epoch
    translate_command = 'python3 "' + os.path.dirname(os.path.dirname(currentpath)) + '/OpenNMT-py-master/translate.py" -model "' + model + '" -src "' + currentpath + '/Corpora/Test_gaps.data" -output "' + currentpath + '/Corpora/NMT_Files/UnfilledRun/pred.txt" -replace_unk -verbose -beam_size 15 -gpu 1'
    os.system(translate_command)

    #Get the BLEU score
    warnings.filterwarnings(action='ignore', category=UserWarning)
    bleu = bleu_score(currentpath + "/Corpora/Test_gaps.text", currentpath + '/Corpora/NMT_Files/UnfilledRun/pred.txt')
    return bleu

UnfilledRun()