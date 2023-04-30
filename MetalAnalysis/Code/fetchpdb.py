'''
fetchpdb.py
    Retrieve the structure files for the PDB entries identified in the given input file.

Usage: fetchpdb.py <pdbIDFilePath>

Parameters:
    <pdbIDFilePath> - path to the file containing the desired PDB IDs

Example: python3 metalAnalysis/code/fetchpdb.py results/standalone_01-04-22.txt
    Run this in LigandDensityAnalysis.
'''


import requests
import os
import sys
import multiprocessing
import Bio.PDB as biopdb

pdbids = [l[0:4] for l in open(sys.argv[1]).readlines()]

def fetch_url(pdbid: str) -> str:
    '''
    Retrieve the structure file for the given PDB entry, if such a file exists.

    :param pdbid: PDB ID
    '''
    pdbfolder = 'results/structFiles_01-04-22/'
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

