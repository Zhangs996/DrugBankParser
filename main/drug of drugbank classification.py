import xml.etree.ElementTree as ET
#root = ET.parse("test50.xml")
root = ET.parse("D:\zhuomian\知识图谱文档\CNN-LSTM\input\drugbank_all_full_database\database.xml").getroot()
small_molecule = []
biotech = []

for drug in root.iterfind("drug"):
    if drug is not None:
        drug_id = drug.find("drugbank-id").text
        if drug.attrib['type'] == 'small molecule':
            small_molecule.append(drug_id)
        if drug.attrib["type"] == "biotech":
            biotech.append(drug_id)
small_molecule_dti = []
biotech_dti = []
import pandas as pd
dti = pd.read_csv("D:\zhuomian\知识图谱文档\CNN-LSTM\input\dti\drugbank\drugbank-drug-target.txt",delimiter='\t',names=["drug","target"],encoding='utf-8')

for i in range(len(dti)):
    if dti.at[i,"drug"] in small_molecule:
        small_molecule_dti.append((dti.at[i,"drug"],dti.at[i,"target"]))
    if dti.at[i, "drug"] in biotech:
        biotech_dti.append((dti.at[i,"drug"],dti.at[i,"target"]))

with open("small_molecule_dti.txt",'w',encoding='utf-8') as f:
    for record in small_molecule_dti:
        print("{}\t{}".format(*record),file=f)
f.close()
with open("biotech_dti.txt",'w',encoding='utf-8') as f:
    for record in biotech_dti:
        print("{}\t{}".format(*record),file=f)
f.close()




        #state.add(drug_state)
# with open("small_molecule_drug.txt",'w',encoding='utf-8') as f:
#     for item in small_molecule:
#         print("{}".format(item),file=f)
# with open("biotech_drug.txt",'w',encoding='utf-8') as f:
#     for item in biotech:
#         print("{}".format(item),file=f)
# approved = set()
# experimental = set()
# illicit = set()
# nutraceutical = set()
# investigational = set()
# withdrawn = set()
#
# drug_dict = {}
# op = ["approved","experimental","illicit","investigational","nutraceutical","withdrawn"]
# for drug in root.iterfind("drug"):
#     drug_id = drug.find("drugbank-id").text
#     drug_group = []
#     groups = drug.find("groups")
#     for group in groups:
#         drug_group.append(group.text)
#     drug_dict[drug_id] = drug_group
#
# for key,value in drug_dict.items():
#     if "approved" in drug_dict[key]:
#         approved.add(key)
#     if "experimental" in drug_dict[key]:
#         experimental.add(key)
#     if "illicit" in drug_dict[key]:
#         illicit.add(key)
#     if "investigational" in drug_dict[key]:
#         investigational.add(key)
#     if "nutraceutical" in drug_dict[key]:
#         nutraceutical.add(key)
#     if "withdrawn" in drug_dict[key]:
#         withdrawn.add(key)
# # print('\n')
# # # print(experimental)
# # # print('\n')
# # # print(illicit)
# # # print('\n')
# # # print(investigational)
# # # print('\n')
# # # print(nutraceutical)
# # # print('\n')
# # # print(withdrawn)
# approved_dti = []
# experimental_dti = []
# illicit_dti = []
# investigational_dti = []
# nutraceutical_dti = []
# withdrawn_dti = []
# import pandas as pd
# dti = pd.read_csv("D:\zhuomian\知识图谱文档\CNN-LSTM\input\dti\drugbank\drugbank-drug-target.txt",delimiter='\t',names=["drug","target"],encoding='utf-8')
# print(dti.at[0,"drug"]+"adf"+dti.at[1,"drug"])
# for i in range(len(dti)):
#     if dti.at[i,"drug"] in approved:
#         approved_dti.append((dti.at[i,"drug"][:7],dti.at[i,"target"]))
#     if dti.at[i, "drug"] in experimental:
#         experimental_dti.append((dti.at[i,"drug"],dti.at[i,"target"]))
#     if dti.at[i, "drug"] in illicit:
#         illicit_dti.append((dti.at[i,"drug"],dti.at[i,"target"]))
#     if dti.at[i, "drug"] in investigational:
#         investigational_dti.append((dti.at[i,"drug"],dti.at[i,"target"]))
#     if dti.at[i, "drug"] in nutraceutical:
#         nutraceutical_dti.append((dti.at[i,"drug"],dti.at[i,"target"]))
#     if dti.at[i, "drug"] in withdrawn:
#         withdrawn_dti.append((dti.at[i,"drug"],dti.at[i,"target"]))
# print(approved_dti)
# with open("approved_dti.txt",'w',encoding='utf-8') as f:
#     for record in approved_dti:
#         print("{}\t{}".format(*record),file=f)
# f.close()
# with open("experimental_dti.txt",'w',encoding='utf-8') as f:
#     for record in experimental_dti:
#         print("{}\t{}".format(*record),file=f)
# f.close()
# with open("illicit_dti.txt",'w',encoding='utf-8') as f:
#     for record in illicit_dti:
#         print("{}\t{}".format(*record),file=f)
# f.close()
# with open("investigational_dti.txt",'w',encoding='utf-8') as f:
#     for record in investigational_dti:
#         print("{}\t{}".format(*record),file=f)
# f.close()
# with open("nutraceutical_dti.txt",'w',encoding='utf-8') as f:
#     for record in nutraceutical_dti:
#         print("{}\t{}".format(*record),file=f)
# f.close()
# with open("withdrawn_dti.txt",'w',encoding='utf-8') as f:
#     for record in approved_dti:
#         print("{}\t{}".format(*record),file=f)
# f.close()
#
#
#
#
#
#
# # lps = []
# # lps.append(approved)
# # lps.append(experimental)
# # lps.append(illicit)
# # lps.append(investigational)
# # lps.append(nutraceutical)
# # lps.append(withdrawn)
# # for i in range(len(op)):
# #     k = op[i] + ".txt"
# #     with open(k,'w',encoding="utf-8") as f:
# #         for j in lps[i]:
# #             print("{}".format(j),file = f)
# #     f.close()
