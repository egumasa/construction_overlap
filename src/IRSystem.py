#!c:/Python/python.exe -u
# This requires python 3.0+
import collections
import os

from IRSystemHelper import IRSystemHelper


class FreqDictReader:
    def __init__(self, directoryOfTexts, extension):
        self.extension = extension
        self.directoryOfTexts = directoryOfTexts

    def ReadFromFile(self, filePath):
        raise NotImplementedError("This method should be implemented by the base class.")


class IRSystem:
    """
    IRSystem takes in its constructor an tokenReader that implements the FreqDictReader interface.
    """
    def __init__(self, tokenReader):
        if tokenReader is None:
            return
        self.doIdf = True
        self.tokenFreqDictReader = tokenReader
        self.idf = collections.defaultdict(lambda: 0.0) # for caching
        self.irsystem_helper = IRSystemHelper()
        if self.doIdf:
            self.BuildDocTokenFreqDict() # builds self.docs
        else:
            self.docs = collections.defaultdict(lambda: None)

    def BuildDocTokenFreqDict(self):
        self.docs = collections.defaultdict(lambda: None)
        for file in os.listdir(self.tokenFreqDictReader.directoryOfTexts):
            if not file.endswith(self.tokenFreqDictReader.extension):
                continue
            filePath = os.path.join(self.tokenFreqDictReader.directoryOfTexts, file)
            self.docs[filePath] = self.GetTokenFreqDict(filePath)

    def GetTokenFreqDict(self, filePath):
        if filePath in self.docs.keys():
            return self.docs[filePath]
        return self.tokenFreqDictReader.ReadFromFile(filePath)

    def JaccardSimilarity(self, filePath1, filePath2):
        return self.irsystem_helper.JaccardSimilarityFromTokens(set(self.GetTokenFreqDict(filePath1).keys()), set(self.GetTokenFreqDict(filePath2).keys()))
    
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

