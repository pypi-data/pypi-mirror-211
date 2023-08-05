BehaviorTool是一个Python包，提供了CombinePattern、ContinuePattern和SequencePattern三个类的实现行为模式挖掘。

## 安装

你可以使用pip安装BahaviorPattern：

```
pip install BehaviorPattern
```

## 使用

在你的Python代码中引入类，例如：

```python
from BehaviorPattern. import CombinePattern, ContinuePattern, SequencePattern

#--------------------------------- 组合行为模式挖掘 ---------------------------------#
use_behavior = []
del_behavior = []
# 创建实例
behavior = CombinePattern.Generate(data=data, 
                                   use_behavior=use_behavior, 
                                   del_behavior=del_behavior, 
                                   min_support=0.1, 
                                   min_confidence=0.5, 
                                   min_length=3, 
                                   max_length=7, 
                                   sep='@') 
# 运行模型，返回pattern结果和使用的行为列表
combine, combine_use_behavior = behavior.run() 
# 筛选lift符合要求的pattern
combine_result = combine[combine['lift'] > 6] 


#--------------------------------- 连续行为模式挖掘 ---------------------------------#
use_behavior = []
del_behavior = []
# 创建实例
behavior = ContinuePattern.Generate(data=data, 
                                    use_behavior=use_behavior, 
                                    del_behavior=del_behavior, 
                                    min_support=0.1, 
                                    min_length=3, 
                                    max_length=6, 
                                    sep='@') 
# 运行模型，返回pattern结果和使用的行为列表
continues, continue_use_behavior = behavior.run() 
# 筛选lift符合要求的pattern
continues_result = continues[continues['lift'] > 6] 


#--------------------------------- 序列行为模式挖掘 ---------------------------------#
use_behavior = []
del_behavior = []
# 创建实例
behavior = SequencePattern.Generate(data=data, 
                                    use_behavior=use_behavior, 
                                    del_behavior=del_behavior, 
                                    min_support=0.1,
                                    min_length=3, 
                                    max_length=7, 
                                    sep='@') 
# 运行模型，返回pattern结果和使用的行为列表
sequence, seq_use_behavior = behavior.run() 
# 筛选lift符合要求的pattern
sequence_result = sequence[sequence['lift'] > 6] 
```

## 依赖

BehaviorPattern依赖以下Python库：

- numpy
- pandas
- efficient_apriori
- tqdm
- prefixspan

完整的依赖列表可以在setup.py中找到。

## 贡献

如果你发现任何bugs，请提交Issue或Pull Request进行更正

## 作者

BehaviorPattern由Chen Chen编写和维护。