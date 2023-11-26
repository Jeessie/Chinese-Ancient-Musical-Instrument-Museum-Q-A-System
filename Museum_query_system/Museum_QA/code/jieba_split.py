#对问句进行分词“漆木的展品都有哪些？”
"""

@desc: 定义Word类的结构；定义Tagger类，实现自然语言转为Word对象的方法。

"""

import jieba
import jieba.posseg as pseg


class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos


class Tagger:
    def __init__(self, dict_paths):
        # TODO 加载外部词典
        for p in dict_paths:
            jieba.load_userdict(p)

        # TODO jieba不能正确切分的词语，我们人工调整其频率。
        jieba.suggest_freq('有哪些',True)
        jieba.suggest_freq('漆木', True)
        # jieba.suggest_freq('材质', True)
        jieba.suggest_freq('是谁', True)
        jieba.suggest_freq('是什么', True)
        jieba.suggest_freq('什么字', True)
        jieba.suggest_freq('漆木', True)

    @staticmethod
    def get_word_objects(sentence):
        # type: (str) -> list
        """
        把自然语言转为Word对象
        :param sentence:
        :return:
        """
        return [Word(word.encode('utf-8'), tag) for word, tag in pseg.cut(sentence)]

# TODO 用于测试
if __name__ == '__main__':
    tagger = Tagger(['dict/material_pos.txt', 'dict/museum_pos.txt', 'dict/exhibits_name_pos.txt', 'dict/person_pos.txt',
               'dict/year_pos.txt'])
    #while True:
    s = '混沌材琴的题词人是谁'
    # s = '辨梦琴展出于哪个博物馆？'
    for i in tagger.get_word_objects(s):
        print(i.token.decode('utf-8'), i.pos)