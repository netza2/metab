#!/usr/bin/env python
from deepdive import *
import random
import sys
from collections import namedtuple

Label = namedtuple('Label', 'p1_id, p2_id,  label, rule_id')

@tsj_extractor
@returns(lambda
        p1_id            = "text",
        p2_id            = "text",
        label            = "int",
        rule_id          = "text",
    :[])
# heuristic rules for finding positive/negative examples of spouse relationship mentions
def supervise(
        p1_id             = "text",
        p2_id             = "text",
        p1_begin          = "int", 
        p1_end            = "int",
        p2_begin          = "int", 
        p2_end            = "int",
        doc_id            = "text", 
        sentence_index    = "int", 
        tokens            = "text[]", 
        pos_tags          = "text[]", 
        ner_tags          = "text[]", 
        lemmas            = "text[]",
        dep_types         = "text[]",
        dep_tokens        = "int[]",
    ):

    # Constants
    
#    RXS = frozenset(['reaction','catalyze','react','catalyzation','reacting'])
#    CONVERT = frozenset(['convert','conversion'])
    PRA = frozenset(['to','from','with','on','the'])
    
    TRANSFORM = frozenset(['transform','transformation'])
    PROM = frozenset(['promiscuous','promiscuity','promiscuously'])
    WORDS = frozenset(['structurally','transfer','interactor','interactors','interaction','activation','compounds','evolutionary','evolution','catalytic','metabolic','structural','chemical','ligand','molecular','activator','receptor'])

    ANOT = frozenset(['IN','DT','CC','MD','VB','VBD','VBG','VBP','RB', 'JJ'])
    KeyW = frozenset(['enzyme','enzymes','protein','proteins','substrate','substrates','gene','genes'])

    # Common data objects
    p1_begin_index = min(p1_begin, p2_begin)
    p2_begin_index = max(p1_begin, p2_begin)
    p1_end_index = min(p1_end,p2_end)
    p2_end_index = max(p1_end, p2_end)
    init_lemmas = lemmas[:p1_begin_index]
    intermediate_lemmas = lemmas[p1_end_index+1:p2_begin_index]
    init_ners = ner_tags[:p1_begin_index]    
    tail_lemmas = lemmas[p2_end_index+1:]

    

    mention1 = ''.join(tokens[p1_begin : p1_end + 1])
    mention2 = ''.join(tokens[p2_begin : p2_end + 1])
    mention_lemmas = lemmas[p1_begin :p2_end + 1]
    mention_lemmas_str = ' '.join(mention_lemmas)

    label = Label(p1_id = p1_id, p2_id = p2_id, label = None, rule_id = None)


    if len(tokens) >= 120:
 #######       print >> sys.stderr, '\n\n\n', tokens,'\n\n\n'
        yield label._replace( label = -6, rule_id = 'neg:sent_too_long')
        pass
    if len(ANOT.intersection(pos_tags[p1_begin : p1_end + 1])) > 0:
        yield label._replace(label = -4, rule_id = 'neg:pos_tag')
        pass
    if mention2.lower() in list(KeyW):
#        print >>sys.stderr, 'no promiscucous function:', mention1, mention2
        yield label._replace(label = -1, rule_id = 'neg:no_prom_mention')


#        print >>sys.stderr,'\n\n','||'.join(list(ANOT)),'\n',mention1,'#',pos_tags[p1_begin:p1_end+1],'\n', 'pos_tags:', pos_tags[p1_begin-1:p1_end + 2],'##', ' '.join(tokens[p1_begin-1: p1_end + 2]),'\n\n'
    if len(intermediate_lemmas) < 6 and mention2.lower() not in list(KeyW):
        yield label._replace(label = 1, rule_id = 'pos:close_mentions')
 
    if len(PROM.intersection(mention2.split(' '))) > 0 or len(PROM.intersection(tokens[p1_begin - 2:p1_end + 3])) > 0:
#        print >>sys.stderr, 'promiscuous :', mention1,'#####'  , mention2, tokens[p1_begin_index : p2_end_index + 1]
        yield label._replace(label = 3, rule_id = 'pos:prom_mention')

 #   if PROM.intersection(tokens[p1_begin_index - 3 : p2_end_index + 3]) > 0:
#        yield label._replace(label = 2, rule_id = 'pos:prom')
    if len(intermediate_lemmas) > 6:
        yield label._replace(label = -2, rule_id = 'neg:far_mentions')

    if 'PERSON' in init_ners:
        yield label._replace(label = -3, rule_id = 'article_ref')

    if len(WORDS.intersection(intermediate_lemmas)) > 0 or len(KeyW.intersection(intermediate_lemmas)) > 0:
        yield label._replace(label = 2, rule_id = 'pos:word_inter')


#mention1.lower() in list(PROM) or mention2.lower() in list(PROM): #mention_lemmas_str.lower() in list(PROM):

#    if len(mention) > 1: 
#        if len(PROM.intersection(mention)) > 0:
#            yield label._replace(label = 4, rule_id = 'pos:prom_mention')
       
"""
    if len(WORDS.intersection(init_lemmas)) > 0:
        yield label._replace(label=1, rule_id='pos:word_init')

    if len(WORDS.intersection(tail_lemmas)) > 0:
        yield label._replace(label=1, rule_id='pos:word_tail')

    if len(KeyW.intersection(intermediate_lemmas)) > 0:
        yield label._replace(label=1, rule_id='pos:word_inter')

    if len(KeyW.intersection(init_lemmas)) > 0:
        yield label._replace(label=1, rule_id='pos:word_init')

    if len(KeyW.intersection(tail_lemmas)) > 0:
        yield label._replace(label=1, rule_id='pos:word_tail')

"""
