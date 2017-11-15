#!/usr/bin/env python
from deepdive import *
import os
import random
from collections import namedtuple

APP_HOME = os.environ['APP_HOME']
#Words mapped
#w = open(APP_HOME + '/input/words.tsv','r')
#words = w.readlines()
#w.close()


#for i in range(len(words)): words[i] = words[i].strip('\n')
w = []
#for i in words:
 #   if i.find(" ") == -1:
  #      for n in i.split(" "): w.append(n)
   # else: w.append(i)

#words = ['promiscuous','promiscuously','promiscuity','function','novel','function','functions','functional', 'escherichia', 'coli','e.']

w = ['promiscuous','promiscuity','novel','function','moonlight','promiscuously']
words = ['promiscuous','promiscuity','novel function','moonlight','promiscuously']
words = set(words)

w = set(w)
key_words = frozenset(['promiscuous','promiscuously','promiscuity','novel','function','functions','functional', 'escherichia' ,'coli'])



@tsj_extractor
@returns(lambda
        mention_id       = "text",
        mention_text     = "text",
        doc_id           = "text",
        sentence_index   = "int",
        begin_index      = "int",
        end_index        = "int",
    :[])

def map_words(
        doc_id         = "text",
        sentence_index = "int",
        tokens         = "text[]",
        pos_tags       = "text[]",
        ner_tags       = "text[]",
    ):

    num_tokens = len(tokens)    #number of tokens, look for mentions of enzymes
    first_indexes = (i for i in xrange(num_tokens) if tokens[i].lower() in w and (i == 0 or tokens[i-1].lower() not in w))    
    for begin_index in first_indexes:                  
        end_index = begin_index + 1  
        #select mentions of the enzymes
        while end_index < num_tokens and (tokens[end_index].lower() in w )  and tokens[end_index].lower() != tokens[end_index-1].lower():
            end_index += 1
        end_index -= 1        
        mention_id = "%s_%d_%d_%d" % (doc_id, sentence_index, begin_index, end_index)
        mention_text = " ".join(map(lambda i: tokens[i], xrange(begin_index, end_index + 1)))
#        mention_text_array = map(lambda i: tokens[i].lower(), xrange(begin_index, end_index +1))
        
        if mention_text.lower() not in words: continue
#        if len(key_words.intersection(mention_text_array)) == 0: continue

        yield [
            mention_id,
            mention_text,
            doc_id,
            sentence_index,
            begin_index,
            end_index,
        ]
