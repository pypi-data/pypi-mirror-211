import numpy as np 
import pandas as pd 
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