# -*- coding: UTF-8 -*-

import re
import pandas as pd
import collections
import nltk
import string
import pickle
import numpy as np
import sys

# Apply the function LIWC_detect to a text. It removes punctuation, tokenizes and matches 
# the tokens to LIWC with the help of the star_check function and the nstar_liwc_dict and 
# star_liwc_dict. The result is a vector of counts for the 73 LIWC categories (see appended 
# list), as well as a counter of matched LIWC tokens, and a counter of tokens in general.
# To a list of these vectors, you can apply the veclist_to_df function, which will transform
# them into a nice pandas dataframe with the LIWC categories as column names. You can divide 
# the categories by either of the two counters to get percentage values.

with open('french_nstar_liwc_dict','rb') as f:
    nstar_liwc_dict = pickle.load(f)

with open('french_star_liwc_dict','rb') as f:
    star_liwc_dict = pickle.load(f)

def star_check(word,vec_length=66):
	# Check for match with wordstem dictionary (star_liwc_dict). If no match, return vector representing unmatched token. 
    for i in reversed([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]):
        try:
            return(star_liwc_dict[i][word[:i]])
        except KeyError:
            continue
    null_vec = np.zeros(vec_length)
    null_vec[-1] = 1
    return(null_vec)

def LIWC_detect(text):
	# chek for match with normal liwc dictionary (nstar_liwc_dict). If non found, apply star_chek.
    vec = np.zeros([66])
    if not isinstance(text,str):
        return(vec)
#    puncts = string.punctuation
    puncts = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
    text = nltk.word_tokenize(re.sub('\&gt;|['+puncts+']', ' ', text).lower())
    for token in text:
        w_emo = nstar_liwc_dict.get(token,0)
        if isinstance(w_emo, int):
            w_emo = star_check(token)
        vec[:] += w_emo
    return(vec)

def veclist_to_df(vec_list):
	col_list = ['fonction', 'pronom', 'pronomp', 'je', 'nous', 'vous', 'il', 'ils', 'pronomimp', 'article', 'verbe', 'verbeauxi', 'verbepassé', 'verbeprésent', 'verbefutur', 'adverbe', 'préposition', 'conjonction', 'négation', 'quantifieur', 'nombre', 'juron', 'social', 'famille', 'ami', 'humain', 'affect', 'émopos', 'émonég', 'anxiété', 'colère', 'tristesse', 'cognition', 'perspicacité', 'cause', 'divergence', 'tentative', 'certitude', 'inhibition', 'inclusion', 'exclusion', 'perception', 'voir', 'entendre', 'sentir', 'biologique', 'corps', 'santé', 'sexualité', 'alimentation', 'relativité', 'mouvement', 'espace', 'temps', 'travail', 'accomplissement', 'loisir', 'maison', 'argent', 'religion', 'mort', 'consentement', 'hésitation', 'remplisseur']
	return(pd.DataFrame(data=vec_list,columns=col_list))




with open(sys.argv[1], "rt") as fin:
    with open(sys.argv[1]+".out.all", "wt") as fout:
        for line in fin:
            fields = line.split("\t")
            liwcs = LIWC_detect(fields[6].lower())
            fout.write(fields[0] + "\t" + fields[1] + "\t" + fields[2] + "\t" + fields[3] + "\t" + fields[4] + "\t" + fields[5])
            l = ""
            for v in liwcs:
                l = l + "\t" + str(v)

            fout.write(l + "\n")


