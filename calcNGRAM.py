import math

class NGRAM(object):
    def __init__(self, inputFile):
        self.Ngrams = {}
        fileObj = open(inputFile)

        for sents in fileObj:
            word, cnt = sents.split(' ')
            self.Ngrams[word] = int(cnt)

        self.length = len(word)
        self.total = sum(self.Ngrams.values())

        wordLst = self.Ngrams.keys()
        for wrd in wordLst:
            tmp = (float(self.Ngrams[wrd])) / (self.total)
            self.Ngrams[wrd] = math.log10(tmp)

        self.val = math.log10(0.01/self.total)

    def calcScore(self, txt):
        score = 0
        Ngrams = self.Ngrams.__getitem__
        length = len(txt)-self.length + 1

        for n in range(length):
            elm = txt[n:n+self.length]
            score = (score + Ngrams(txt[n:n+self.length])) if elm in self.Ngrams else (score + self.val)

        return score
