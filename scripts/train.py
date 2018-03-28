from defs import *
from parseData import *

# assume list is ordered
def getTopCnt(wordArray, threshold):
    cnt = 0
    for item in wordArray:
        if item[-1] <= threshold:
            break
        cnt = cnt + 1
    return cnt