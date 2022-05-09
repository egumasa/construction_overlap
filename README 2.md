# FluencySimilarity

This repo is a copy of [fluencysimilarity by Philip Tillman](https://bitbucket.org/philtillman/fluencysimilarity/src/master/).

This repository contains scripts to compare textual similarity using trigrams and unigram (words) using two metrics 
for similarity: Jaccard Similarity and Cosine Similarity of tf-idf vectors. These measures are used to compare
unigrams and trigrams of words and/or parts of speech tokens. The idea is that we can measure the relative fluency
of a pair of text using these measures.

### How do I get set up? ###
* Install [Anaconda3](https://www.anaconda.com/distribution/#download-section).
* Open a command prompt
* Run `$ cd "C:\Path\to\project"` and replace the path with the correct one.
* Run `$ pip install -r requirements.txt`
* Run `$ SimilarityAnalysis.bat`. This runs the script on some sample data provided in the folder sample_data.
  Which runs the command `$ python "src\SimilarityAnalysis.py" -t trigram -d "sample_data" --begin-line 7 > "result.csv"`
* Running `$ SimilarityAnalysis.bat` will output a file `result.csv` in root of the repository.
* To list options for the scripts use the command `$ python src\SimilarityAnalysis.py --help`

**Notes**

* Dependencies: Uses interpreter version Python 3 (tested on 3.7) and NOT Python 2.x, third party libraries are in 
the requirement.txt file
* How to run unit tests: Install PyCharm IDE and configure paths to resolve dependencies within each project. Once 
this is done you should be able to run the unit tests in PyCharm.

To see help from the command line run the command

`$ python "src\SimilarityAnalysis.py" -h`

## Expected file format
**File name format:** {condition}_{session}_{studentId}_{story}{delivery}_blah_blah.cex

Ex) "NoTP_918_1_a1_10250_checked_AS-mlv_trans.str.fix.fxb.mor.pst_err-jms.chstr.coocr.cex"
`condition = "NoTP", session = 1, sudentId = 918, story = "a", delivery = 1`

Note that the story and delivery must be one character. If you want to change this behavior then
see file `BaseFreqDictReader.py` method `ParseFileName()`

**Contents** The contents of the file should contain lines of the form "    {freq}  {word1} {word2} {word3}"
where freq is the frequency of the trigram and words 1 through 3 are the words in the trigram. For example,
given the text `my_text = "This is my text. This is my new text."` the file would contain the trigrams:

    2  . . this
    2 . this is
    2  this is my
    1  is my text
    1  my text .
    2  text . .
    1  is my new
    1  my new text
    1  new text .

Note that we use the convention tbat the "." means the end and beginning of a sentence.

**How we compare files:** Comparison are made between files with same {condition, studentId, delivery} unless the 
"abc" flag is set in which
the comparisons are made between files with same {condition, studentId, session}.

### Examples

Ex1) Similarity based on trigrams. `$ SimilarityAnalysis.bat`

`$ python "src\SimilarityAnalysis.py" -t trigram -d "sample_data" --begin-line 7 > "result.csv"`

Ex2) Similarity based on words (unigrams). `SimilarityAnalysisUnigram.bat`

`$ python "src\SimilarityAnalysis.py" -t unigram -d "sample_data_unigram" --begin-line 7 > "result_unigram.csv"`

### Documentation of SimilarityAnalysis

To understand how Similarity in SimilarityAnalysis is computed one should start by running and inspecting the unit 
tests in SimpleTests.py. These tests should give a basic understanding of what this core of the code does. The other 
code in this  is mainly for performance and unpacking the data from the form it is in so that we can compute the 
 imilarity (i.e., plumbing)

The raw methods that compute the compute the Jaccard Similarity and Cosine Similarity are in
IRSystemHelper.py. IRSystem.py and IRSystemSimple.py are wrapper classes around methods of this class that adds 
caching for performance and methods to read files from disk. If you want to understand how these basic methods 
can be used, look at SimpleTests.py. Here there are unit tests that set up very simple test documents and compute 
all the desired similarities.

### Who do I talk to? ###

* admin: Philip Tillman <phil.tillman@gmail.com>
* researcher: Nel de Jong <c.a.m.dejong@uva.nl>

### Publishing using our code ###
Please cite our paper if you use this code:

de Jong, N., & Tillman, P. C. (2018). Grammatical structures and oral fluency in immediate task repetition: 
trigrams across repeated performances. In M. Bygate (Ed.), Learning language through task repetition (pp. 43-73). 
Amsterdam: John Benjamins.

```
@article{deJongTillman2018,
  title={ Grammatical structures and oral fluency in immediate task repetition: trigrams across repeated performances},
  author={de Jong, N., & Tillman, P. C.},
  journal={Learning language through task repetition},
  editor={M. Bygate},
  publisher={John Benjamins},
  location={Amsterdam},
  year={2018}
}
```

### License ###
Copyright 2019 Philip Tillman

Licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html) (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
