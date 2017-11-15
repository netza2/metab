#!/usr/bin/env python
from deepdive import *
import os
import sys
import random

APP_HOME = os.environ['APP_HOME']

#Names of Enzymes
#with open(APP_HOME + '/input/enzymes_names.tsv','r') as E1: enz1 = E1.readlines()
#with open(APP_HOME + '/input/enzymes_names_n.tsv','r') as E2: enz_n = E2.readlines()
with open(APP_HOME + '/input/enz_words.tsv', 'r') as E: enz = E.readlines()
#with open(APP_HOME + '/input/dois.tsv', 'r') as d: dois = d.readlines()

words = []
words_o = []
for i in range(len(enz)): enz[i] = enz[i].lower().strip('\n')

for i in enz:
    if i.find(" ") != -1: 
        for n in i.split(" "): words.append(n)
    else: words.append(i)
    if i.find("---") != -1:
        for n in i.split('---'): words.append(n)
words_o = set(words_o)
words = set(words)
enz = set(enz)
#for i in range(len(dois)): dois[i]  = dois[i].strip('\n')
#dois = set(dois)
#c = 0
#print >> sys.stderr, '\n\n\n\n\n' + str('adp-glucose' in words) + '\n\n\n\n\n'
#print >> sys.stderr,"##################" +  "\n\n\n\n\nWORDS ALONE:" + str(len(words_o)) + "\nWORDS: " + str(len(words)) + "\nENZYMES: " + str(len(enz)) + '\n\n\n\n\n'
# For python 3 compatibility ?
try:
    xrange
except NameError:
    xrange = range


@tsj_extractor
@returns(lambda
        mention_id       = "text",
        mention_text     = "text",
        doc_id           = "text",
        sentence_index   = "int",
        begin_index      = "int",
        end_index        = "int",
    :[])

def map_enz(
        doc_id         = "text",
        sentence_index = "int",

        tokens         = "text[]",
        pos_tags       = "text[]",
        ner_tags       = "text[]",
    ):
#   global c

    num_tokens = len(tokens)
#    print >> sys.stderr, doc_id
    if num_tokens < 130:# and doc_id in dois:
        first_indexes = []
        for i in range(num_tokens):
#            if tokens[i].lower() == 'adp-glucose': print >> sys.stderr, '\n\n\n\n\n' +tokens[i]  + '\n\n\n\n\n'
            if tokens[i].lower() in words and (i == 0 or tokens[i-1].lower() not in words):
                first_indexes.append(i)
            elif tokens[i].find('-') != -1 and tokens[i].lower().replace('-',' ') in enz:
                enz.add(tokens[i])
                first_indexes.append(i)
               ##   Add tokens[i] to words.tsv
#        first_indexes = (i for i in xrange(num_tokens) if tokens[i].lower() in set(words) and (i == 0 or tokens[i-1].lower() not in set(words)))    
        for begin_index in first_indexes:                  
            end_index = begin_index + 1
  
# # # # # # # # # # # # #Select mentions of the enzymes
            while end_index < num_tokens and tokens[end_index].lower() in set(words) and tokens[end_index].lower() != tokens[end_index-1].lower():
                end_index += 1
            end_index -= 1
#        n = pos_tags[begin_index:end_index + 1]
#        if 'IN' in n or 'DT' in n or 'CC' in n or 'MD' in n or 'VB' in n or 'VBD' in n or 'VBG' in n or 'VBP' in n: continue
        
            mention_id = "%s_%d_%d_%d" % (doc_id, sentence_index, begin_index, end_index)
            mention_text = " ".join(map(lambda i: tokens[i], xrange(begin_index, end_index + 1)))
            if mention_text.lower() not in enz: continue

            yield [
                mention_id,
                mention_text,
                doc_id,
                sentence_index,
                begin_index,
                end_index,
            ]

    else:
        pass
 





#        with open(APP_HOME + '/output.tsv','a') as F:

#            F.write(doc_id + '\t' + str(sentence_index) + '\t' + "[" + ' '.join(tokens) + "]" + '\t' + "[" + ' '.join(pos_tags) + "]" + '\t'+ "[" + ' '.join(ner_tags) + "]"  + '\n')
        
#        print >> sys.stderr , '\n\n\n\n' , c , "| # number of tokens: ", num_tokens
#        print >> sys.stderr, ' '.join(tokens),'\n\n\n\n'
        
