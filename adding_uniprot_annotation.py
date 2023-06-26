import cobra

#check for duplicate gene names
def duplicates(file_name):
    gene_names = []
    seen = set()
    dupes = []
    file = open(file_name, 'r')    
    
    #reading in alle gene names
    for line in file:
        name = line.strip()
        gene_names.append(name)
    file.close()        
    
    #check for duplicates
    for gene_name in gene_names:
        if gene_name in seen:
            dupes.append(gene_name)
        else:
            seen.add(gene_name)
    #print(gene_names)
    #print(f'There are {len(dupes)} duplicates.')
    #print(f'There are {len(seen)} unique gene names.')
    return gene_names
#duplicates('all_gene_names_from_model.txt')

def getting_gene_names_from_model(model_name, file_name):
    model = cobra.io.read_sbml_model(model_name)
    file = open(file_name, 'w')    
    for gene in model.genes:
        file.write(str(gene))
        file.write('\n')
    file.close()
#getting_gene_names_from_model('hESCNet.xml', 'all_gene_names_from_model.txt')

def writing_csv_file(input_file_name, output_file_name):
    #input file is a TSV .txt file with raw data from UniProtKB.
    #Each line has 9 values: gene_name  UniProtID   value3  value4  etc
    #raw data from: https://www.uniprot.org/id-mapping
    #output file is a CSV .txt file. Each line has the format: gene_name,uniprot_id
    
    #reading in all gene names from raw data (input file)
    all_gene_names_and_uniprot_ids = {} #dictionary{gene_name, list[uniprot_ids]}
    file = open(input_file_name, 'r')
    next(file)                              #skip header line
    for line in file:
        data = line.strip().split("\t")     #the values are tab separated (TSV)
        gene_name = data[0].strip()
        uniprot_id = data[1].strip()
        if gene_name not in all_gene_names_and_uniprot_ids:
            uniprot_id_list = [uniprot_id]
            all_gene_names_and_uniprot_ids[gene_name] = uniprot_id_list #creating new entry in dic
        else:
            all_gene_names_and_uniprot_ids[gene_name].append(uniprot_id) #adding to list aldready in dic
    file.close()

    #writing CSV file
    file2 = open(output_file_name, 'w')
    names_mapping_to_multiple_ids = []
    for gene_name in all_gene_names_and_uniprot_ids:
        number_of_ids = len(all_gene_names_and_uniprot_ids[gene_name])
        if number_of_ids == 1:
            uniprot_id = all_gene_names_and_uniprot_ids[gene_name][0]
            file2.write(f'{gene_name},{uniprot_id}\n')
        else:
            names_mapping_to_multiple_ids.append(gene_name)
    print(f'{len(names_mapping_to_multiple_ids)} gene names mapped to multiple IDs')
    file2.close()

    #gene_names = duplicates('all_gene_names_from_model.txt')
    #print('number of unique gene names: ', len(gene_names))
    #print('length of dic: ', len(all_gene_names_and_uniprot_ids))
    #missing = []
    #for name in gene_names:
    #    if name not in all_gene_names_and_uniprot_ids:
    #        missing.append(name)
    #print('len missing', len(missing))
    #print(missing)
    #print(all_gene_names_and_uniprot_ids['PTGS1'])
    #finding duplicates
    #seen = set()
    #dupes = []
    #for gene_name in gene_names:
    #    if gene_name in seen:
    #        dupes.append(gene_name)
    #    else:
    #        seen.add(gene_name)
    #print(f'There are {len(dupes)} duplicates.')
    #print(f'There are {len(seen)} gene names that map to exactly 1 uniprotID.')
#writing_csv_file('uniprot_raw_data.txt', 'gene_names_and_uniprotIDs.txt')

def create_dictionary(file_name):
    name_ID = {}
    file = open(file_name, 'r')
    for line in file:
        data = line.strip().split(",")
        gene_name = data[0].strip()
        uniprotID = data[1].strip()
        name_ID[gene_name] = uniprotID
    file.close()
    return name_ID

def add_annotation(model_name):
    model = cobra.io.read_sbml_model(model_name)
    name_ID_dic = create_dictionary('gene_names_and_uniprotIDs.txt')
    for gene_name in name_ID_dic:
        gene = model.genes.get_by_id(gene_name)            #gene name is used as gene ID in model
        uniprot_ID = name_ID_dic[gene_name]
        
        #adding uniprotID to annotation of gene in model
        annotation_dic = gene.annotation
        annotation_dic['uniprot'] = uniprot_ID
        gene.annotation = annotation_dic                    #using decorator in cobrapy source code
        cobra.io.write_sbml_model(model, 'hESCNet.xml')
add_annotation('hESCNet.xml')