#import sys, os
#scriptpath = "/home/phil/NelsScripts/TrigramAnalysis/"
#
## Add the directory containing your module to the Python path (wants absolute paths)
#sys.path.append(os.path.basename(scriptpath))

import os
import unittest
from IRSystem import IRSystem
from BaseFreqDictReader import TrigramFreqDictReader


class TestSimilarityAnalysis(unittest.TestCase):
    def setUp(self):
        tgfr = TrigramFreqDictReader("../testdata/", ".txt", False)
        self.ir = IRSystem(tgfr)

    def testSimOutputs(self):
        print(os.getcwd())
        #raise NameError()
        ir = self.ir
        #filesPathsForComparison = ["trigramTest1.txt", "trigramTest1Copy.txt", "trigramTest2.txt", "trigramTest3.txt"]
        tol = 0.0000001
        assert(ir.JaccardSimilarity("../testdata/trigramTest1.txt", "../testdata/trigramTest1Copy.txt") - 1.0 < tol)
        assert(ir.CosineSimilarity("../testdata/trigramTest1.txt", "../testdata/trigramTest1Copy.txt") - 1.0 < tol)
#        assert(ir.JaccardSimilarity("../testdata/trigramTest1.txt", "../testdata/trigramTest2.txt") - 0.16666666666666666 < tol)
#        assert(ir.CosineSimilarity("../testdata/trigramTest1.txt", "../testdata/trigramTest2.txt") - 0.028292495285324692 < tol)
        #was
        assert(ir.JaccardSimilarity("../testdata/trigramTest1.txt", "../testdata/trigramTest2.txt") - 0.2857142857142857 < tol)
        assert(ir.CosineSimilarity("../testdata/trigramTest1.txt", "../testdata/trigramTest2.txt") - 0.0927469237619761 < tol)
        assert(ir.JaccardSimilarity("../testdata/trigramTest1.txt", "../testdata/trigramTest3.txt") < tol)
        assert(ir.CosineSimilarity("../testdata/trigramTest1.txt", "../testdata/trigramTest3.txt") < tol)


if __name__ == '__main__':
    unittest.main()
