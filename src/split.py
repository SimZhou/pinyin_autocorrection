#!/usr/bin/env python
# coding: utf-8
# author: https://github.com/SimZhou

import pickle
from functools import lru_cache

counter_1g = pickle.load(open("1gram.counter", 'rb'))

def P(string_list, counterObject=counter_1g, default=0):
    "返回一列字符串的出现概率（依据词库）"
    probility = 1
    for token in string_list:
        if token not in counterObject:
            probility *= default
        else:
            probility *= counterObject.get(token)/sum(counterObject.values())
    return probility

P(['wo'], counter_1g), P(['w'], counter_1g)


split_solutions = {}
@lru_cache(maxsize=2**10)
def best_split(string):
    
    notes = [(P([string]), '', string)] + [(best_split(string[:i]) * best_split(string[i:]), string[:i], string[i:]) for i in range(1, len(string))]
    
    prob, left, right = max(notes, key = lambda x: x[0])
    
    split_solutions[string] = (left, right)
    return prob

best_split('woyaoshangqinghua')

split_solutions

def parse_split_solution(string):
    left, right = split_solutions[string]
    if not left: return [right]
    return parse_split_solution(left) + parse_split_solution(right)

parse_split_solution('woyaoshangqinghua')
parse_split_solution('woshiyizhizhu')

def split(string):
    if string in split_solutions: return parse_split_solution(string)
    else:
        best_split(string)
        return parse_split_solution(string)

split("wobushizhu")
    