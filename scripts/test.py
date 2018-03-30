from parseData import *

def testParse():

    list_all, list_spam, list_ham = loadTopWordLists()

    print(list_all[:20])
    print(list_spam[:20])
    print(list_ham[:20])

    allData = loadAllData()
    print(len(allData))
    # print(allData)

def testLoad():
    train = loadDataSet("train")
    print(train[0])

    valid = loadDataSet("valid")
    print(valid[0])


# def testList():
#     list_all, list_spam, list_ham = loadTopWordLists()
#     cnt_all = getTopCnt(list_all, 1)
#     print(list_all[0])
#     print(list_all[cnt_all - 1])

#     cnt_spam = getTopCnt(list_spam, 1)
#     print(list_spam[0])
#     print(list_spam[cnt_spam - 1])

#     cnt_ham = getTopCnt(list_ham, 1)
#     print(list_ham[0])
#     print(list_ham[cnt_ham - 1])

# def testTrain():
    # lt, lv = getDataSet()
    # print(lt[80])
    # print(lv[10])

def transList():
    list_all, list_spam, list_ham = loadTopWordLists()

    list_all = convertObjListToArray(list_all)
    list_spam = convertObjListToArray(list_spam)
    list_ham = convertObjListToArray(list_ham)
    

    with open(topListPath_all, mode='w', encoding='utf-8') as fout:
            jsonData = json.dumps(list_all, ensure_ascii=False)
            fout.write(jsonData)
        
    with open(topListPath_spam, mode='w', encoding='utf-8') as fout:
        jsonData = json.dumps(list_spam, ensure_ascii=False)
        fout.write(jsonData)
    
    with open(topListPath_ham, mode='w', encoding='utf-8') as fout:
        jsonData = json.dumps(list_ham, ensure_ascii=False)
        fout.write(jsonData)
    
testLoad()