#!/usr/bin/env python
from deepdive import *
words_e = ['escherichia coli', 'e. coli', 'escherichia coli k12', 'e. coli k12', 'mg1655', 'k12 mg1655', 'ijo1366','escherichia coli k12 mg1655']
words = ['coli','e.','escherichia', 'mg1655', 'ijo1366','k12']

@tsj_extractor
@returns(lambda
        mention_id       = "text",
        mention_text     = "text",
        doc_id           = "text",
        sentence_index   = "int",
        begin_index      = "int",
        end_index        = "int",
    :[])
def map_mention_e(
        doc_id         = "text",
        sentence_index = "int",

        tokens         = "text[]",
        pos_tags       = "text[]",
        ner_tags       = "text[]",
            ):

    num_tokens = len(tokens)    #number of tokens, look for mentions of e. coli 
    first_indexes = (i for i in xrange(num_tokens) if tokens[i].lower() in set(words) and (i == 0 or tokens[i-1].lower() not in set(words)))    
    for begin_index in first_indexes:                  
        end_index = begin_index + 1  
        #select just the indexes for words not repeated and mentions only made of two words
        while end_index < num_tokens and (tokens[end_index] in set(words)) and (tokens[end_index] != tokens[end_index-1]) and end_index-begin_index < 2:
            end_index += 1
        end_index -= 1
        mention_id = "%s_%d_%d_%d" % (doc_id, sentence_index, begin_index, end_index)
        mention_text = " ".join(map(lambda i: tokens[i], xrange(begin_index, end_index + 1)))
#        if mention_text.lower() == 'e.' or mention_text.lower() == 'coli':
#            continue
        if mention_text.lower() not in words_e: continue
        yield [
            mention_id,
            mention_text,
            doc_id,
            sentence_index,
            begin_index,
            end_index,
        ]
