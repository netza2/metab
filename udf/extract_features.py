#!/usr/bin/env python
from deepdive import *
import ddlib
import os
import sys
import random

APP_HOME = os.environ['APP_HOME']

with open(APP_HOME + '/input/articles_id.tsv', 'r') as file: dois = file.readlines()

for i in range(len(dois)): dois[i] = dois[i].strip('\n')
for i in range(len(dois)): dois[i] = dois[i].strip('"')

dois = set(dois)

@tsj_extractor
@returns(lambda
        p1_id          = "text",
        p2_id          = "text",
        feature        = "text",
    :[])
def extract(
        p1_id          = "text",
        p2_id          = "text",
        p1_begin       = "int", 
        p1_end         = "int",
        p2_begin       = "int", 
        p2_end         = "int",
        doc_id         = "text",
        sentence_index = "int",
        tokens         = "text[]",
        pos_tags       = "text[]",
        ner_tags       = "text[]",
        lemmas         = "text[]",
        dep_types      = "text[]",
        dep_tokens     = "int[]",
    ):
    # Create a DDLIB sentence object, which is just a list of DDLIB Word objects

    val = 1
    if doc_id in dois: val = 0
    sent = []
    for i,t in enumerate(tokens):
        sent.append(ddlib.Word(
            begin_char_offset=None,
            end_char_offset=None,
            word=t,
            lemma=lemmas[i],
            pos=pos_tags[i],
            ner=ner_tags[i],
            dep_par=dep_tokens[i] - val,
            dep_label=dep_types[i]))#  # Note that as stored from CoreNLP 0 is ROOT, but for DDLIB -1 is ROOT



    span1 = ddlib.Span(begin_word_id = p1_begin, length = (p1_end - p1_begin + 1))
    span2 = ddlib.Span(begin_word_id = p2_begin, length = (p2_end - p2_begin + 1))

    for feature in ddlib.get_generic_features_relation(sent, span1, span2):
        yield [p1_id, p2_id, feature]



"""
  span = ddlib.Span(begin_word_id=begin_index, length=(end_index-begin_index+1))
    for feature in ddlib.get_generic_features_mention(sent, span):
        yield [mention_id, feature]
"""
