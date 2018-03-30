from defs import *
from parseData import * 
from naiveBayes import *
import random, sys, getopt, time

class Classifier:

    def __init__(self, trainWeight=0.8, smooth=1.0, addition=False, useTime=False, update=False):
        self.dataLoaded = False
        self.bayes = None
        self.initialize(trainWeight, smooth, addition, useTime, update)
        self.bayes.setup()
        return

    def initialize(self, trainWeight, smooth, addition, useTime, update):
        if not self.dataLoaded:
            print("\nClassifier is loading data...")
            # trainSet = loadDataSet("train")
            # topList_all, topList_spam, topList_ham = loadTopWordLists()

            trainSet, topList_all, topList_spam, topList_ham = getDataSet(trainWeight, update=update)
            
            totalSpam = 0
            totalHam = 0
            
            # ip
            ip_spam = {}
            ip_ham = {}

            for email in trainSet:
                ip = email['info']['ip']
                if email['label'] == "spam":
                    totalSpam += 1
                    if ip not in ip_spam:
                        ip_spam[ip] = 0
                    ip_spam[ip] += 1
                elif email['label'] == "ham":
                    totalHam += 1
                    if ip not in ip_ham:
                        ip_ham[ip] = 0
                    ip_ham[ip] += 1

            ipSet = set(ip_spam)
            ipSet.union(set(ip_ham))
            ipSize = len(ipSet)

            # time (hour)
            time_spam = {}
            time_ham = {}

            for email in trainSet:
                hour = email['info']['hour']
                if email['label'] == "spam":
                    if hour not in time_spam:
                        time_spam[hour] = 0
                    time_spam[hour] += 1
                elif email['label'] == "ham":
                    if hour not in time_ham:
                        time_ham[hour] = 0
                    time_ham[hour] += 1

            timeSet = set(time_spam)
            timeSet.union(set(time_ham))
            timeSize = len(timeSet)

            print("smooth factor: %e" % (smooth))
            print("train set weight: %f" % (trainSetWeight))
            print("email cnt: spam %d, ham %d" % (totalSpam, totalHam))

            self.trainSet = trainSet

            self.bayes = NaiveBayes(spamCnt=totalSpam, hamCnt=totalHam, smooth=smooth,
                wordList_all=topList_all, wordList_ham=topList_ham, wordList_spam=topList_spam,
                ip_spam=ip_spam, ip_ham=ip_ham, ip_size=ipSize, addition=addition,
                time_spam=time_spam, time_ham=time_ham, time_size=timeSize, use_time=useTime)
            
            self.dataLoaded = True
        return

    def inspect(self, dataSet):
        cnt = 0
        acc = 0
        TP = [0, 0]
        FP = [0, 0]
        FN = [0, 0]
        
        outType = {'spam':0, 'ham':1}
        for email in dataSet:
            # print("%d: " % cnt, end=' ')
            res = self.bayes.inspectEmail(email)
            if res == email['label']:
                acc += 1
                TP[outType[res]] += 1
            else:
                FP[outType[res]] += 1
                FN[outType[email['label']]] += 1
            cnt += 1

        print("count: %d, correct: %d, accuracy: %f" % (cnt, acc, float(acc) / float(cnt)))
        precision = [float(TP[0]) / float(TP[0] + FP[0]), float(TP[1]) / float(TP[1] + FP[1])]
        recall = [float(TP[0]) / float(TP[0] + FN[0]), float(TP[1]) / float(TP[1] + FN[1])]
        f1 = [2 * precision[0] * recall[0] / (precision[0] + recall[0]), 2 * precision[1] * recall[1] / (precision[1] + recall[1])]

        print("SPAM: precision: %f, recall: %f, F1: %f" % (precision[0], recall[0], f1[0]))
        print("HAM: precision: %f, recall: %f, F1: %f" % (precision[1], recall[1], f1[1]))
        return
    
    def checkOnTrainSet(self):
        print("Checking on train set...")
        self.inspect(self.trainSet)
        print("Finished!\n")
        return
        

    def validate(self):
        print("Validating...")
        self.validSet = loadDataSet('valid')
        self.inspect(self.validSet)
        print("Finished!\n")
        return
        
if __name__ == '__main__':
    # training config
    trainSetWeight = 0.8
    smooth = 1.0
    addition = False
    useTime = False

    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv,"s:w:it")
    for opt, arg in opts:
        if opt == "-i":
            addition = True
        elif opt == "-t":
            useTime = True
        elif opt == "-s":
            smooth = float(arg)
        elif opt == "-w":
            trainSetWeight = float(arg)

    print("-------------------------------------------")
    print("# time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
    print("# args: train_weight %f, smooth %e, addition" % (trainSetWeight, smooth), addition)
    
    cl = Classifier(trainSetWeight, smooth, addition=addition, useTime=useTime, update=True)
    cl.checkOnTrainSet()
    if trainSetWeight < 1.0:
        cl.validate()
