from idna import unicode
from lxml import etree
from io import StringIO
from collections import defaultdict
import csv

# Parse XML
# f = open('C:/Users/zhangshuo/Desktop/full database.xml','r')
# data = f.read()
# #data = bytes(bytearray(data, encoding = 'utf-8'))
# f.close()

# tree = etree.parse('test19.xml')
# context = etree.iterparse('test19.xml')

tree = etree.parse('C:/Users/zhangshuo/Desktop/database.xml')
#tree = etree.parse('test19.xml')
context = etree.iterparse('C:/Users/zhangshuo/Desktop/database.xml')
#context = etree.iterparse('test19.xml')

root = tree.getroot()#这个得到的根节点应该是<drug>标签
print (len(root), 'drugs')


#######################################################################
# Iterate over drugs
drug2attrib = defaultdict(dict)
# drugbank_id -> {'drugname', 'drug_type', 'groups', 'targets/enzymes/transporters': [_id, _actions]}

target2attrib = defaultdict(dict)
enzyme2attrib = defaultdict(dict)
transporter2attrib = defaultdict(dict)
#print(transporter2attrib)#defaultdict(<class 'dict'>, {})
# drugbank_target_id -> {'gene', 'name', 'organism', 'taxonomy_id', 'uniprot_id', 'genbank_gene_id', 'genbank_protein_id', 'hgnc_id'}

# = '{http://www.drugbank.ca}'新版本应该没有这个东西了

#child是<drug>对象，在总文件夹有上万种药物对象
for child in root:
    #print(child)
    for s in child.findall('drugbank-id'):
        #s.attrib是<drugbank-id>的属性，比如primary是其中的一个属性
        if 'primary' in s.attrib:
            drugbank_id = s.text
    drugname = child.findall('name')[0].text
    drug2attrib[drugbank_id]['drug-id'] = drugbank_id
    drug2attrib[drugbank_id]['drugname'] = drugname
    #print(drug2attrib[drugbank_id])#{'drugname': 'Cetuximab'}
    #给每种药物添加药物的类别（生物技术）
    drug_type = child.attrib['type']
    drug2attrib[drugbank_id]['drug_type'] = drug_type
    #print(drug2attrib[drugbank_id])#{'drugname': 'Cetuximab', 'drug_type': 'biotech'}
    #给每种药物添加组别（approved是已批准的药物）
    groups = [s.text for s in child.find('groups').findall('group')]
    drug2attrib[drugbank_id]['groups'] = groups
    #print(drug2attrib[drugbank_id])#{'drugname': 'Cetuximab', 'drug_type': 'biotech', 'groups': ['approved']}
    # Get targets
    drug2attrib[drugbank_id]['targets'] = []
    for target in child.find('targets').findall('target'):
        if target.find('polypeptide') is None:
            target_id = target.find('id').text
            target_name = target.find('name').text
            drug2attrib[drugbank_id]['targets'].append(target_id)
             # continue
        else:
            target_id = target.find('id').text
            target_gene = target.find('polypeptide').find('gene-name').text
            target_name = target.find('name').text
            target_organism = target.find('organism').text
            target_taxonomy_id = target.find('polypeptide').find('organism').attrib['ncbi-taxonomy-id']

            if target_organism is None and target_taxonomy_id == '9606':
                target_organism = 'Humans'
            if target_organism == 'Humans' and target_taxonomy_id == '':
                target_taxonomy_id = '9606'
            if target_organism == 'Homo sapiens':
                target_organism = 'Humans'
            if target_gene is None or target_organism is None or target_taxonomy_id is None:
                continue

            target_external_ids = target.find('polypeptide').find('external-identifiers').findall('external-identifier')
            target_uniprot_id = ''
            target_genbank_gene = ''
            target_genbank_protein = ''
            target_hgnc_id = ''

            for external_id in target_external_ids:
                if external_id.find('resource').text == 'UniProtKB':
                    target_uniprot_id = external_id.find('identifier').text
                elif external_id.find('resource').text == 'GenBank Gene Database':
                    target_genbank_gene = external_id.find('identifier').text
                elif external_id.find('resource').text == 'GenBank Protein Database':
                    target_genbank_protein = external_id.find('identifier').text
                elif external_id.find('resource').text == 'HUGO Gene Nomenclature Committee (HGNC)':
                    target_hgnc_id = external_id.find('identifier').text

            target_actions = [s.text.lower() for s in target.find('actions').findall('action')]

            drug2attrib[drugbank_id]['targets'].append(target_id)
            #drug2attrib[drugbank_id]['targets'].append((target_id, target_actions))

    print(drug2attrib[drugbank_id])

        #关于targets的一些信息
        # if target_id not in target2attrib:  # {'gene', 'name', 'organism', 'taxonomy_id', 'uniprot_id', 'genbank_gene_id', 'genbank_protein_id', 'hgnc_id'}
        #     target2attrib[target_id]['gene'] = target_gene
        #     target2attrib[target_id]['name'] = target_name
        #     target2attrib[target_id]['organism'] = target_organism
        #     target2attrib[target_id]['taxonomy_id'] = target_taxonomy_id
        #
        #     target2attrib[target_id]['uniprot_id'] = target_uniprot_id
        #     target2attrib[target_id]['genbank_gene_id'] = target_genbank_gene
        #     target2attrib[target_id]['genbank_protein_id'] = target_genbank_protein
        #     target2attrib[target_id]['hgnc_id'] = target_hgnc_id
        #
        # print(target2attrib)

        # print target_id, target_gene, target_name, target_organism, target_taxonomy_id, target_actions

    # Get enzymes
    drug2attrib[drugbank_id]['enzymes'] = []
    for enzyme in child.find('enzymes').findall('enzyme'):
        if enzyme.find('polypeptide') is None:
            continue
        else:
            enzyme_id = enzyme.find('id').text
            enzyme_gene = enzyme.find('polypeptide').find('gene-name').text
            enzyme_name = enzyme.find('name').text
            enzyme_organism = enzyme.find('organism').text
            enzyme_taxonomy_id = enzyme.find('polypeptide').find('organism').attrib['ncbi-taxonomy-id']

            if enzyme_organism is None and enzyme_taxonomy_id == '9606':
                enzyme_organism = 'Human'
            if enzyme_organism == 'Human' and enzyme_taxonomy_id == '':
                enzyme_taxonomy_id = '9606'
            if enzyme_organism == 'Homo sapiens':
                enzyme_organism = 'Human'
            if enzyme_gene is None or enzyme_organism is None or enzyme_taxonomy_id is None:
                continue

            enzyme_external_ids = enzyme.find('polypeptide').find('external-identifiers').findall('external-identifier')
            enzyme_uniprot_id = ''
            enzyme_genbank_gene = ''
            enzyme_genbank_protein = ''
            enzyme_hgnc_id = ''

            for external_id in enzyme_external_ids:
                if external_id.find('resource').text == 'UniProtKB':
                    enzyme_uniprot_id = external_id.find('identifier').text
                elif external_id.find('resource').text == 'GenBank Gene Database':
                    enzyme_genbank_gene = external_id.find('identifier').text
                elif external_id.find('resource').text == 'GenBank Protein Database':
                    enzyme_genbank_protein = external_id.find('identifier').text
                elif external_id.find('resource').text == 'HUGO Gene Nomenclature Committee (HGNC)':
                    enzyme_hgnc_id = external_id.find('identifier').text

            enzyme_actions = [s.text.lower() for s in enzyme.find('actions').findall('action')]

            drug2attrib[drugbank_id]['enzymes'].append((enzyme_id, enzyme_actions))

            if enzyme_id not in enzyme2attrib:  # {'gene', 'name', 'organism', 'taxonomy_id', 'uniprot_id', 'genbank_gene_id', 'genbank_protein_id', 'hgnc_id'}
                enzyme2attrib[enzyme_id]['gene'] = enzyme_gene
                enzyme2attrib[enzyme_id]['name'] = enzyme_name
                enzyme2attrib[enzyme_id]['organism'] = enzyme_organism
                enzyme2attrib[enzyme_id]['taxonomy_id'] = enzyme_taxonomy_id

                enzyme2attrib[enzyme_id]['uniprot_id'] = enzyme_uniprot_id
                enzyme2attrib[enzyme_id]['genbank_gene_id'] = enzyme_genbank_gene
                enzyme2attrib[enzyme_id]['genbank_protein_id'] = enzyme_genbank_protein
                enzyme2attrib[enzyme_id]['hgnc_id'] = enzyme_hgnc_id

        # print enzyme_id, enzyme_gene, enzyme_name, enzyme_organism, enzyme_taxonomy_id, enzyme_actions

    # Get transporters
    drug2attrib[drugbank_id]['transporters'] = []
    for transporter in child.find('transporters').findall('transporter'):
        if transporter.find('polypeptide') is None:
            continue

        transporter_id = transporter.find('id').text
        transporter_gene = transporter.find('polypeptide').find('gene-name').text
        transporter_name = transporter.find('name').text
        transporter_organism = transporter.find('organism').text
        transporter_taxonomy_id = transporter.find('polypeptide').find('organism').attrib['ncbi-taxonomy-id']

        if transporter_organism is None and transporter_taxonomy_id == '9606':
            transporter_organism = 'Human'
        if transporter_organism == 'Human' and transporter_taxonomy_id == '':
            transporter_taxonomy_id = '9606'
        if transporter_organism == 'Homo sapiens':
            transporter_organism = 'Human'
        if transporter_gene is None or transporter_organism is None or transporter_taxonomy_id is None:
            continue

        transporter_external_ids = transporter.find('polypeptide').find('external-identifiers').findall('external-identifier')
        transporter_uniprot_id = ''
        transporter_genbank_gene = ''
        transporter_genbank_protein = ''
        transporter_hgnc_id = ''

        for external_id in transporter_external_ids:
            if external_id.find('resource').text == 'UniProtKB':
                transporter_uniprot_id = external_id.find('identifier').text
            elif external_id.find('resource').text == 'GenBank Gene Database':
                transporter_genbank_gene = external_id.find('identifier').text
            elif external_id.find('resource').text == 'GenBank Protein Database':
                transporter_genbank_protein = external_id.find('identifier').text
            elif external_id.find('resource').text == 'HUGO Gene Nomenclature Committee (HGNC)':
                transporter_hgnc_id = external_id.find('identifier').text

        transporter_actions = [s.text.lower() for s in transporter.find('actions').findall('action')]

        drug2attrib[drugbank_id]['transporters'].append((transporter_id, transporter_actions))

        if transporter_id not in transporter2attrib:  # {'gene', 'name', 'organism', 'taxonomy_id', 'uniprot_id', 'genbank_gene_id', 'genbank_protein_id', 'hgnc_id'}
            transporter2attrib[transporter_id]['gene'] = transporter_gene
            transporter2attrib[transporter_id]['name'] = transporter_name
            transporter2attrib[transporter_id]['organism'] = transporter_organism
            transporter2attrib[transporter_id]['taxonomy_id'] = transporter_taxonomy_id

            transporter2attrib[transporter_id]['uniprot_id'] = transporter_uniprot_id
            transporter2attrib[transporter_id]['genbank_gene_id'] = transporter_genbank_gene
            transporter2attrib[transporter_id]['genbank_protein_id'] = transporter_genbank_protein
            transporter2attrib[transporter_id]['hgnc_id'] = transporter_hgnc_id

        # print transporter_id, transporter_gene, transporter_name, transporter_organism, transporter_taxonomy_id, transporter_actions

    #print(drugbank_id, drugname, drug_type, groups)
    print('targets:', len(drug2attrib[drugbank_id]['targets']))
    print('enzymes:', len(drug2attrib[drugbank_id]['enzymes']))
    print('transporters:', len(drug2attrib[drugbank_id]['transporters']))
    print('\n')

print('\n')

#######################################################################
# List of drugs to save (as long as num_targets + num_enzymes + num_transporters != 0)
drugs = []
for drugbank_id in sorted(drug2attrib.keys()):
    if len(drug2attrib[drugbank_id]['targets']) == 0 and len(drug2attrib[drugbank_id]['enzymes']) == 0 and len(
            drug2attrib[drugbank_id]['transporters']) == 0:
        continue
    else:
        drugs.append(drugbank_id)

print(len(drug2attrib), "drugs parsed from XML")
print(len(drugs), "drugs with at least 1 target/ enzyme/ transporter")

#######################################################################
# Save drug attributes to CSV {'drugname', 'drug_type', 'groups', 'targets/enzymes/transporters': [_id, _actions]}
outf = open('drugbank05_drugs.csv', 'w')
writer = csv.writer(outf)
writer.writerow(
    ['drugbank_id', 'drugname', 'drug_type','target','approved', 'experimental', 'illicit', 'investigational', 'nutraceutical',
     'withdrawn'])

for drugbank_id in drugs:
    drugname = drug2attrib[drugbank_id]['drugname']
    # if isinstance(drugname, unicode):
    #     if u'\u03b2' in drugname:
    #         drugname = drugname.replace(u'\u03b2', 'beta')
    #     if u'\u03b1' in drugname:
    #         drugname = drugname.replace(u'\u03b1', 'alpha')
    #     drugname = drugname.encode("utf-8")
    drug_type = drug2attrib[drugbank_id]['drug_type']
    drug_target = drug2attrib[drugbank_id]['targets']
    groups = [1 if group in drug2attrib[drugbank_id]['groups'] else 0 for group in
              ['approved', 'experimental', 'illicit', 'investigational', 'nutraceutical', 'withdrawn']]

    writer.writerow([drugbank_id, drugname, drug_type, drug_target] + groups)

outf.close()

######################################################################
#将所有的targets, enzymes, transporters 保存成csv文件

# drugbank_target_id -> #{'gene', 'name', 'organism', 'taxonomy_id', 'uniprot_id', 'genbank_gene_id', 'genbank_protein_id', 'hgnc_id'}

# outf = open('drugbank05_partner_protein.csv', 'w')
# outfh = open('drugbank05_partner_protein_human.csv', 'w')
# writer = csv.writer(outf)
# writerh = csv.writer(outfh)
#
# writer.writerow(
#     ['partner_id', 'partner_name', 'gene_name', 'uniprot_id', 'genbank_gene_id', 'genbank_protein_id', 'hgnc_id',
#      'organism', 'taxonomy_id'])
# writerh.writerow(
#     ['partner_id', 'partner_name', 'gene_name', 'uniprot_id', 'genbank_gene_id', 'genbank_protein_id', 'hgnc_id',
#      'organism', 'taxonomy_id'])
#
# partners_written = set()
#
# # Targets
# for partner_id in sorted(target2attrib.keys()):
#     if partner_id in partners_written:
#         # print partner_id, target2attrib[partner_id]['gene'], 'already recorded'
#         continue
#
#     partner_name = target2attrib[partner_id]['name']
#     gene_name = target2attrib[partner_id]['gene']
#     organism = target2attrib[partner_id]['organism']
#     taxonomy_id = target2attrib[partner_id]['taxonomy_id']
#
#     uniprot_id = target2attrib[partner_id]['uniprot_id']
#     genbank_gene_id = target2attrib[partner_id]['genbank_gene_id']
#     genbank_protein_id = target2attrib[partner_id]['genbank_protein_id']
#     hgnc_id = target2attrib[partner_id]['hgnc_id']
#
#     partners_written.add(partner_id)
#
#     writer.writerow(
#         [partner_id, partner_name, gene_name, uniprot_id, genbank_gene_id, genbank_protein_id, hgnc_id, organism,
#          taxonomy_id])
#
#     if taxonomy_id == '9606' and organism == 'Human':
#         writerh.writerow(
#             [partner_id, partner_name, gene_name, uniprot_id, genbank_gene_id, genbank_protein_id, hgnc_id, organism,
#              taxonomy_id])
#
#     if taxonomy_id == '9606' and organism.lower() != 'human':
#         print(partner_id, target2attrib[partner_id]['gene'], organism, taxonomy_id, 'organism mismatch')
#
# # enzymes
# for partner_id in sorted(enzyme2attrib.keys()):
#     if partner_id in partners_written:
#         # print partner_id, enzyme2attrib[partner_id]['gene'], 'already recorded in targets'
#         continue
#
#     partner_name = enzyme2attrib[partner_id]['name']
#     gene_name = enzyme2attrib[partner_id]['gene']
#     organism = enzyme2attrib[partner_id]['organism']
#     taxonomy_id = enzyme2attrib[partner_id]['taxonomy_id']
#
#     uniprot_id = enzyme2attrib[partner_id]['uniprot_id']
#     genbank_gene_id = enzyme2attrib[partner_id]['genbank_gene_id']
#     genbank_protein_id = enzyme2attrib[partner_id]['genbank_protein_id']
#     hgnc_id = enzyme2attrib[partner_id]['hgnc_id']
#
#     partners_written.add(partner_id)
#
#     writer.writerow(
#         [partner_id, partner_name, gene_name, uniprot_id, genbank_gene_id, genbank_protein_id, hgnc_id, organism,
#          taxonomy_id])
#
#     if taxonomy_id == '9606' and organism == 'Human':
#         writerh.writerow(
#             [partner_id, partner_name, gene_name, uniprot_id, genbank_gene_id, genbank_protein_id, hgnc_id, organism,
#              taxonomy_id])
#
#     if taxonomy_id == '9606' and organism.lower() != 'human':
#         print(partner_id, enzyme2attrib[partner_id]['gene'], organism, taxonomy_id, 'organism mismatch')
#
# # transporters
# for partner_id in sorted(transporter2attrib.keys()):
#     if partner_id in partners_written:
#         # print partner_id, transporter2attrib[partner_id]['gene'], 'already recorded in targets and/or enzymes'
#         continue
#
#     partner_name = transporter2attrib[partner_id]['name']
#     gene_name = transporter2attrib[partner_id]['gene']
#     organism = transporter2attrib[partner_id]['organism']
#     taxonomy_id = transporter2attrib[partner_id]['taxonomy_id']
#
#     uniprot_id = transporter2attrib[partner_id]['uniprot_id']
#     genbank_gene_id = transporter2attrib[partner_id]['genbank_gene_id']
#     genbank_protein_id = transporter2attrib[partner_id]['genbank_protein_id']
#     hgnc_id = transporter2attrib[partner_id]['hgnc_id']
#
#     partners_written.add(partner_id)
#
#     writer.writerow(
#         [partner_id, partner_name, gene_name, uniprot_id, genbank_gene_id, genbank_protein_id, hgnc_id, organism,
#          taxonomy_id])
#
#     if taxonomy_id == '9606' and organism == 'Human':
#         writerh.writerow(
#             [partner_id, partner_name, gene_name, uniprot_id, genbank_gene_id, genbank_protein_id, hgnc_id, organism,
#              taxonomy_id])
#
#     if taxonomy_id == '9606' and organism.lower() != 'human':
#         print(partner_id, transporter2attrib[partner_id]['gene'], organism, taxonomy_id, 'organism mismatch')
#
# outf.close()
# outfh.close()
#
# #######################################################################
# # Save drug-target, -enzyme, -transporter pairs to CSV
#
# # target [('antagonist', 1374), ('agonist', 857), ('inhibitor', 1818)]
# # enzyme [('substrate', 2402), ('inducer', 407), ('inhibitor', 1350)]
# # transporter [('substrate', 790), ('inducer', 100), ('inhibitor', 1075)]
#
# # Targets
# outf = open('drugbank05_drug2target.csv', 'w')
# outfh = open('drugbank05_drug2target_human.csv', 'w')
# writer = csv.writer(outf)
# writerh = csv.writer(outfh)
#
# target_actions_to_write = ['inhibitor', 'antagonist', 'agonist']
# writer.writerow(['drugbank_id', 'partner_id'] + target_actions_to_write)
# writerh.writerow(['drugbank_id', 'partner_id'] + target_actions_to_write)
#
# for drugbank_id in drugs:
#     for (target_id, target_actions) in drug2attrib[drugbank_id]['targets']:
#         actions = [1 if action in target_actions else 0 for action in target_actions_to_write]
#
#         writer.writerow([drugbank_id, target_id] + actions)
#
#         if target2attrib[target_id]['organism'] == 'Human' and target2attrib[target_id]['taxonomy_id'] == '9606':
#             writerh.writerow([drugbank_id, target_id] + actions)
#
# outf.close()
# outfh.close()
#
# # Enzymes
# outf = open('drugbank05_drug2enzyme.csv', 'w')
# outfh = open('drugbank05_drug2enzyme_human.csv', 'w')
# writer = csv.writer(outf)
# writerh = csv.writer(outfh)
#
# enzyme_actions_to_write = ['substrate', 'inducer', 'inhibitor']
# writer.writerow(['drugbank_id', 'partner_id'] + enzyme_actions_to_write)
# writerh.writerow(['drugbank_id', 'partner_id'] + enzyme_actions_to_write)
#
# for drugbank_id in drugs:
#     for (enzyme_id, enzyme_actions) in drug2attrib[drugbank_id]['enzymes']:
#         actions = [1 if action in enzyme_actions else 0 for action in enzyme_actions_to_write]
#
#         writer.writerow([drugbank_id, enzyme_id] + actions)
#
#         if enzyme2attrib[enzyme_id]['organism'] == 'Human' and enzyme2attrib[enzyme_id]['taxonomy_id'] == '9606':
#             writerh.writerow([drugbank_id, enzyme_id] + actions)
#
# outf.close()
# outfh.close()
#
# # Transporters
# outf = open('drugbank05_drug2transporter.csv', 'w')
# outfh = open('drugbank05_drug2transporter_human.csv', 'w')
# writer = csv.writer(outf)
# writerh = csv.writer(outfh)
#
# transporter_actions_to_write = ['substrate', 'inducer', 'inhibitor']
# writer.writerow(['drugbank_id', 'partner_id'] + transporter_actions_to_write)
# writerh.writerow(['drugbank_id', 'partner_id'] + transporter_actions_to_write)
#
# for drugbank_id in drugs:
#     for (transporter_id, transporter_actions) in drug2attrib[drugbank_id]['transporters']:
#         actions = [1 if action in transporter_actions else 0 for action in transporter_actions_to_write]
#
#         writer.writerow([drugbank_id, transporter_id] + actions)
#
#         if transporter2attrib[transporter_id]['organism'] == 'Human' and transporter2attrib[transporter_id][
#             'taxonomy_id'] == '9606':
#             writerh.writerow([drugbank_id, transporter_id] + actions)
#
# outf.close()
# outfh.close()
