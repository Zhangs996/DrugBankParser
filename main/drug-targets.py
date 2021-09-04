# from xml.dom import minidom
# # doc = minidom.parse("C:/Users/zhangshuo/Desktop/知识图谱/基于知识图谱嵌入和卷积- lstm网络的药物-药物相互作用预测/Drug-Drug-Interaction-Prediction-master/data/drugbank_all_full_database/drugbank.xml")
# # items = doc.getElementsByTagName('drug-interaction')
# # print(len(items))
# # print('\nAll attributes:')
# # i = 0
# # for elem in items:
# #     i = i+1
# # print(i)
import pandas as pd

# df = pd.read_csv('C:/Users/zhangshuo/Desktop/知识图谱/基于知识图谱嵌入和卷积- lstm网络的药物-药物相互作用预测/Drug-Drug-Interaction-Prediction-master/data/drugbank_all_full_database/twosides_every20_first1500.tsv',sep='\t')
# print(df.count())
# length = len(df[['drug1', 'drug2']])
# print(length)
# print(len(df.groupby(['drug1', 'drug2'])))
#
# groupedDf = df.groupby(['drug1', 'drug2'])
# groupedDf.sum().reset_index().to_csv('Twosides_interactions.tsv',sep='\t')
from lxml import etree
import xml.etree.ElementTree as ET

root = ET.parse("D:\zhuomian\知识图谱文档\CNN-LSTM\input\drugbank_all_full_database\database.xml").getroot()

res = []
for drug in root.iterfind("drug"):
	drug_id = drug.find("drugbank-id").text
	print(drug_id)
	interactions = drug.find("targets")
	for interaction in interactions.iterfind("target"):
		target_id = interaction.find("id").text
		print(drug_id,target_id)
		res.append((drug_id, target_id))
with open("drug-target.txt", "w+") as output_file:
	print("Drug1\ttarget", file=output_file)
	for record in res:
		print("{}\t{}".format(*record), file=output_file)#https://www.cnblogs.com/qiaoxin/p/10109877.html



