# functions for taking list of protein IDs we are interested in, fetching the sequences using uniprotID, 
# converting to FASTA file then running this through CD-HIT
# This returns a cleaned row of representative protein IDs that are used downstream for position weight matrix generation

import requests
import os 
import subprocess

def fetch_uniprot_sequences(ids, batch):
    
    """
    Takes list of UNIPROT ids and fetches corresponding sequence
    
    inputs:
    list of UNIPROT ids
    batch number - how many to query at one time
    
    outputs:
    dict in format:{id: sequence}
    list of UNIPROT ids for which sequences weren't found
    """
    
    missing = []
    id_dict = {}
    for i in range(0, len(ids), batch):
        
        chunk = ids[i : i + batch]
        #print(chunk)
        
        for uniprot_id in chunk:
            url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
            response = requests.get(url)
            
            #print(response.text)

            if response.status_code == 200:
                fasta = response.text
                #print(fasta)
                for line in fasta.splitlines():
                    if line.startswith(">"):
                        # f.write(f"\n")
                        parts = line.split("|")
                        
                        id = parts[1]
                        id_dict[id] = ""
                        #print(id)
                        #f.write(f">{id}\n")
                        continue
                        
                    # f.write(f"{line}\n")
                    id_dict[id] += line
            else:
                print(f"Failed to retrieve {uniprot_id}")
                missing.append(uniprot_id)
    return id_dict, missing



def create_fasta(dic):
    """
    converts previously returned dict to FASTA format for CD-HIT
    
    inputs: id:sequence dict
    
    outputs: FASTA file
    """
    
    with open(f"{file_path}/Test.fasta", "w") as f:
        for id, seq in dic.items():
            f.write(f">{id}\n{seq}\n")
            
    f.close()