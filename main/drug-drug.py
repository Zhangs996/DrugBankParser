# import xml.etree.ElementTree as ET
# root = ET.parse("C:/Users/zhangshuo/Desktop/database.xml").getroot()
# res = []
# for drug in root.iterfind("drug"):
# 	drug_id = drug.find("drugbank-id").text
# 	print(drug_id)
# 	interactions = drug.find("drug-interactions")
# 	for interaction in interactions.iterfind("drug-interaction"):
# 		another_id = interaction.find("drugbank-id").text
# 		print(drug_id,another_id)
# 		res.append((drug_id, another_id))
# with open("drug-drug-interaction.csv", "w+") as output_file:
# 	print("Drug1 \t Drug2", file=output_file)
# 	for record in res:
# 		print("{} \t {}".format(*record), file=output_file)

import xml.etree.ElementTree as ET
#root = ET.parse("test50.xml")
root = ET.parse("D:\zhuomian\知识图谱文档\CNN-LSTM\input\drugbank_all_full_database\database.xml").getroot()
res = []
for drug in root.iterfind('drug'):
	drug_id = drug.find('drugbank-id').text
	art_codes = drug.find('cas-number').text
	interactions = drug.find("targets")
	if interactions is None:
		continue
	if art_codes is None:
		continue
	for interaction in interactions.iterfind("target"):
		target_id = interaction.find("id").text
		res.append((drug_id,art_codes,target_id))
with open('drug-target-cas.txt','w+') as output_file:
	for record in res:
		print("{0}\t{1}\t{2}".format(*record),file=output_file)
#一个星（*）：表示接收的参数作为元组来处理
#两个星（**）：表示接收的参数作为字典来处理
'''
"{} {}".format("hello", "world")    # 不设置指定位置，按默认顺序
'hello world'
"{0} {1}".format("hello", "world")  # 设置指定位置
'hello world'
"{1} {0} {1}".format("hello", "world")  # 设置指定位置
'world hello world'
'''
# fg = [(1,2),('j','o')]
# for i in fg:
# 	print("{0}\t{1}".format(*i))