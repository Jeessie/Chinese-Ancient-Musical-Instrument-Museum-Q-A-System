# Chinese-Ancient-Musical-Instrument-Museum-Q-A-System
Developed using Django, the System serves as an online Museum, broadening understanding of traditional instruments. It utilizes Neo4j to store data and employs template matching for natural language queries, allowing administrators to manage data conveniently through login for operations

# Environment
* python3.6-3.8
* neo4j community 3.5
* jieba, py2neo 4.3.0,
* Django，Web应用框架，用于交互展示
      
# 主要文件夹功能说明
Museum_query_system 程序主文件夹
* Museum_QA 主要包含前后端交互的接口设置，问句分析的代码，以及分词需要的外部词典的导入
  * code 问答系统后端的主文件
    * jieba_split.py 处理问句、分词标注词性等
    * template.py 处理问句模板
    * query_to_nql.py 进行语义解析，找到匹配的模板，返回对应的nql查询语句
    * main.py 对问句解析的整合和返回结果的处理
    * dict1.py 对可视化的数据库增删改查操作
  * templates 前端网页的格式排版 
  * view.py 前端网页的接口
* mysite-settings 设置django和数据库和前端网页的连接

# 项目运行
* 运行Museum_query_system文件夹中的main.py，开启命令行模式。
```
python
python main.py
```
* 在项目根目录下运行manage.py,开启项目的web模式
```
python manage.py runserver
```
