import unittest
import numpy as np
from IRSystemHelper import IRSystemHelper
from IRSystemSimple import IRSystemSimple


class TestSimple(unittest.TestCase):
    def setUp(self):
        self.docsContents = {"file1": "the the white car", "file2": "the white white dog", "file3": "the black dog",
                             "file4": "the white car"}
        self.ir = IRSystemSimple(self.docsContents)
        self.ir_helper = IRSystemHelper()
        self.irTrigrams = IRSystemSimple(self.docsContents, trigrams=True)
        self.docs = {}
        for docid in self.docsContents:
            self.docs[docid] = self.ir_helper.getFreqDict(self.docsContents[docid])
        self.docsTrigrams = {}
        for docid in self.docsContents:
            self.docsTrigrams[docid] = self.ir_helper.getFreqDictTrigrams(self.docsContents[docid])

    def testJaccardSimilarityFromTokens(self):
        docs = self.docs
        file1_set = set(docs["file1"].keys())
        file2_set = set(docs["file2"].keys())
        file4_set = set(docs["file4"].keys())
        np.testing.assert_almost_equal(self.ir_helper.JaccardSimilarityFromTokens(file1_set, file2_set), 2.0 / 4.0, 4)
        np.testing.assert_almost_equal(self.ir_helper.JaccardSimilarityFromTokens(file1_set, file1_set), 1.0, 4)
        np.testing.assert_almost_equal(self.ir_helper.JaccardSimilarityFromTokens(file1_set, file4_set), 1.0, 4)

    def testJaccardSimilarityFromTrigrams(self):
        docs = self.docsTrigrams
        file1_set = set(docs["file1"].keys())
        file2_set = set(docs["file2"].keys())
        file4_set = set(docs["file4"].keys())
        np.testing.assert_almost_equal(self.ir_helper.JaccardSimilarityFromTokens(file1_set, file2_set), 0.0, 4)
        np.testing.assert_almost_equal(self.ir_helper.JaccardSimilarityFromTokens(file1_set, file1_set), 1.0, 4)
        np.testing.assert_almost_equal(self.ir_helper.JaccardSimilarityFromTokens(file1_set, file4_set), 0.5, 4)

    def testCosineSimilarityFromTokenFreqDict(self):
        docs = self.docs
        np.testing.assert_almost_equal(self.ir.CosineSimilarityFromTokenFreqDict(docs["file1"], docs["file1"]), 1.0, 4)
        np.testing.assert_almost_equal(self.ir.CosineSimilarityFromTokenFreqDict(docs["file1"], docs["file2"]), 0.24483609296025027, 4)
        np.testing.assert_almost_equal(self.ir.CosineSimilarityFromTokenFreqDict(docs["file2"], docs["file3"]), 0.3441097854253426, 4)
        np.testing.assert_almost_equal(self.ir.CosineSimilarityFromTokenFreqDict(docs["file1"], docs["file4"]), 1.0, 4)

    def testCosineSimilarityFromTrigramFreqDict(self):
        docs = self.docsTrigrams
        np.testing.assert_almost_equal(self.irTrigrams.CosineSimilarityFromTokenFreqDict(docs["file1"], docs["file1"]), 1.0, 4)
        np.testing.assert_almost_equal(self.irTrigrams.CosineSimilarityFromTokenFreqDict(docs["file1"], docs["file2"]), 0.0, 4)
        np.testing.assert_almost_equal(self.irTrigrams.CosineSimilarityFromTokenFreqDict(docs["file2"], docs["file3"]), 0.0, 4)
        np.testing.assert_almost_equal(self.irTrigrams.CosineSimilarityFromTokenFreqDict(docs["file1"], docs["file4"]), 0.4472135954999579, 4)

    # Helper methods to get tokens and trigrams. #####################

    def assertFloatEqual(self, v1, v2):
        tol = 0.0001
        self.assertTrue(abs(v1 - v2) < tol)

    def testGetTokens(self):
        self.assertEqual(["the", "white", ",", "white", "dog", "."], self.ir_helper.getTokens(" the  white,  white dog."))
        self.assertEqual(['Hi', 'How', 'are', 'you', '?', 'i', 'am', 'fine', 'and', 'you'],
                         self.ir_helper.getTokens("Hi How are you? i am fine and you"))

    def testGetTrigrams(self):
        self.assertEqual([("the", "white", ","), ("white", ",", "white"), (",", "white", "dog"), ("white", "dog", ".")],
                         self.ir_helper.getTrigrams(" the  white,  white dog."))
        self.assertEqual([('Hi', 'How', 'are'), ('How', 'are', 'you'), ('are', 'you', '?'), ('you', '?', 'i'),
                          ('?', 'i', 'am'), ('i', 'am', 'fine'), ('am', 'fine', 'and'), ('fine', 'and', 'you')],
                         self.ir_helper.getTrigrams("Hi How are you? i am fine and you"))


if __name__ == '__main__':
    unittest.main()