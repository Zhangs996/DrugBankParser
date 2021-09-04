import pandas as pd
import json
Enzyme = pd.read_csv('Enzyme.csv',delimiter=',')
with open('target-uniprot.json') as drug_uniprot_json:
    drug_uniprot = json.load(drug_uniprot_json)
with open('h2u.json') as h2u_json:
    h2u = json.load(h2u_json)
with open('kegg-drugbank.json') as kd:
    kd = json.load(kd)
# print(Enzyme.head())
# print(drug_uniprot,h2u)
print(len(drug_uniprot))
Enzyme.replace('\s+', '', regex=True, inplace=True)
for i in range(len(Enzyme)):
    if Enzyme.at[i,'protein'] in h2u:
        up = h2u[Enzyme.at[i,'protein']]
        up = up.replace(" ",'')
        if up in drug_uniprot:
            BE = drug_uniprot[up]
            Enzyme.at[i, 'protein'] = BE
        else:
            #print(up)
            continue
    else:
        print(Enzyme.at[i,'protein'])
        continue
#print(Enzyme)
new = Enzyme.drop(Enzyme[Enzyme['protein'].str.contains('hsa')].index)

new = new.reset_index(drop=True)
print(new)
for i in range(len(new)):
    if new.at[i,'drug'] in kd:
        print(new.at[i,'drug'])
        new.at[i,'drug'] = kd[new.at[i, 'drug']]
print(new)
index_list = []
for i in range(len(new)):
    if new.at[i,'drug'].startswith('DB'):
        continue
    else:
        index_list.append(i)
new.drop(labels=index_list,axis=0,inplace=True)
new = new.reset_index(drop=True)
print(new)

new.to_csv('drug-uniprot.txt',encoding='utf-8',sep='\t',index=False)
