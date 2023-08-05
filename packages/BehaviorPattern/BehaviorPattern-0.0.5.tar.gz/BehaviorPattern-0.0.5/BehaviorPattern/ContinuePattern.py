import numpy as np 
import pandas as pd 
from tqdm import tqdm 
import warnings 
from DataClass import DataClass
warnings.filterwarnings('ignore') 
tqdm.pandas() 

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