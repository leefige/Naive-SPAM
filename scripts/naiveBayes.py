import math

# Naive Bayes Classifier
class NaiveBayes:
    # init
    def __init__(self, spamCnt, hamCnt, wordList_all=None, wordList_spam=None, wordList_ham=None, ip_spam=None, ip_ham=None, ip_size=0, smooth=1.0, addition=False):
        # setup flag
        self.__initialized = False

        # constant
        self.__outputLabel = ["spam", "ham"]
        self.__laplaceFac = smooth
        self.__topThreshold = 1

        # backup
        self.__wordList_all = wordList_all
        self.__wordList_spam = wordList_spam
        self.__wordList_ham = wordList_ham
        self.__cnt_spam = spamCnt
        self.__cnt_ham = hamCnt
        self.__addition = addition

        self.__ip_spam = ip_spam
        self.__ip_ham = ip_ham

        # core values
        self.__vocabularySize = 0
        self.__ipPoolSize = ip_size
        self.__total_spam = 0
        self.__total_ham = 0

        self.__prob_spam = 0.0
        self.__prob_ham = 0.0

        self.__wordProb_spam = dict()
        self.__wordProb_ham = dict()
        return
    
    # setup core values
    def setup(self):
        print("\nSetting up Naive Bayes classifier...")
        self.__initialized = True

        # calc feature count
        self.__vocabularySize = len(self.__wordList_all)

        self.__wordProb_spam.update(self.__convertArrayToDict(self.__wordList_spam))
        self.__wordProb_ham.update(self.__convertArrayToDict(self.__wordList_ham))

        spamCnt = 0
        for word in self.__wordProb_spam.keys():
            spamCnt += self.__wordProb_spam[word]
        hamCnt = 0
        for word in self.__wordProb_ham.keys():
            hamCnt += self.__wordProb_ham[word]

        self.__total_spam = spamCnt
        self.__total_ham = hamCnt

        # calc P(y_k)
        totalMailCnt = self.__cnt_spam + self.__cnt_ham
        self.__prob_spam = math.log(float(self.__cnt_spam) / float(totalMailCnt))
        self.__prob_ham = math.log(float(self.__cnt_ham) / float(totalMailCnt))

        print("vocabulary size: %d" % self.__vocabularySize)
        print("feature cnt: spam %d, ham %d" % (spamCnt, hamCnt))
        print("type prob: spam %f, ham %f" % (self.__prob_spam, self.__prob_ham))
        print("Setup finished!\n")
        return

    # inspect email
    def inspectEmail(self, email, display=False):
        # setup
        if not self.__initialized:
            self.setup()
        
        words = email['info']['words']
        ip = email['info']['ip']

        score = [self.__prob_spam, self.__prob_ham]

        if self.__addition:
            # add ip
            score[0] += self.__calcIPProb_spam(ip)
            score[1] += self.__calcIPProb_ham(ip)
        
        # calc score for each word
        for word in words:
            score[0] += self.__calcProb_spam(word)
            score[1] += self.__calcProb_ham(word)

        res = self.__outputLabel[0] if score[0] >= score[1] else self.__outputLabel[1]

        if display:
            print(res, score)
        return res

    # [[]] -> {}
    def __convertArrayToDict(self, wordList):
        return dict(wordList)

    # assume list is ordered
    def __getTopCnt(self, wordList, threshold):
        cnt = 0
        for item in wordList:
            if item['cnt'] <= threshold:
                break
            cnt += 1
        return cnt

    def __calcProb_spam(self, word):
        cnt = self.__wordProb_spam[word] if word in self.__wordProb_spam.keys() else 0
        return math.log((cnt + self.__laplaceFac) / (self.__total_spam + self.__laplaceFac * self.__vocabularySize))
    
    def __calcProb_ham(self, word):
        cnt = self.__wordProb_ham[word] if word in self.__wordProb_ham.keys() else 0
        return math.log((cnt + self.__laplaceFac) / (self.__total_ham + self.__laplaceFac * self.__vocabularySize))
    
    def __calcIPProb_spam(self, ip):
        cnt = self.__ip_spam[ip] if ip in self.__ip_spam.keys() else 0
        return math.log((cnt + self.__laplaceFac) / (self.__cnt_spam + self.__laplaceFac * self.__ipPoolSize))
    
    def __calcIPProb_ham(self, ip):
        cnt = self.__ip_ham[ip] if ip in self.__ip_ham.keys() else 0
        return math.log((cnt + self.__laplaceFac) / (self.__cnt_ham + self.__laplaceFac * self.__ipPoolSize))
