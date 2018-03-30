from defs import *
import os, random, json, re

# -------------FROM RAW FILE--------------
# STEP 1
# read all index data to a dict
def __readIndex():
    allData = {}
    with open(labelPath, mode='r') as fin:
        for line in fin:
            line = line.strip()
            parts = line.split(" ")
            label = parts[0]

            # parse path
            path = parts[-1]
            paths = path.split("/")
            firstDir = paths[-2]
            secondDir = paths[-1]

            if not (firstDir in allData):
                allData[firstDir] = {}
            if not (secondDir in allData[firstDir]):
                allData[firstDir][secondDir] = {}

            # add label
            allData[firstDir][secondDir]["label"] = label
    
    return allData

# STEP 2
# read all emails after reading index
def __parseEmails():
    allData = __readIndex()

    for firstDir in allData.keys():
        print("Parsing %s..." % firstDir)
        for secondDir in allData[firstDir].keys():
            email = allData[firstDir][secondDir]
            info = __readEmail(cutDir, firstDir, secondDir)
            email['info'] = info
    return allData

# TOP PARSING METHOD
def parseAll(isDump=False, trainWeight=0.8):
    allData = __parseEmails()
    dataList = convertDataToList(allData)
    # split
    trainSet, validSet = __genDataSet(dataList, trainWeight)

    # statistics
    toplist_all, toplist_spam, toplist_ham = __statistics(trainSet)
    
    # dump json data
    if isDump:
        # check dump dir
        if not os.path.exists(dumpDir):
            os.makedirs(dumpDir)

        __dumpJson(allData, dataJsonPath)
        __dumpJson(trainSet, trainDataPath)
        __dumpJson(validSet, validDataPath)

        __dumpJson(toplist_all, topListPath_all)
        __dumpJson(toplist_spam, topListPath_spam)
        __dumpJson(toplist_ham, topListPath_ham)

    return (trainSet, toplist_all, toplist_spam, toplist_ham)

# ---------------LOAD------------------
# load dumped data
def loadDataSet(set_t):
    if set_t == "train":
        return __loadJson(trainDataPath)
    elif set_t == "valid":
        return __loadJson(validDataPath)
    else:
        print("Error: arg 'set_t' should be data set type: one of ['train', 'valid']")
        exit(1)

# load dumped data
def loadAllData():
    print("loading allData from dumped file...")
    allData = __loadJson(dataJsonPath)
    print("Finished!")
    return allData

# load dumped list
def loadTopWordLists():
    topList_all = __loadJson(topListPath_all)
    topList_spam = __loadJson(topListPath_spam)
    topList_ham = __loadJson(topListPath_ham)
    return (topList_all, topList_spam, topList_ham)

# --------------PARSING METHODS------------------

# dump json
def __dumpJson(data, path):
    with open(path, mode='w', encoding='utf-8') as fout:
            jsonData = json.dumps(data, ensure_ascii=False)
            fout.write(jsonData)
    return

# load json
def __loadJson(path):
    with open(path, mode='r', encoding='utf-8') as fin:
        dumped = json.loads(fin.readline(), encoding='utf-8')
    return dumped

# convert data obj to list
def convertDataToList(dataDict):
    allList = []
    valList = dataDict.values()
    for entry in valList:
        allList.extend(entry.values())
    return allList

# read a certain email
# path: root/dirName/fileName
# return a dict of info
def __readEmail(root, dirName, fileName):
    mailPath = root + sep + dirName + sep + fileName
    info = {}
    info['words'] = {}
    with open(mailPath, mode='r', encoding='utf8') as fin:
        contentStart = False
        for line in fin:
            line = line.strip()
            info['hour'] = "null"
            # parse ip
            if re.match(r'Received: from.*', line):
                ipRe = re.search(r'\[.*\]', line, flags=0)
                if ipRe:
                    ip = line[ipRe.start():ipRe.end()].strip("[]")
                    info['ip'] = ip
                else:
                    info['ip'] = ""
            # parse time
            if re.match(r'Date: .*', line):
                if not contentStart:
                    ipRe = re.findall(r'\d+:', line, flags=0)
                    if len(ipRe) > 0:
                        hour = ipRe[0].strip(":")
                        info['hour'] = hour
            # assume that blank line means content starts
            elif re.match(r'^$', line):
                contentStart = True
            elif not contentStart:
                continue
            # parse words in email
            else:
                words = line.split(" ")
                for word in words:
                    if re.match(r'\d+', word):
                        continue
                    if not (word in info['words']):
                        info['words'][word] = 0
                    info['words'][word] = info['words'][word] + 1
    return info

# [[x, y]...] -> [{'x':x, 'y':y}]
def convertDuoListToObjList(li):
    objList = []
    for subli in li:
        obj = {}
        obj["word"] = subli[0]
        obj["cnt"] = subli[-1]
        objList.append(obj)
    return objList

# [[x, y]...] -> [{'x':x, 'y':y}]
def convertObjListToArray(li):
    array = []
    for obj in li:
        array.append([obj["word"], obj["cnt"]])
    return array

# split into train & valid
def __genDataSet(dataList, trainSetWeight):
    # shuffle!!
    random.shuffle(dataList)
    listLen = len(dataList)
    trainLen = int(trainSetWeight * listLen)
    # split
    trainSet = dataList[:trainLen]
    validSet = dataList[trainLen:]
    return (trainSet, validSet)

def __statistics(trainSet):
    # statistics based on train set
    topWords_all = {}
    topWords_spam = {}
    topWords_ham = {}

    for email in trainSet:
        info = email['info']
        label = email['label']
        
        # count words
        for word in info['words']:
            if not word in topWords_all:
                topWords_all[word] = 0
            topWords_all[word] = topWords_all[word] + 1

            # check label
            if label == "spam":
                if not word in topWords_spam:
                    topWords_spam[word] = 0
                topWords_spam[word] = topWords_spam[word] + 1
            elif label == "ham":
                if not word in topWords_ham:
                    topWords_ham[word] = 0
                topWords_ham[word] = topWords_ham[word] + 1
            else:
                print("Warning: invalid label '%s'" % label)

    # sort
    toplist_all = sorted(topWords_all.items(),key = lambda x:x[1],reverse = True)
    toplist_spam = sorted(topWords_spam.items(),key = lambda x:x[1],reverse = True)
    toplist_ham = sorted(topWords_ham.items(),key = lambda x:x[1],reverse = True)

    return (toplist_all, toplist_spam, toplist_ham)

# assume that all data has been dumped
def getDataSet(trainWeight, update=False):
    if update:
        # read all data
        assert(os.path.exists(dataJsonPath))
        allData = loadAllData()
        trainSet, validSet = __genDataSet(convertDataToList(allData), trainWeight)

        toplist_all, toplist_spam, toplist_ham = __statistics(trainSet)
        
        # dump json data
        # check dump dir
        if not os.path.exists(dumpDir):
            os.makedirs(dumpDir)

        __dumpJson(trainSet, trainDataPath)
        __dumpJson(validSet, validDataPath)

        __dumpJson(toplist_all, topListPath_all)
        __dumpJson(toplist_spam, topListPath_spam)
        __dumpJson(toplist_ham, topListPath_ham)

        return (trainSet, toplist_all, toplist_spam, toplist_ham)
    else:
        trainSet = loadDataSet('train')
        toplist_all, toplist_spam, toplist_ham = loadTopWordLists()
        return (trainSet, toplist_all, toplist_spam, toplist_ham)

if __name__ == '__main__':
    parseAll(isDump=True)
