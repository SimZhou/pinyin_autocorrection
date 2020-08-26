#!/usr/bin/env python
# coding: utf-8
# author: https://github.com/SimZhou

import pickle

class Corrector:
    def __init__(self, gram=1):
        '''
        the grams parameter specifies the N-gram counter object to read from.
        Currently we only have 1gram, 4gram and 7gram
        '''
        print("Loading corpus...")
        self.counter = pickle.load(open(str(gram)+"gram.counter", 'rb'))
        print("Corpus loading complete!")        
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        
    def correct(self, word):
        candidates = (self.known(self.edits0(word)) or 
                     self.known(self.edits1(word)) or
                     self.known(self.edits2(word)) or
                     [word])
        return max(candidates, key=lambda x: self.counter.get(x))

    def correct_sequence(self, text):
        '''
        This function corrects a sequence of pinyin splited by spaces.
        E.g. 
        "wo shi shiu" -> "wo shi shui"
        '''
        return ' '.join(map(self.correct, text.split()))

    def known(self, words):
        '''
        判断某个词是否在Counter中
        '''
        return {w for w in words if w in self.counter}
    
    def edits0(self, word):
        return {word}
    
    def edits1(self, word):
        '''
        编辑距离为1的词，应该是这些词，在原词的每个<切分点>，可以有这么些操作：
        1. 漏打：删除<切分点>右边的字符（当切分点右边有词时）
        2. 错打：替换<切分点>右边的字符（当切分点右边有词时）
        3. 多打：在<切分点>插入一个字符
        4. 换位：两个字符的位置打反了，交换切分点左右的两个词（当切分点左右都有词时）
        '''
        pairs      = self.allSplits(word)
        deletes    = [a+b[1:]           for (a, b) in pairs if b]
        replaces   = [a+c+b[1:]         for (a, b) in pairs for c in self.alphabet if b]
        inserts    = [a+c+b             for (a, b) in pairs for c in self.alphabet]
        switches   = [a[:-1]+b[0]+a[-1]+b[1:] for (a, b) in pairs if (a and b)]
        return set(deletes + replaces + inserts + switches)
    
    def edits2(self, word):
        '''编辑距离为2的词，就是所有那些与目标词编辑距离为1的词 编辑距离为1的词'''
        return {e2 for e1 in self.edits1(word) for e2 in self.edits1(e1)}
    
    def edits3(self, word):
        return {e3 for e1 in self.edits1(word) for e2 in self.edits1(e1) for e3 in self.edits1(e2)}
    
        
    def allSplits(self, word):
        '''Return a list of all possible (first, rest) pairs that comprise pinyin'''
        return [(word[:i], word[i:])
                 for i in range(len(word)+1)]
    
    def get_deletes(self, word):
        pairs      = self.allSplits(word)
        deletes    = [a+b[1:]           for (a, b) in pairs if b]
        return deletes
    
    def get_replaces(self, word):
        pairs      = self.allSplits(word)
        replaces   = [a+c+b[1:]         for (a, b) in pairs for c in self.alphabet if b]
        return replaces
        
    def get_inserts(self, word):
        pairs      = self.allSplits(word)
        inserts    = [a+c+b             for (a, b) in pairs for c in self.alphabet]
        return inserts
    
    def get_transposes(self, word):
        pairs      = self.allSplits(word)
        transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
        return transposes

if __name__ == "__main__":
    crt = Corrector(4)
    crt.correct("zhognguo")
    crt.correct("qighuadaxeu")
    crt.correct("beijindaxue")



# ## 思考总结：
# **1. 成功通过n-gram实现了连打拼音纠错功能，初步判断效果还不错**
# 
# **2. 我最后的实现方式和高老师上课所提到的方法不同：高老师提到的先切分再改进的方法，我尝试了一下，由于错误的输入序列很难通过语言模型进行正确的分割，所以没能成功；因此我改用了另一种方法，也就是直接进行纠错，然后再切分的方法，成功实现了**
# 
# **3. 这种实现方式需要的计算量并不算大，不过需要提前建立n-gram的语言模型并保存到硬盘中，需要的储存量可能较大，这可能也是各大输入法的拼音纠错功能仅在联网时开启的原因？（手机端）**
# 
# **改进方向1：这次用的语料库有限（仅为article_9k），可以用过增加、改进语料库来进一步提升效果**
# 
# **改进方向2：这次没有考虑中文分词，可以考虑在预处理token的时候，先用jieba进行分词，然后再建n-gram，而不是现在这样简单地用单个中文字当作token**
# 
