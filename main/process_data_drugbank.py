#!/usr/bin/env python
# -*- coding:utf-8 -*-
# drugbank.txt: drugbank_id, name, state, description
# drugbank2.txt: drugbank_id1, drugbank_id2, drugbank_id2_name, interaction
# drugbank_d2d.txt: drugbank_id1, drugbank_id2
import lxml.etree as ET
from tqdm import tqdm
import numpy as np

drugbank_path = "../test50.xml"
drugbank = ET.parse(drugbank_path)
root = drugbank.getroot()
# nodes = root.xpath("//drugbank-id[@primary='true']")
# for node in nodes:
#     print(node.text)
# 表达式	        描述
# nodename	   选取已匹配节点下名为 nodename 的子元素节点
# /	           如果以 / 开头，表示从根节点作为选取起点。
# //	       在已匹配节点后代中选取节点，不考虑目标节点的位置。
# .	           选取当前节点
# ..	       选取当前节点的父元素节点。
# @	           选取属性。

# 通配符   	描述
# *     	匹配任何元素。
# @*    	匹配任何属性。
# node()	匹配任何类型的节点。
#预判是用来查找某个特定的节点或者符合某种条件的节点，预判表达式位于方括号中。
#https://blog.csdn.net/dengzhilong_cpp/article/details/51828672
ns = {'db': 'http://www.drugbank.ca'}
drug_content = []
drug_network = []

for drug in tqdm(root.xpath("db:drug[db:groups/db:group='approved']", namespaces=ns)):
    drugName = drug.find("db:name", ns).text
    drugbank_id = drug.find("db:drugbank-id[@primary='true']", ns).text
    drugDescription = drug.find("db:description", ns).text
    #\n匹配一个换行符#\r匹配一个回车符
    if drugDescription is not None:
        drugDescription = drugDescription.replace("\n", "")
        drugDescription = drugDescription.replace("\r", "")
    state = drug.find("db:state", ns)
    if state is not None:
        state = state.text
    else:
        state = "None"
    drug_interactions = drug.xpath("db:drug-interactions/db:drug-interaction", namespaces=ns)
    drug_content.append([drugbank_id, drugName, state, drugDescription])

    for t in drug_interactions:
        t_drugbank_id = t.find("db:drugbank-id", ns).text
        name = t.find("db:name", ns).text
        interaction = t.find("db:description", ns).text
        drug_network.append([drugbank_id, t_drugbank_id, name, interaction])
drug_content = np.array(drug_content, dtype=np.str)
drug_network = np.array(drug_network, dtype=np.str)

#drugbank.content: drugbank_id, name, state, description
np.savetxt("drugbank.txt", drug_content, fmt="%s", delimiter='  ', encoding="utf-8")
#drugbank2.txt: drugbank_id1, drugbank_id2, drugbank_id2_name, description
np.savetxt("drugbank2.txt", drug_network, fmt="%s", delimiter=' ', encoding="utf-8")
#drugbank_d2d.txt drugbank_id1, drugbank_id2
np.savetxt("drugbank_d2d.txt", drug_network[:, [0, 1]], fmt="%s", delimiter="   ", encoding="utf-8")
