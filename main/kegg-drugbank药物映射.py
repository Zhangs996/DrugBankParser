from xml.etree import ElementTree as ET
import json
root = ET.parse("D:\zhuomian\知识图谱文档\CNN-LSTM\input\drugbank_all_full_database\database.xml").getroot()
res = []
tu = {}
for drug in root.iterfind('drug'):
    drug_id = drug.find('drugbank-id').text
    interactions = drug.find('external-identifiers')
    for interaction in interactions.iterfind('external-identifier'):
        resource = interaction.find("resource").text
        identifier = interaction.find("identifier").text
        if resource != "KEGG Drug":
            continue
        else:
            res.append((identifier,drug_id))
            tu[identifier] = drug_id
with open('kegg-drugbank.txt','w',encoding='utf-8') as f:
    print("kegg"+'\t'+'drugbank',file=f)
    for record in res:
        print("{}\t{}".format(*record), file=f)
dk = {value:key for key,value in tu.items()}
with open('kegg-drugbank.json','w',encoding='utf-8') as di:
    json.dump(dk,di)