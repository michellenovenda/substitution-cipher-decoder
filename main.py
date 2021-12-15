import random
import string
import time
from calcNGRAM import NGRAM
from tqdm import *
from datetime import datetime
from datetime import timedelta

ciphertext = input('Please input Ciphertext: ')

mutProbs = 10
alphabets = list(string.ascii_uppercase)
fitness = NGRAM('engQuads.txt')

def generateFreqDict(text):
    freqDict = {}
    for alpha in text:
        if not alpha.isalpha():
            continue
        key = alpha.upper()
        if key in freqDict:
            freqDict[key] += 1
        else:
            freqDict[key] = 1
    return freqDict

def frequencyAnalysis(sentence):
    freqDict = generateFreqDict(sentence)
    print(freqDict)

def delSpace(sentence):
    sentence = sentence.lower()
    alphaList = list(sentence.replace(' ', ''))
    string = ''
    for alpha in alphaList:
        string += alpha
    return string

ciphertext = delSpace(ciphertext)

def randomize():
    randomizedList = list(string.ascii_uppercase)
    random.shuffle(randomizedList)
    return randomizedList[:]

def breakEncryption(sentence, key):
    result = ''
    for alpha in sentence:
        c = alpha.upper()
        idx = alphabets.index(c)
        result += str(key[idx])
    return result

def pickRandom():
    randomList = []
    for num in range(100):
        randomList.append(randomize())
    return randomList

def arrangeList(list1, list2):
    list1Length = random.randint(0, 26)
    out = list1[:list1Length] + list2[list1Length:]
    keyExcluded = []
    keyIncluded = []
    dup = []

    for ch in alphabets:
        if ch not in out:
            keyExcluded.append(ch)

    for ch in out:
        if ch not in keyIncluded:
            keyIncluded.append(ch)
        else:
            dup.append(ch)

    for ch in dup:
        outIdx = out.index(ch)
        exIdx = dup.index(ch)
        out[outIdx] = keyExcluded[exIdx]
        
    return out

def discard(putList, sentence):
    f = []
    cur = []
    for elm in putList:
        fit = fitness.calcScore(breakEncryption(sentence, elm))
        f.append(fit)
    fSorted = sorted(f)
    maxVal = fSorted[len(fSorted)-1]
    fSorted = fSorted[33:]
    for elm in fSorted:
        cur.append(putList[f.index(elm)])
    return [cur, maxVal]

def gen(putList):
    res = []
    for idx in range(33):
        getRes = arrangeList(putList[idx], putList[idx+32])
        res.append(getRes)
    retVal = modifyList(res)
    retVal += putList
    return retVal

def swap(key):
    tmp = key[:]
    n1 = random.randint(0, 25)
    n2 = random.randint(0, 25)
    tmp[n1], tmp[n2] = tmp[n2], tmp[n1]
    return tmp

def modifyList(putList):
    tmpLst = putList[:]
    tmpLen = len(tmpLst)
    for num in range(tmpLen):
        probs = random.randint(0, 100)
        if probs <= mutProbs:
            elm = tmpLst[num]
            tmpLst.remove(elm)
            tmpLst.insert(num, swap(elm))
    return tmpLst

def helper(processText, givenKey):
    text = delSpace(processText)
    loopNo = 0
    noIter = 0
    textTop = None
    fitnessTop = -1000000
    keyTop = None

    firstExec = datetime.now()
    m = 8
    while 1:
        curTime = datetime.now()
        if (curTime) < (firstExec + timedelta(minutes=m)):
            if givenKey == None:
                key = randomize()
            else:
                key = givenKey
            ctr = 0
            while ctr < 1000:
                f1 = fitness.calcScore(breakEncryption(text, key))
                swappedKey = swap(key[:])
                if key == swappedKey:
                    ctr += 1
                f2 = fitness.calcScore(breakEncryption(text, swappedKey))
                if f2 > f1:
                    key = swappedKey[:]
                    if f2 > fitnessTop:
                        fitnessTop = f2
                        textTop = breakEncryption(text, swappedKey)
                        keyTop = swappedKey
                        print("==========CURRENT BEST PLAINTEXT==========")
                        print(textTop.lower())
                        print("==========================================")
                        print('Cur Iteration: ' + str(noIter))
                        print('Cur Fitness:' + str(fitnessTop))

                elif f1 > f2:
                    ctr += 1
                noIter += 1
            loopNo += 1
        else:
            break
    print("\n\n===============FINAL PLAINTEXT===============")
    print(textTop.lower())
    print("===============FINAL PLAINTEXT===============")
    print('\n')
    print("==============MORE DETAILS==============")
    print('TOTAL ITERATION: ' + str(noIter + 1))
    print('FITNESS:' + str(fitnessTop))
    print('FREQUENCY ANALYSIS:')
    frequencyAnalysis(ciphertext)

def solve(sentence):
    maxVal = -10000
    r = pickRandom()
    noIter = 0
    num = 0

    flag = 1
    while flag:
        rem = discard(r, sentence)[0]
        val = discard(r, sentence)[1]
        if val > maxVal:
            maxVal = val
            print((breakEncryption(sentence, sorted(r)[len(r)-1])).lower())
            num = 0
        else:
            num += 1

        r = gen(rem)
        noIter += 1
        if num > 20:
            break
    helper(breakEncryption(sentence, sorted(r)[len(r)-1]), sorted(r)[len(r)-1])

solve(ciphertext)