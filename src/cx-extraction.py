#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This program extracts constructions for overlap calculation.

Plan:


'''
import ntpath
import glob
import re
import spacy
from corpus_toolkit import corpus_tools as ct
from streamlit import stop

__author__ = 'Masaki Eguchi'

nlp = spacy.load("en_core_web_trf")


def preprocess(text):
    # spaces
    text = text.strip()
    text = re.sub("\n+", "\n", text)
    text = re.sub("(-\n)+", " ", text)
    text = re.sub("\t+", " ", text)
    text = re.sub("\s+", " ", text)
    text = text.replace(";", ".")
    text = text.replace(":", ".")
    #while "-\n" in text:
    #	text = text.replace("-\n", " ")
    #while "\t" in text:
    #	text = text.replace("\t", " ")
    #while "  " in text:
    #	text = text.replace("  ", " ")
    #while ";" in text:
    #	text = text.replace(";", ".")
    #while ":" in text:
    #	text = text.replace(":", ".")
    return (text)


def ngrammer(tokenized, number, connect="__", stop_list=['.', ',', '!', '?']):
    ngram_list = []  #empty list for ngrams
    last_index = len(tokenized) - 1
    #this will let us know what the last index number is
    for i, token in enumerate(tokenized):
        #enumerate allows us to get the index number for each iteration (this is i) and the item
        if i + number > last_index:  #if the next index doesn't exist (because it is larger than the last index)
            continue
        else:
            ngram = tokenized[i:i + number]
            #the ngram will start at the current word, and continue until the nth word
            ngram_string = connect.join(ngram)
            #turn list of words into an n-gram string
            if any(s in ngram_string for s in
                   stop_list):  #Check if a stop list word is in the string.
                continue
            else:
                ngram_list.append(ngram_string)  #add string to ngram_list

    return (ngram_list)  #add ngram_list to master list


def simple_tokenizer(text, split_token=" "):

    tok_list = text.split(split_token)
    return tok_list


def tokenizer(text, sent_bound=True, lemmatize=False, pos=False):
    doc = nlp(text)
    tok_list = []
    for sent in doc.sents:
        sent_tok = []
        for tok in sent:
            if lemmatize:
                sent_tok.append(tok.lemma_)
            elif pos:
                sent_tok.append(tok.tag_)
            else:
                sent_tok.append(tok.norm_)
        if sent_bound:
            tok_list.append(sent_tok)
        else:
            if len(tok_list) == 0:
                tok_list.append([])
            tok_list[0].extend(sent_tok)
    return tok_list


def counter(items: list):
    res = {}
    for item in items:
        if item not in res:
            res[item] = 1
        else:
            res[item] += 1
    return res


def dict_to_cex(dict, output_dir, s_filename, header):
    with open(output_dir + s_filename + '.cex', 'w') as outf:
        outf.write(header)

        for item, freq in dict.items():
            outf.write(' '.join([str(freq), item]))
            outf.write("\n")


def text_to_ngrams(filename, length=1):
    s_fname = ntpath.basename(filename)

    text = open(filename, 'r').read()
    text = preprocess(text)
    #tok = simple_tokenizer(text)
    tok = tokenizer(text, sent_bound=False, lemmatize=False, pos=False)
    ngrams = ngrammer(tok[0], length, connect=" ")
    ngram_dict = counter(ngrams)
    dict_to_cex(ngram_dict, 'input/trigram/', s_fname, "#\n#\n#\n#\n#\n#\n")


# if __name__ == "__main__":
filename = glob.glob('rawtexts/*')

for file in filename:
    text_to_ngrams(file, length=3)
