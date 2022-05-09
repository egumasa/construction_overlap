import os, sys, collections, ntpath
from IRSystem import FreqDictReader
__author__ = 'Phil'

class BaseFreqDictReader(FreqDictReader):
    def __init__(self, directoryOfTexts, extension, compare_abc):
        super(BaseFreqDictReader, self).__init__(directoryOfTexts, extension)
        self.compare_abc = compare_abc

    def CompareFiles(self, filesPathsForComparison, simMethod, simMethodName):
        similarities = {}
        for i1, filePath1 in enumerate(filesPathsForComparison):
            if not filePath1.endswith(self.extension):
                continue
            for i2, filePath2 in enumerate(filesPathsForComparison):
                if not filePath2.endswith(self.extension):
                    continue
                if i1 >= i2:
                    continue
                condition1, studentId1, session1, story1, delivery1 = self.ParseFilePath(filePath1)
                condition2, studentId2, session2, story2, delivery2 = self.ParseFilePath(filePath2)
                if(not self.compare_abc):
                    if condition1 != condition2 and studentId1 != studentId2 and session1 != session2 and story1 != story2:
                        raise NameError("these should all be the same.")
                    if delivery1 < delivery2:
                        comparison = str.format("{3}_{0}{1}_{0}{2}", story1, delivery1, delivery2, simMethodName)
                    else:
                        comparison = str.format("{3}_{0}{2}_{0}{1}", story1, delivery1, delivery2, simMethodName)
                else:
                    if condition1 != condition2 and studentId1 != studentId2 and delivery1 != delivery2:
                        raise NameError("these should all be the same.")
                    if(story1 < story2):
                        comparison = str.format("{4}_{0}{1}_{2}{3}", story1, delivery1, story2, delivery2, simMethodName)
                    else:
                        comparison = str.format("{4}_{2}{3}_{0}{1}", story1, delivery1, story2, delivery2, simMethodName)

                if comparison not in similarities:
                    similarities[comparison] = simMethod(filePath1, filePath2)

        return similarities

    def GenerateTokenIntersections(self, filesPathsForComparison, outputDirectory):
        tokensDict = {}
        studentId = ""
        commonTokensDict = {}
        for i1, filePath1 in enumerate(filesPathsForComparison):
            if not filePath1.endswith(self.extension):
                continue
            for i2, filePath2 in enumerate(filesPathsForComparison):
                if not filePath2.endswith(self.extension):
                    continue
                if i1 >= i2:
                    continue

                condition1, studentId1, session1, story1, delivery1 = self.ParseFilePath(filePath1)
                condition2, studentId2, session2, story2, delivery2 = self.ParseFilePath(filePath2)
                studentId = studentId1
                if(filePath1 not in tokensDict.keys()):
                    tokensDict[filePath1] = set(self.ReadFromFile(filePath1).keys())
                if(filePath2 not in tokensDict.keys()):
                    tokensDict[filePath2] = set(self.ReadFromFile(filePath2).keys())
                intersection = tokensDict[filePath1].intersection(tokensDict[filePath2])
                filename = str.format("TokenIntersection_{3}_{0}{1}_{0}{2}.tokens.txt", story1, delivery1, delivery2, studentId)
                with open(os.path.join(outputDirectory, filename), 'w') as outputFile:
                    for token in intersection:
                        outputFile.write(token + "\n")
                if(story1 not in commonTokensDict):
                    commonTokensDict[story1] = tokensDict[filePath1]
                commonTokensDict[story1] = commonTokensDict[story1].intersection(tokensDict[filePath1])
                commonTokensDict[story1] = commonTokensDict[story1].intersection(tokensDict[filePath2])

        for story in commonTokensDict.keys():
            intersection = commonTokensDict[story]
            filename = str.format("TokenIntersection_{0}_{1}_common.tokens.txt", studentId, story)
            if(intersection is None):
                intersection = set([])
            with open(os.path.join(outputDirectory, filename), 'w') as outputFile:
                for token in intersection:
                    outputFile.write(token + "\n")
                if(len(intersection) == 0):
                    outputFile.write("\n")


    def GetFilesGroupedByStudents(self):
        filesGroupedByStudents = {}
        for fileName in os.listdir(self.directoryOfTexts):
            if not fileName.endswith(self.extension):
                continue
            filePath = os.path.join(self.directoryOfTexts,fileName)
            condition, studentId, session, story, delivery = self.ParseFileName(fileName)
            if(self.compare_abc):
                studentKey = str.format("{0}_{1}_{2}", condition, studentId, delivery)
            else:
                studentKey = str.format("{0}_{1}_{2}", condition, studentId, session)
            if studentKey not in filesGroupedByStudents:
                filesGroupedByStudents[studentKey] = []
            filesGroupedByStudents[studentKey].append(filePath)
        return filesGroupedByStudents

    def ParseFilePath(self, filePath):
        fileName = ntpath.basename(filePath)
        return self.ParseFileName(fileName)

    def ParseFileName(self, fileName):
        fileNameAsArray = fileName.split('_')
        condition = fileNameAsArray[0]
        studentId = int(fileNameAsArray[1])
        session = fileNameAsArray[2]
        story = fileNameAsArray[3][0]
        delivery = int(fileNameAsArray[3][1])
        return condition, studentId, session, story, delivery

class TrigramFreqDictReader(BaseFreqDictReader):
    def __init__(self, directoryOfTexts, extension, compare_abc, beginLine=0):
        super(TrigramFreqDictReader,self).__init__(directoryOfTexts, extension, compare_abc)
        self.beginLine = beginLine

    def ReadFromFile(self, filePath):
        trigramsFreqDict = collections.defaultdict(lambda: 0.0)
        if not os.path.exists(filePath):
            raise NameError(str.format("the file '{0}' does not exist", filePath))
        with open(filePath, 'r') as trigramFile:
            for i, line in enumerate(trigramFile):
                if i < self.beginLine or line is None or line.strip() == "":
                    continue
                lineAsArray = line.strip().split()
                if len(lineAsArray) != 4:
                    sys.stderr.write(str.format("trigrams must be of length 3. Occurred at line {0} with text '{1}'", i,line))
                    continue
                trigram = ""
                for j in range(1,4):
                    trigram += lineAsArray[j] + " "
                trigram = trigram.strip()
                trigramsFreqDict[trigram] = int(lineAsArray[0])
            return trigramsFreqDict

class UnigramFreqDictReader(BaseFreqDictReader):
    def __init__(self, directoryOfTexts, extension, compare_abc, beginLine=0):
        super(UnigramFreqDictReader,self).__init__(directoryOfTexts, extension, compare_abc)
        self.beginLine = beginLine

    def ReadFromFile(self, filePath):
        unigramsFreqDict = collections.defaultdict(lambda: 0.0)
        if not os.path.exists(filePath):
            raise NameError(str.format("the file '{0}' does not exist", filePath))
        with open(filePath, 'r') as unigramFile:
            for i, line in enumerate(unigramFile):
                if i < self.beginLine  or line is None or line.strip() == "":
                    continue
                if line.startswith("---"): # this marks the end of the file
                    break
                lineAsArray = line.strip().split()
                if len(lineAsArray) != 2:
                    sys.stderr.write(str.format("Unigrams must be of length 1. Occurred at line {0} with text '{1}'", i,line))
                    continue
                unigram = ""
                for j in range(1,2):
                    unigram += lineAsArray[j] + " "
                unigram = unigram.strip()
                unigramsFreqDict[unigram] = int(lineAsArray[0])
            return unigramsFreqDict
