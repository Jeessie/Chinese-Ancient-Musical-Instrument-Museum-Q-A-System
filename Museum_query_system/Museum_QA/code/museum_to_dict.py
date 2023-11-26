import json
path_r="lib_data.json"
path_w="sound_pos.txt"
# path="test.json"
with open(path_r,'r',encoding='utf=8')as fr:
    row_data=json.load(fr)
    data=[]
    data.append(row_data)
# print(data[0])
total_values = []
for d in data[0]:
   # print(d.get('人物'))
   if(d.get('声音')!=None):
       total_values.append(d['声音'])

f=open(path_w,'w',encoding='utf-8')
for i in total_values:
    f.write(i + ' ns' + '\n')