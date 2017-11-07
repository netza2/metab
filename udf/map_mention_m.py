#!/usr/bin/env python
from deepdive import *
import os

##metabolites
APP_HOME = os.environ['APP_HOME']


M = open(APP_HOME + '/input/Metab.tsv','r')
Me = M.readlines()
M.close()

m = open(APP_HOME +'/input/metabol.tsv','r')
me = m.readlines()
m.close()


words = []
Metabolites = []
for i in me: Metabolites.append(i.lower().strip('\n'))
for i in me: 
    for n in i.lower().strip('\n').split(' '):
        words.append(n)  ##delete the new line character

words = set(words)
Metabolites = set(Metabolites)

exact = {'co','cO','CO','cA','ca','CA','aG', 'AG','ag','cD', 'CD','cd', 'CU','cu','cU', 'HG','hg','hG','CL','cl','cL','FE','fe','fE','Mn','MN','mN','mn','Mg','mg','mG','No','no','Camp','camp','k','NA','na','nA','h'}

@tsv_extractor
@returns(lambda
        mention_id       = "text",
        mention_text     = "text",
        doc_id           = "text",
        sentence_index   = "int",
        begin_index      = "int",
        end_index        = "int",
    :[])

def map_mention_m(
        doc_id         = "text",
        sentence_index = "int",
        tokens         = "text[]",
        pos_tags       = "text[]",
        ner_tags       = "text[]",
    ):

    num_tokens = len(tokens)    #number of tokens, look for mentions of metabolites
    first_indexes = (i for i in xrange(num_tokens) if tokens[i].lower() in set(words) and (i == 0 or tokens[i-1].lower() not in set(words)))    
    for begin_index in first_indexes:                  
        end_index = begin_index + 1  

        #select mentions of the metabolites
        while end_index < num_tokens and (tokens[end_index].lower() in set(words))  and (tokens[end_index].lower() != tokens[end_index-1].lower()):
            end_index += 1
        end_index -= 1
        #n = pos_tags[begin_index:end_index + 1]
        #if 'IN' in n or 'DT' in n or 'CC' in n: continue
        

        mention_id = "%s_%d_%d_%d" % (doc_id, sentence_index, begin_index, end_index)
        mention_text = " ".join(map(lambda i: tokens[i], xrange(begin_index, end_index + 1)))

        if end_index == begin_index and ('CD' in n or 'VBD' in n or 'VBG' in n or 'VBN' in n or 'JJ' in n): continue


        if mention_text.lower() not in Metabolites:continue
        if mention_text in exact: continue
        yield [
            mention_id,
            mention_text,
            doc_id,
            sentence_index,
            begin_index,
            end_index,
        ]



"""
words = ' '.join(words)                   ##join all the words with a space
words2 = words.replace(' ','-')             ##split them again in a single list
words2 = words2.split('-')
words = words.split(' ')
words = words + words2
words = set(words)
words = list(words)

remove = ['amino acid','acid','adapted','alcohol','alpha','amino','aromatic','anion','antigen','acetic','acyl','coenzyme','b4','benzyl','carbon','carbonic','cofactor','cold','cyclic','core','derivative','enzyme','ferric','g2','heme','iia','iii','ion','iva','ix','linear','lipid','inorganic','minus','modified','oxo','protein','reduced','secondary','sugar','vitamin','lactic','ketone','ester','aryl']
r_not_first = ['core','iii','ix','iia','iva']

        if mention_text.lower() in set(remove):continue


        if mention_text.find(' ') != -1:
            s = mention_text.split(' ')
            if s[0].lower() in set(r_not_first):continue

        if len(mention_text) == 1:
            continue
        if  mention_text.lower() in set(remove):
            continue 

        if end_index == begin_index and ('CD' in n or 'VBD' in n or 'VBG' in n or 'VBN' in n or 'JJ' in n): continue
        
        if mention_text.find(' ') != -1:
            s = ''.join(mention_text.split(' '))
            i = 0
            for j in s:
                if ord(j) > 58 or ord(j) < 47:
                    i+=1
            if i == 0: continue
                
            if s[-1] == '-': continue
            if s[0] == ')' or s[-1] == ')': continue
            if len(s) == 2:
                if ( pos_tags[begin_index] == 'CD' and len(s[1]) == 1 ) or ( pos_tags[begin_index + 1] == 'CD' and len(s[0]) == 1 ) or ( len(s[0]) == 1 and s[1].lower() in set(remove) ) or (len(s[1]) == 1 and s[0].lower() in set(remove) ): continue
                if s[1] == ')': continue
"""


"""

        if mention_text.find(',') != -1:           ### continue if the mention is
            s =''.join(mention_text.split(','))   ### a list of numbers separated
            i = 0                                  ### by a coma
            for j in s:
                if ord(j) > 58 or ord(j) < 47:
                    i+=1
            if i == 0: continue
                
"""


