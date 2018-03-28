import os.path

sep = os.path.sep

# input path
__dataDir = ".." + sep + "trec06c-utf8"
cutDir = __dataDir + sep + "data_cut"
rawDir = __dataDir + sep + "data"
testDir = __dataDir + sep + "data_test"

labelPath = __dataDir + sep + "label" + sep + "index"
testLabelPath = __dataDir + sep + "label_test" + sep + "index"

# json saved path
dumpDir = ".." + sep + "data"

__dataJsonFileName = "allData.json"
dataJsonPath = dumpDir + sep + __dataJsonFileName

__trainDataFileName = "trainData.json"
trainDataPath = dumpDir + sep + __trainDataFileName

__validDataFileName = "validData.json"
validDataPath = dumpDir + sep + __validDataFileName

__topListFileName_all = "topList_all.json"
topListPath_all = dumpDir + sep + __topListFileName_all

__topListFileName_spam = "topList_spam.json"
topListPath_spam = dumpDir + sep + __topListFileName_spam

__topListFileName_ham = "topList_ham.json"
topListPath_ham = dumpDir + sep + __topListFileName_ham
