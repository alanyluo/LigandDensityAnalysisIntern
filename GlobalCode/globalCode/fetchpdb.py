'''
Retrieve the structure files for the given PDB entries.

fetchpdb.py pdbIDFilePath resDirPath
'''


import requests
import os
import sys
import multiprocessing
import Bio.PDB as biopdb

pdbids = [l[0:4] for l in open(sys.argv[1]).readlines()]

def fetch_url(pdbid):
    pdbfolder = sys.argv[2]
    if not os.path.isfile(pdbfolder + 'pdb' + pdbid.lower() + '.ent'):
        try:
            pdbl = biopdb.PDBList()
            pdbl.retrieve_pdb_file(pdbid, pdir=pdbfolder, file_format="pdb")
            return 'True'
        except:
            print(pdbid)
            return 'False'


workers = multiprocessing.Pool(11)
results = workers.map(fetch_url, pdbids)

