#!/usr/bin/env python
# coding: utf-8
# author: https://github.com/SimZhou

'''
This script preprosesses the raw corpus, 
makes it into reusable objects for split and autocorrection.

To be specific, the raw corpus is pre-calculated into those objects:
    
<Counter object>: containing different levels (up to 7) of gram tokens, with their count
'''

from collections import Counter
import pinyin
import re
import pickle

# Read Dataset
CHN_CHAR_SET = open("article_9k.txt", encoding='utf-8').read()
CHN_CHAR_SET[:1000]

# CHAR to PINYIN
def chn_to_py(character):
    '''
    Chinese to Pinyin
    '''
    return pinyin.get(character, format='strip', delimiter=' ')

CHN_PY_SET = chn_to_py(CHN_CHAR_SET)
CHN_PY_SET[:1000]
len(CHN_PY_SET)

# wash tokens preserving a-z only, and make them into List 
def token(text):
    '''
    去掉所有的数字，特殊符号，仅保留[a-z]+
    返回拼音列表
    '''
    return re.findall('[a-z]+', text.lower())

TOKENS = token(CHN_PY_SET)
TOKENS[:50]


# Making counters with 1-7 Grams
def generate_ngrams(tokens, n):   
    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return ["".join(ngram) for ngram in ngrams]

generate_ngrams(["wo", "hen", "hao"], 2)

TOKENS_1G = TOKENS
TOKENS_2G = generate_ngrams(TOKENS, 2)
TOKENS_3G = generate_ngrams(TOKENS, 3)
TOKENS_4G = generate_ngrams(TOKENS, 4)
TOKENS_5G = generate_ngrams(TOKENS, 5)
TOKENS_6G = generate_ngrams(TOKENS, 6)
TOKENS_7G = generate_ngrams(TOKENS, 7)
TOKENS_7G[:1000]

# Making Tokens into Counter
Counter_1G = Counter(TOKENS_1G)
Counter_1G.most_common(200)

Counter_till_7G = Counter(TOKENS_1G)
pickle.dump(Counter_till_7G, open("1gram.counter", 'wb')) # saving staged counter
Counter_till_7G.update(TOKENS_2G)
Counter_till_7G.update(TOKENS_3G)
Counter_till_7G.update(TOKENS_4G)
pickle.dump(Counter_till_7G, open("4gram.counter", 'wb')) # saving staged counter
Counter_till_7G.update(TOKENS_5G)
Counter_till_7G.update(TOKENS_6G)
Counter_till_7G.update(TOKENS_7G)
pickle.dump(Counter_till_7G, open("7gram.counter", 'wb')) # saving staged counter


Counter_till_7G.most_common(200)

