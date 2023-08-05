import numpy as np 
import pandas as pd 
from prefixspan import PrefixSpan 
from tqdm import tqdm 
import warnings 
from dataclass import DataClass
warnings.filterwarnings('ignore') 
tqdm.pandas() 

class SequencePattern(DataClass):
    def __init__(self, data, use_behavior=[], del_behavior = [], min_support=0.2, min_length=3, max_length=6, sep='@'):
        self.min_support = min_support
        self.min_length = min_length
        self.max_length = max_length
        self.behavior_set = set()
        self.black_behavior, self.white_behavior = self.data_preprocess(data, use_behavior, del_behavior, sep)

    def is_subsequence(self, s, t):
        if len(s) > len(t):
            return False
        n, m = len(s), len(t)
        i = j = 0
        while i < n and j < m:
            if s[i] == t[j]:
                i += 1
            j += 1
        return i == n
    
    def remove_subseq(self, lst):
        n = len(lst)
        flag = [True] * n   # 标记每个序列是否被删除
        for i in range(n):
            for j in range(i+1, n):
                # 若lst[i]是lst[j]的子序列，则删除lst[i]
                if self.is_subsequence(lst[i], lst[j]):
                    flag[i] = False
                    break
                # 若lst[j]是lst[i]的子序列，则删除lst[j]
                elif self.is_subsequence(lst[j], lst[i]):
                    flag[j] = False
        # 将没有被删除的序列加入新的列表中，并返回该列表
        res = [lst[i] for i in range(n) if flag[i]]
        return res
    
    def run(self, lift=2):
        
        ps = PrefixSpan(self.black_behavior)
        ps.minlen = self.min_length # 最小模式长度
        ps.maxlen = self.max_length # 最大模式长度
        result = ps.frequent(self.min_support * len(self.black_behavior), closed = True) 
        
        patten_use = self.remove_subseq([temp[1] for temp in result])
        
        white_count = []
        for com in tqdm(patten_use):
            count = np.sum([self.is_subsequence(com, behavior) for behavior in self.white_behavior])
            white_count.append(count)
        
        result = pd.DataFrame(result, columns = ['hit_black_count', 'patten_use'])
        result['patten'] = result['patten_use'].apply(lambda x: '->'.join(x))

        temp = pd.DataFrame([patten_use, white_count]).T
        temp.columns = ['patten', 'hit_white_count']
        temp['patten'] = temp['patten'].apply(lambda x: '->'.join(x))

        result = pd.merge(result, temp, on = 'patten', how = 'left') 
        result['patten_len'] = result['patten_use'].apply(lambda x: len(x))

        result['patten_black_retio'] = result['hit_black_count'] / (result['hit_white_count'] + result['hit_black_count'])
        result['data_black_retio'] = len(self.black_behavior) / (len(self.black_behavior) + len(self.white_behavior))
        result['lift'] = result['patten_black_retio'] / result['data_black_retio']
        result = result.sort_values(by = ['lift'], ascending=False).reset_index(drop = True)

        result.insert(0, 'id', 'combine_pattern_' + result.index.astype(str))
        result = result[['id', 'patten', 'patten_len', 'patten_black_retio', 'data_black_retio', 'lift', 'hit_black_count', 'hit_white_count']]

        for p in patten_use:
            self.behavior_set.update(p)

        return result, self.behavior_set