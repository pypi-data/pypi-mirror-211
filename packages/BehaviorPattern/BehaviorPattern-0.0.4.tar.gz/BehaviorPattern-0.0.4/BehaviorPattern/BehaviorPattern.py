import numpy as np 
import pandas as pd 
from efficient_apriori import apriori 
from prefixspan import PrefixSpan 
from tqdm import tqdm 
import warnings 
warnings.filterwarnings('ignore') 
tqdm.pandas() 

class DataClass:
    def data_preprocess(self, data, use_behavior, del_behavior, sep):
        """
        data: DataFrame, 包含用户行为序列和标签的数据集
        use_behavior: list, 需要使用的行为列表
        """
        data_black, data_white = data[data['label'] == 1], data[data['label'] == 0]
        black_behavior, white_behavior = data_black['action_sequence'], data_white['action_sequence']
        black_behavior = black_behavior.apply(lambda x: x.split(sep)[1::2]).to_list()
        white_behavior = white_behavior.apply(lambda x: x.split(sep)[1::2]).to_list()
        if len(use_behavior) > 0:
            black_behavior = [self.use_behavior_tool(x, use_behavior, del_behavior) for x in black_behavior]
            white_behavior = [self.use_behavior_tool(x, use_behavior, del_behavior) for x in white_behavior]
        elif len(del_behavior) > 0:
            black_behavior = [self.del_behavior_tool(x, del_behavior) for x in black_behavior]
            white_behavior = [self.del_behavior_tool(x, del_behavior) for x in white_behavior]
        else:
            pass
        return black_behavior, white_behavior
    
    def data_preprocess_2(self, data, use_behavior, del_behavior, sep):
        """
        data: DataFrame, 包含用户行为序列和标签的数据集
        use_behavior: list, 需要使用的行为列表
        """
        data_black, data_white = data[data['label'] == 1], data[data['label'] == 0]
        data_black['action_sequence'] = data_black['action_sequence'].apply(lambda x: x.split(sep)[1::2]).to_list()
        data_white['action_sequence'] = data_white['action_sequence'].apply(lambda x: x.split(sep)[1::2]).to_list()
        if len(use_behavior) > 0:
            data_black['action_sequence'] = data_black['action_sequence'].apply(self.use_behavior_tool, args=(use_behavior,del_behavior,))
            data_white['action_sequence'] = data_white['action_sequence'].apply(self.use_behavior_tool, args=(use_behavior,del_behavior,))
        elif len(del_behavior) > 0:
            data_black['action_sequence'] = data_black['action_sequence'].apply(self.del_behavior_tool, args=(del_behavior,))
            data_white['action_sequence'] = data_white['action_sequence'].apply(self.del_behavior_tool, args=(del_behavior,))
        else:
            pass
        return data_black, data_white
    
    def del_behavior_tool(self, lst, del_behavior):
        return [x for x in lst if x not in del_behavior]
    
    def use_behavior_tool(self, lst, use_behavior, del_behavior):
        return [x for x in lst if x in use_behavior and x not in del_behavior]
    
class CombinePattern(DataClass):
    def __init__(self, data, use_behavior=[], del_behavior = [], min_support=0.2, min_confidence=0.5, min_length=3, max_length=6, sep = '@'):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.min_length = min_length
        self.max_length = max_length
        self.behavior_set = set()
        self.black_behavior, self.white_behavior = self.data_preprocess(data, use_behavior, del_behavior, sep)

    def isin_behavior(self, com, behavior):
        return set(com).issubset(set(behavior))

    def remove_sublists(self, lists):
        result = []
        for l in lists:
            if not any(set(l).issubset(set(x)) for x in lists if x != l):
                result.append(l)
        return result
        
    def run(self, lift=2):
        itemsets, rules = apriori(self.black_behavior,
                                  min_support=self.min_support,
                                  min_confidence=self.min_confidence,
                                  max_length=self.max_length,
                                  output_transaction_ids=True,
                                  )
        
        black_temp = []
        for i in range(self.min_length, self.max_length + 1):
            try:
                now = itemsets[i]
                temp = []
                for k in now.keys():
                    n = now[k].itemset_count
                    m = now[k].members
                    temp.append([i, k, n, m])
                black_temp = black_temp + temp
            except:
                pass

        use_pattern = self.remove_sublists(list(np.array(black_temp)[:,1]))
        white_count = []
        for com in tqdm(use_pattern):
            count = np.sum([set(com).issubset(set(behavior)) for behavior in self.white_behavior])
            white_count.append(count)
        
        result = pd.DataFrame(black_temp, columns = ['patten_len', 'patten', 'hit_black_count', 'black_user_set'])
        result = result[result['patten'].isin(use_pattern)]
        result['hit_white_count'] = white_count
        result['patten_black_retio'] = result['hit_black_count'] / (result['hit_white_count'] + result['hit_black_count'])
        result['data_black_retio'] = len(self.black_behavior) / (len(self.black_behavior) + len(self.white_behavior))
        result['lift'] = result['patten_black_retio'] / result['data_black_retio']
        result = result.sort_values(by = ['lift'], ascending=False).reset_index(drop = True)

        result.insert(0, 'id', 'combine_pattern_' + result.index.astype(str))
        result = result[['id', 'patten', 'patten_len', 'patten_black_retio', 'data_black_retio', 'lift', 'hit_black_count', 'hit_white_count']]
        result['patten'] = result['patten'].apply(list)

        for p in result['patten']:
            self.behavior_set.update(p)

        return result, self.behavior_set

class ContinuePattern(DataClass):
    def __init__(self, data, use_behavior=[], del_behavior=[], min_support=0.1, min_length=3, max_length=6, sep = '@'):
        """
        data: DataFrame, 包含用户行为序列和标签的数据集
        use_behavior: list, 需要使用的行为列表，默认为空
        min_support: float, 最小支持度，默认为0.05
        """
        self.min_support = min_support
        self.min_length = min_length
        self.max_length = max_length
        self.behavior_set = set()
        self.data_black, self.data_white = self.data_preprocess_2(data, use_behavior, del_behavior, sep)
    
    def isin_behavior(self, com, behavior):
        if len(com) > len(behavior):
            return False
        else:
            return ' '.join(com) in ' '.join(behavior)

    def ngram(self, b, n):
        """
        b: list, 行为列表
        n: int, n-gram中的n
        """
        lst = []
        for m in range(1, n+1):
            for i in range(len(b)-m+1):
                lst.extend(['->'.join(b[i:i+m])])
        return '; '.join(lst)

    def isin_behavior(self, com, behavior):
        if len(com) > len(behavior):
            return False
        else:
            return ' '.join(com) in ' '.join(behavior)
    
    def run(self):
        """
        lift: float, 最小提升度，默认为2
        """
        self.data_black['key'] = list(range(len(self.data_black)))
        self.data_black['action_sequence'] = self.data_black['action_sequence'].apply(lambda x: self.ngram(x, self.max_length))
        result = self.data_black.set_index(['key'])["action_sequence"].str.split('; ', expand=True).stack()
        result = result.reset_index(drop=True,level=-1).reset_index().rename(columns={0:'patten'})
        result = result.groupby(['patten']).agg({'key': pd.Series.nunique}).reset_index()
        result.columns=['patten','hit_black_count']

        result['black_retio'] = result['hit_black_count'] / len(self.data_black)
        result['patten_use'] = result['patten'].apply(lambda x: x.split('->'))
        result['patten_len'] = result['patten_use'].apply(lambda x: len(x))

        result = result[result['black_retio'] >= self.min_support]
        result = result[result['patten_len'] >= self.min_length]

        white_behavior = self.data_white['action_sequence'].tolist()
        white_count = [sum(self.isin_behavior(com, b) for b in white_behavior) for com in tqdm(result['patten_use'])]
        
        result['hit_white_count'] = white_count
        result['white_retio'] = result['hit_white_count'] / len(self.data_white)
        result['patten_black_retio'] = result['hit_black_count'] / (result['hit_white_count'] + result['hit_black_count'])
        result['data_black_retio'] = len(self.data_black) / (len(self.data_black) + len(self.data_white))
        result['lift'] = result['patten_black_retio'] / result['data_black_retio']
        result = result[['patten', 'patten_len', 'patten_black_retio', 'data_black_retio', 'lift', 'hit_black_count', 'hit_white_count']]
        result = result.sort_values(by = ['lift'], ascending=False).reset_index(drop=True)
        result.insert(0, 'id', 'combine_pattern_' + result.index.astype(str))
        
        for p in result['patten']:
            self.behavior_set.update(p.split('->'))

        return result, self.behavior_set

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