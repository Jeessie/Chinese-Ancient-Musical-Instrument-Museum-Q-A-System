# encoding=utf-8

"""
@desc: 将自然语言转为neo4j查询语句
"""

from Museum_QA.code import template
from Museum_QA.code import jieba_split


class Nql:
    def __init__(self, dict_paths):
        self.tw = jieba_split.Tagger(dict_paths)
        self.rules = template.rules

    def get_nql(self, question):
        """
        进行语义解析，找到匹配的模板，返回对应的nql查询语句
        :param question:
        :return:
        """
        word_objects = self.tw.get_word_objects(question)
        queries_dict = dict()

        for rule in self.rules:
            # word_objects是一个列表，元素为是包含词语和词语对应词性的对象
            query, num = rule.apply(word_objects)

            if query is not None:
                queries_dict[num] = query

        if len(queries_dict) == 0:
            return None
        elif len(queries_dict) == 1:
            return list(queries_dict.values())[0]
        else:
            # TODO 匹配多个语句，以匹配关键词最多的句子作为返回结果
            sorted_dict = sorted(queries_dict.items(), key=lambda item: item[1])
            return sorted_dict[0][1]

if __name__ == '__main__':
    q_s = Nql(['dict/material_pos.txt', 'dict/museum_pos.txt', 'dict/exhibits_name_pos.txt', 'dict/person_pos.txt',
               'dict/year_pos.txt','dict/history_pos.txt'])
    # question = '漆木材质的展品有哪些'
    question = '辨梦琴展出于哪个博物馆？'
    # question = '漆木材质的展品有哪些'
    # question='山东省博物馆有哪些展品'
    # question='夏莲居为什么展品题字了'
    # question='石峁口簧的年代是什么？'
    # question='铜钹的历史背景故事是什么'
    # question = '铜钹的种类是什么'
    # question = '铜钹的音色是什么'
    # question = '铜钹的制造者是谁'
    # question='混沌材琴的题词人是谁'
    # question='混沌材琴和哪些人有关'

    my_query = q_s.get_nql(question)
    print(my_query)
