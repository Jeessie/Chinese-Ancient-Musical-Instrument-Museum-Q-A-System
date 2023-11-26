
"""
@desc:main函数，整合整个处理流程。
"""
# from mysite.settings import q_to_nql
from Museum_QA.code import query_to_nql
q_to_nql=query_to_nql.Nql(['D:/Museum-query/Museum_query_system/Museum_QA/code/dict/material_pos.txt',
                           'D:/Museum-query/Museum_query_system/Museum_QA/code/dict/museum_pos.txt',
                           'D:/Museum-query/Museum_query_system/Museum_QA/code/dict/exhibits_name_pos.txt',
                           'D:/Museum-query/Museum_query_system/Museum_QA/code/dict/person_pos.txt',
                            'D:/Museum-query/Museum_query_system/Museum_QA/code/dict/year_pos.txt'])

def query_function(question):
    while True:
        question = question
        # print(question.encode('utf-8'))
        # isinstance(question.encode('utf-8'))
        my_query = q_to_nql.get_nql(question.encode('utf-8'))
        # print(my_query)
        answer=[]
        if my_query is not None:
            result = my_query
            for i in range(len(result)):
                value = result[i]
                for v in value.values():
                    answer.append(v)
            return (answer)
        else:
            # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
            return '我还只是一个小程序，无法理解你的问题！！！'

        # print('#' * 100)

def get_img(question):
    while True:
        question = question
        # print(question.encode('utf-8'))
        # isinstance(question.encode('utf-8'))
        my_query = q_to_nql.get_nql(question.encode('utf-8'))
        # print(my_query)
        answer_list=[]
        if my_query is not None:
            result = my_query
            for i in range(len(result)):
                value = result[i]
                for v in value.values():
                    answer_list.append(v)
        img=[]
        dataFilePath = "D:/Museum-query/Museum_query_system/Museum_QA/static/txt/instrument.txt"
        # print(dataFilePath)
        with open(dataFilePath, 'r', encoding="utf-8") as finContent:
            for line in finContent:
                # print(1)
                if line.strip() == "":
                    # print(2)
                    continue
                items = line.strip().split("#")
                # print(items[0]+"<br />")
                for i in range(0,len(answer_list)):
                    if answer_list[i]==items[0]:
                        img.append("../../static/img/" + items[1])

        return img

def get_museum_img(question):
    while True:
        question = question
        # print(question.encode('utf-8'))
        # isinstance(question.encode('utf-8'))
        my_query = q_to_nql.get_nql(question.encode('utf-8'))
        # print(my_query)
        answer_list=[]
        if my_query is not None:
            result = my_query
            for i in range(len(result)):
                value = result[i]
                for v in value.values():
                    answer_list.append(v)
        img=[]
        dataFilePath = "D:/Museum-query/Museum_query_system/Museum_QA/static/txt/museum.txt"
        # print(dataFilePath)
        with open(dataFilePath, 'r', encoding="utf-8") as finContent:
            for line in finContent:
                # print(1)
                if line.strip() == "":
                    # print(2)
                    continue
                items = line.strip().split("#")
                # print(items[0]+"<br />")
                for i in range(0,len(answer_list)):
                    if answer_list[i]==items[0]:
                        img.append(items[1])
                        img.append("../../static/img/" + items[2])

        # print(rslt)夏莲居和哪个展品有关
        return img


if __name__ == '__main__':
    while True:
        question = input('请输入你的问题：')
        # print(question.encode('utf-8'))
        # isinstance(question.encode('utf-8'))
        print(query_function(question))
        print(get_img(question))
        print(get_museum_img(question))
        # question = input('请输入你的问题：')
        # # print(question.encode('utf-8'))
        # # isinstance(question.encode('utf-8'))
        # my_query = q_to_nql.get_nql(question.encode('utf-8'))
        # # print(my_query)
        # answer_list = []
        # if my_query is not None:
        #     result = my_query
        #     for i in range(len(result)):
        #         value = result[i]
        #         for v in value.values():
        #             print(v)
        #     img=get_img(question)
        #     museum=get_museum_img(question)
        #     print(img)
        #     print(museum)
        # else:
        #     print('I can\'t understand. :(')
        print('#' * 100)
# 中国国家博物馆的展品有什么
# 辨梦琴展出于哪个博物馆
