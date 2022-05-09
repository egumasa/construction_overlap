#!c:/Python/python.exe -u
# This requires python 3.0+
import collections
from IRSystemHelper import IRSystemHelper


class IRSystemSimple:
    def __init__(self, docsAsStrings, trigrams=False):
        self.doIdf = True
        self.docs = {}
        self.idf = collections.defaultdict(lambda: 0.0)  # for caching
        self.irsystem_helper = IRSystemHelper()
        for docid in docsAsStrings:
            if trigrams:
                self.docs[docid] = self.irsystem_helper.getFreqDictTrigrams(docsAsStrings[docid])
            else:
                self.docs[docid] = self.irsystem_helper.getFreqDict(docsAsStrings[docid])

    def GetTokenFreqDict(self, filePath):
        return self.docs[filePath]

    def JaccardSimilarity(self, filePath1, filePath2):
        return self.irsystem_helper.JaccardSimilarityFromTokens(set(self.GetTokenFreqDict(filePath1).keys()),
                                                set(self.GetTokenFreqDict(filePath2).keys()))

    def GetTfVector(self, tokenFreqDict):
        """
        Returns a unit vector
        :param tokenFreqDict:
        :return:
        """
        return self.irsystem_helper.getTfIdfVector(self.doIdf, self.getIdf, tokenFreqDict)

    def getIdf(self, token):
        return self.irsystem_helper.getIdf(token, self.docs, self.idf)

    def CosineSimilarityFromTokenFreqDict(self, tokenFreqDict1, tokenFreqDict2):
        v1 = self.GetTfVector(tokenFreqDict1)
        v2 = self.GetTfVector(tokenFreqDict2)
        return self.irsystem_helper.DotProduct(v1, v2)

    def CosineSimilarity(self, filePath1, filePath2):
        return self.CosineSimilarityFromTokenFreqDict(self.GetTokenFreqDict(filePath1),
                                                      self.GetTokenFreqDict(filePath2))

