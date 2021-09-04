import xml.etree.ElementTree as ET

root = ET.parse('D:\zhuomian\知识图谱文档\CNN-LSTM\input\drugbank_all_full_database\database.xml').getroot()
#root = ET.parse('test50.xml').getroot()
res = []
sou = {}
import json
for drug in root.iterfind("drug"):
    drug_id = drug.find("drugbank-id").text
    drug_group = []
    groups = drug.find("groups")
    for group in groups:
        drug_group.append(group.text)
    print(drug_id)
    if "approved" in drug_group:
        interactions = drug.find("targets")
        for interaction in interactions.iterfind("target"):
            target_id = interaction.find("id").text
            polypeptide_id = interaction.find("polypeptide")
            if polypeptide_id is None:
                polypeptide_id = target_id
            else:
                polypeptide_id = polypeptide_id.attrib['id']
                print(polypeptide_id)
                res.append((drug_id, polypeptide_id))
with open("approved-uniprot.txt", "w+") as output_file:
	print("drug"+'\t'+"uniprot", file=output_file)
	for record in res:
		print("{} \t {}".format(*record), file=output_file)