import numpy as np 
import pandas as pd 
from efficient_apriori import apriori 
from tqdm import tqdm 
import warnings 
from dataclass import DataClass
warnings.filterwarnings('ignore') 
tqdm.pandas() 

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