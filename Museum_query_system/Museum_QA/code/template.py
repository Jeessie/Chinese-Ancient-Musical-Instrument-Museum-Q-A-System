from py2neo import *
from mysite.settings import graph
import json
from refo import finditer, Predicate, Star, Any, Disjunction
import re
import random


# graph = Graph('http://localhost:7474/', auth=("neo4j", "neo4j"))
# data = graph.run('MATCH (n:Person) RETURN n').data()
# result = json.loads(json.dumps(data, ensure_ascii = False))
# print(result)

class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        # 正则表达式
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        """
        采用正则表达式同时匹配对象（word）的字符（token）和词性（pos）
        """
        m1 = self.token.match(word.token.decode('utf-8'))
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = random.random()

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num


class QuestionSet:
    # def __init__(self):
    #    pass

    @staticmethod
    def material_of_exhibits_question(word_objects):
        """
         xx材质的展品有哪些？
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == material_pos:
                exp = u"MATCH(n:Exhibits{{`材质`:'{e}'}}) RETURN n.`名称`".format(e=w.token.decode('utf-8'))
                nql = graph.run(exp).data()
                break

        return nql
        # return json.loads(json.dumps(nql, ensure_ascii = False))

    @staticmethod
    def display_of_exhibits_question(word_objects):
        """
         xx展品展出于xx博物馆？
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == exhibits_pos:
                exp = u"Match (n:Exhibits{{`名称`:'{e}'}})-[:展出于]->(end:Museum) return end.`博物馆`".format(
                    e=w.token.decode('utf-8'))
                nql = graph.run(exp).data()
                break

        return nql


    @staticmethod
    def museum_have_ex_question(word_objects):
        """
         博物馆有哪些展品
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == museum_pos:
                exp = u"Match (n:Museum{{博物馆:'{e}'}})-[:`展出`]->(b:Exhibits) return b.`名称`".format(
                    e=w.token.decode('utf-8'))

                nql = graph.run(exp).data()
                break

        return nql

    @staticmethod
    def museum_address_question(word_objects):
        """
         博物馆在哪、地址
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == museum_pos:
                exp = u"Match (n:Museum{{博物馆:'{e}'}}) return n.`地址`".format(
                    e=w.token.decode('utf-8'))

                nql = graph.run(exp).data()
                break

        return nql

    @staticmethod
    def museum_description_question(word_objects):
        """
         博物馆简介
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == museum_pos:
                exp = u"Match (n:Museum{{博物馆:'{e}'}}) return n.`简介`".format(
                    e=w.token.decode('utf-8'))

                nql = graph.run(exp).data()
                break

        return nql
    # @staticmethod
    # def display_of_exhibits_question(word_objects):
    #     """
    #      xx展品）的展出于？
    #      :param word_objects:
    #      :return:
    #      """
    #
    #     nql = None
    #     for w in word_objects:
    #         if w.pos == exhibits_pos:
    #             exp = u"Match (n:Exhibits{{`名称`:'{e}'}})-[:展出于]->(end:Museum) return end.`博物馆`".format(
    #                 e=w.token.decode('utf-8'))
    #             nql = graph.run(exp).data()
    #             break
    #
    #     return nql

    @staticmethod
    def year_of_exhibits_question(word_objects):
        """
         xx展品的年代是什么？
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == exhibits_pos:
                exp = u"Match (n:Exhibits{{`名称`:'{e}'}}) return n.`年代`".format(e=w.token.decode('utf-8'))
                nql = graph.run(exp).data()
                break

        return nql

    @staticmethod
    def story_of_exhibits_question(word_objects):
        """
         xx展品）的历史背景故事是什么？
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == exhibits_pos:
                exp = u"Match (n:Exhibits{{`名称`:'{e}'}}) return n.`年代`,n.`背景`".format(e=w.token.decode('utf-8'))
                nql = graph.run(exp).data()
                break

        return nql

    @staticmethod
    def type_of_exhibits_question(word_objects):
        """
         xx展品）的种类是什么？
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == exhibits_pos:
                exp = u"Match (n:Exhibits{{`名称`:'{e}'}}) return n.`种类`".format(e=w.token.decode('utf-8'))
                nql = graph.run(exp).data()
                break

        return nql

    @staticmethod
    def sound_of_exhibits_question(word_objects):
        """
         xx展品）的音色是什么？
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == exhibits_pos:
                exp = u"Match (n:Exhibits{{`名称`:'{e}'}}) return n.`声音`".format(e=w.token.decode('utf-8'))
                nql = graph.run(exp).data()
                break

        return nql

    @staticmethod
    def make_of_exhibits_question(word_objects):
        """
         xx展品）的制造者是谁？
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == exhibits_pos:
                exp = u"Match (n:Exhibits{{名称:'{e}'}})-[:制造]->(a:Person) return a.`人物`".format(
                    e=w.token.decode('utf-8'))
                nql = graph.run(exp).data()
                break

        return nql

    @staticmethod
    def inscription_of_exhibits_question(word_objects):
        """
         xx展品）的题词人是什么？
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == exhibits_pos:
                exp = u"Match (n:Exhibits{{名称:'{e}'}})-[:题字]->(a:Person) return a.`人物`".format(
                    e=w.token.decode('utf-8'))
                nql = graph.run(exp).data()
                break

        return nql

    @staticmethod
    def person_of_exhibits_question(word_objects):
        """
         xx展品）和哪些人物相关？
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == exhibits_pos:
                exp = u"Match (n:Exhibits{{名称:'{e}'}})-[:制造]->(a:Person),(n)-[:`题字`]->(b:Person) return a.`人物`,b.`人物`".format(
                    e=w.token.decode('utf-8'))
                nql = graph.run(exp).data()
                break

        return nql


    @staticmethod
    def exhibits_of_person_question(word_objects):
        """
         xx人）和哪些展品相关？
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == person_pos:
                exp1 = u"Match (n:Person{{人物:'{e}'}})-[:`题字`]->(b:Exhibits) return b.`名称`".format(
                    e=w.token.decode('utf-8'))
                exp2 = u"Match (n:Person{{人物:'{e}'}})-[:制造]->(a:Exhibits)return a.`名称`".format(
                    e=w.token.decode('utf-8'))
                nql = graph.run(exp1).data() + graph.run(exp2).data()
                break

        return nql

    @staticmethod
    def person_inscription_ex_question(word_objects):
        """
         xx为什么展品题字了？
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == person_pos:
                exp = u"Match (n:Person{{人物:'{e}'}})-[:`题字`]->(b:Exhibits) return b.`名称`".format(
                    e=w.token.decode('utf-8'))

                nql = graph.run(exp).data()
                break

        return nql

    @staticmethod
    def person_make_ex_question(word_objects):
        """
         xx制造了什么展品？
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == person_pos:
                exp = u"Match (n:Person{{人物:'{e}'}})-[:`制造`]->(b:Exhibits) return b.`名称`".format(
                    e=w.token.decode('utf-8'))

                nql = graph.run(exp).data()
                break

        return nql

    @staticmethod
    def person_whatword_question(word_objects):
        """
         xx题了什么字
         :param word_objects:
         :return:
         """

        nql = None
        for w in word_objects:
            if w.pos == person_pos:
                exp = u"Match (n:Person{{人物:'{e}'}})-[r:`题字`]->(b:Exhibits) return r.property".format(
                    e=w.token.decode('utf-8'))

                nql = graph.run(exp).data()
                break

        return nql




# xx材质的展品有哪些？
exhibits_pos = "ne"
material_pos = "nm"
museum_pos="nmuseum"
person_pos="np"
exhibits_entity = (W(pos=exhibits_pos))
material_entity = (W(pos=material_pos))
person_entity=(W(pos=person_pos))
museum_entity=(W(pos=museum_pos))

# material_keyword = (W('材质'))
# have_keyword = (W('有哪些'))
# what_keyword=(W('是什么')|W('是谁')|W('怎么样'))


#xx材质的展品有哪些
exhibits_keyword=(W('展品'))

#xx博物馆有哪些展品
# exhibits_keyword=(W('展品'))
#xx博物馆的地址/在哪里
address_keyword=(W('地址')|W('在哪'))
#xx博物馆的介绍
description_keyword=(W('介绍')|W('简介'))


#xx为什么展品题字了？
inscription_keyword=(W('题词')|W('题字'))
#（人）和哪个展品有关？
about_keyword=(W('有关')|W('相关')|W('关系'))
#xx制造了什么展品？
make_keyword=(W('制造者')|W('创造')|W('制成')|W('制造人'))
#xx题了什么字？
whatword_keyword=(W('什么字'))

#（展品）的展出于？
display_keyword = (W('展出') | W('博物馆'))
#（展品）的年代是什么？
year_keyword = (W('年代'))
#（展品）的历史背景故事是什么？
story_keyword=(W('故事')|W('历史背景')|W('历史'))
#（展品）的种类是什么？
type_keyword=(W('种类')|W('分类')|W('类别'))
#（展品）的音色是什么？
sound_keyword=(W('音色')|W('声音')|W('听起来'))
#（展品）的制造者是谁？
# make_keyword=(W('制造者')|W('创造')|W('制成'))
#（展品）的题词人是谁？
# inscription_keyword1=(W('题词人')|W('题字人'))
#（展品）和哪些人物相关？
person_keyword=(W('人物')|W('人'))







rules=[
#（展品）和哪些人物相关？
    Rule(condition_num=2,condition=exhibits_entity+ Star(Any(), greedy=False) +person_keyword+ Star(Any(),greedy=False),action=QuestionSet.person_of_exhibits_question),
#（展品）的题词人是谁？
    Rule(condition_num=2, condition=exhibits_entity + Star(Any(), greedy=False) + inscription_keyword + Star(Any(),greedy=False) , action=QuestionSet.inscription_of_exhibits_question),
# （展品）的制造者是谁？
    Rule(condition_num=2, condition=exhibits_entity + Star(Any(), greedy=False) + make_keyword + Star(Any(),greedy=False) , action=QuestionSet.make_of_exhibits_question),
# （展品）的音色是什么？
    Rule(condition_num=2, condition=exhibits_entity + Star(Any(), greedy=False) + sound_keyword + Star(Any(),greedy=False) , action=QuestionSet.sound_of_exhibits_question),
#（展品）的种类是什么？
    Rule(condition_num=2, condition=exhibits_entity + Star(Any(), greedy=False) + type_keyword + Star(Any(),greedy=False), action=QuestionSet.type_of_exhibits_question),
#（展品）的历史背景故事是什么？
    Rule(condition_num=2, condition=exhibits_entity + Star(Any(), greedy=False) + story_keyword + Star(Any(),greedy=False), action=QuestionSet.story_of_exhibits_question),
#（展品）的年代是什么？
    Rule(condition_num=2,condition=exhibits_entity + Star(Any(),greedy=False) + year_keyword +Star(Any(),greedy=False),action=QuestionSet.year_of_exhibits_question),
#（展品）的展出于？
    Rule(condition_num=2,condition=exhibits_entity + Star(Any(), greedy=False) + display_keyword + Star(Any(), greedy=False),action=QuestionSet.display_of_exhibits_question),

# （人）和哪个展品有关？
    Rule(condition_num=2,condition=person_entity+ Star(Any(), greedy=False)+about_keyword+ Star(Any(),greedy=False),action=QuestionSet.exhibits_of_person_question),
#xx为什么展品题字了？
    Rule(condition_num=3,condition=person_entity + Star(Any(),greedy=False) + inscription_keyword +Star(Any(),greedy=False),action=QuestionSet.person_inscription_ex_question),
#xx制造了什么展品？
    Rule(condition_num=3,condition=person_entity + Star(Any(),greedy=False) + make_keyword +Star(Any(),greedy=False),action=QuestionSet.person_make_ex_question),
#xx题了什么字？
    Rule(condition_num=3,condition=person_entity + Star(Any(),greedy=False) + whatword_keyword +Star(Any(),greedy=False),action=QuestionSet.person_whatword_question),

#xx博物馆有哪些展品
    Rule(condition_num=3,condition=museum_entity + Star(Any(),greedy=False) + exhibits_keyword +Star(Any(),greedy=False),action=QuestionSet.museum_have_ex_question),
#xx博物馆的地址/在哪里
    Rule(condition_num=3,condition=museum_entity + Star(Any(), greedy=False) + address_keyword + Star(Any(), greedy=False),action=QuestionSet.museum_address_question),
#xx博物馆的介绍/简介
    Rule(condition_num=3,condition=museum_entity + Star(Any(), greedy=False) + description_keyword + Star(Any(), greedy=False),action=QuestionSet.museum_description_question),

#xx材质的展品有哪些
    Rule(condition_num=3,condition=material_entity + Star(Any(),greedy=False) +exhibits_keyword+ Star(Any(),greedy=False),action=QuestionSet.material_of_exhibits_question),

       ]

