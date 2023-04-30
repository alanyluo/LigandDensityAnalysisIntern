'''
getMetalDatasets.py
    Get the within_3_5 and beyond_3_5 datasets for each of the three sets of metals.
    
    In this code, these sets are denoted as follows.

    "First": only Mg
    "Second": Mg & 5 most prevalent metals
    "Third": all metals

Usage: getMetalDatasets.py <pdbIDFilePath> <discrepancyDataDirPath> <withinFilePath> <beyondFilePath> <distCutoff> <metalNameList>

Parameters:
    <pdbIDFilePath> - file path to text file of PDB IDs.
    <discrepancyDataDirPath> - path to directory containing discrepancy data.
    <withinFilePath> - file path to the text file in which to store within dataset.
    <beyondFilePath> - file path to the text file in which to store beyond dataset.
    <distCutoff> - distance cutoff to distinguish within and beyond datasets.
    <metalNameList> - comma-separated list of metals.

Example 1: python3 metalAnalysis/code/getMetalDatasets.py results/standalone_01-04-22.txt results/standalone_01-04-22  metalAnalysis/results/firstWithin.txt metalAnalysis/results/firstBeyond.txt 3.5 MG

Example 2: python3 metalAnalysis/code/getMetalDatasets.py results/standalone_01-04-22.txt results/standalone_01-04-22 metalAnalysis/results/secondWithin.txt metalAnalysis/results/secondBeyond.txt 3.5 ZN,MG,CA,FE,NA,MN

Example 3: python3 metalAnalysis/code/getMetalDatasets.py results/standalone_01-04-22.txt results/standalone_01-04-22 metalAnalysis/results/thirdWithin.txt metalAnalysis/results/thirdBeyond.txt 3.5 ZN,MG,CA,FE,NA,MN,K,CU,NI,CO,CD,HG,PT,MO,AL,V,BA,SR,RU,CS,W,YB,AU,Y,LI,PB,GD,TL,RB,SM,IR,PR,RH,EU,PD,AG,OS,LU,HO,TB,CR,GA,LA,SB,CE,ER,IN,BI,DY,BE,ZR,SN,HF,TA,RE,PA,U
    
    Run all three example commands in LigandDensityAnalysis.
'''


import sys
import Bio.PDB as bioPDB
import numpy as np
import json
import os


pdbFolderPath = 'results/structFiles_01-04-22/'


def main(pdbIDFilePath: str, discrepDirPath: str, withinFilePath: str, beyondFilePath: str, distCutoff: float, metalNameList: str) -> None:
    """
    :param pdbIDFilePath: path to text file of PDB IDs.
    :param discrepDirPath: path to directory of discrepancy data.
    :param withinFilePath: path to text file of within results.
    :param beyondFilePath: path to text file of beyond results.
    :param distCutoff: distance cutoff for metal ion contact distance.
    :param metalNameList: list of metals to collect.
    """
    # Get the metal ion dictionary.
    resDictList = getResDictList(metalNameList, pdbIDFilePath)
    # print('length of metalList 2 ', len(metalList))
    # assert(len(metalList) > 0)
    
    # Get the regional discrepancy dictionary discrepDict.
    discrepDict = getDiscrepDict(discrepDirPath)

    # Add metal ion distances to discrepDict.
    for resDict in resDictList:
        residueID = (resDict['pdbid'], resDict['model'], resDict['chain'], resDict['residue_name'], resDict['residue_number'])

        if residueID in discrepDict.keys():
            discrepDict[residueID].update({'metal_distance':resDict['min_dist']})

    with open(withinFilePath, 'w') as withinFile, \
        open(beyondFilePath, 'w') as beyondFile:

        withinList = []
        beyondList = []

        for ((pdbID, _, _, _, _), residueDict) in discrepDict.items():
            absDiscrep = residueDict['num_electrons_actual_abs_significant_regional_discrepancy']
            nonabsDiscrep = residueDict['num_electrons_actual_significant_regional_discrepancy']

            if 'metal_distance' in residueDict.keys():
                metalDist = residueDict['metal_distance']

                metalData = ','.join(str(val) for val in [pdbID, absDiscrep, nonabsDiscrep, metalDist])

                # Put metalData into the correct datasets.
                # print('last')
                if metalDist > distCutoff:
                    beyondList.append(metalData)
                else:
                    withinList.append(metalData)
        
        withinFile.write('\n'.join(withinList))
        beyondFile.write('\n'.join(beyondList))

    print('Finished running!')


def getInitDist(metalList, atomList):
    '''
    Get the initial metal distance to use as the initial value for minDist in getResDictList.

    :param metalList: list of metals
    :param atomList: list of atoms
    '''
    for metal in metalList:
        distList = [np.linalg.norm(atom.coord - metal.coord) for atom in atomList if not np.array_equal(atom.coord, metal.coord)]

        if(len(distList) > 0):
            return np.min(distList)
    return sys.maxsize


def getResDictList(metalNameList: list, pdbIDFilePath: str) -> list:
    '''
    Return the list of ATP residues that are each paired with their minimum metal ion distances. The ATP residues reside in the PDB entries referenced in the file at pdbIDFilePath.

    :param metalNameList: list of names of metals
    :param pdbIDFilePath: path to the file containing the list of PDB IDs
    '''

    resDictList = []
    
    with open(pdbIDFilePath, 'r') as pdbIDFile:
        pdbIDList = [line.rstrip('\n') for line in pdbIDFile]
        for pdbid in pdbIDList:
            pdbID = pdbid.lower()
            structFilePath = pdbFolderPath + 'pdb' + pdbID + '.ent'

            if os.path.isfile(structFilePath):
                parser = bioPDB.PDBParser(QUIET=True)
                bioPDBObj = parser.get_structure(pdbID, structFilePath)
            
                atomList = list(bioPDBObj.get_atoms())
                metalList = [atom for atom in atomList if atom.element in metalNameList]
                resList = list(bioPDBObj.get_residues())
                atpResList = [res for res in resList if res.resname == 'ATP']

                for res in atpResList:
                    atpAtomList = list(res.get_atoms())

                    # NOTE: This is just an initial value for minDist.
                    minDist = getInitDist(metalList, atpAtomList)

                    for metal in metalList:
                        distList = [np.linalg.norm(atom.coord - metal.coord) for atom in atpAtomList if not np.array_equal(atom.coord, metal.coord)]

                        if(len(distList) > 0):
                            currMinDist = np.min(distList)

                            if currMinDist < minDist:
                                minDist = currMinDist
                        
                    # If there is a minimum distance
                    if minDist < sys.maxsize:
                        resDictList.append({'pdbid':pdbID, 'model':res.parent.parent.id, 'chain':res.parent.id, 'residue_name':res.resname, 'residue_number':res.id[1], 'min_dist':minDist})
            
            else:
                print('no struct file for ' + pdbID)
            
            # print('')

    return resDictList


def getDiscrepDict(discrepDirPath: str) -> dict:
    '''
    Return the discrepancy data referenced at discrepDirPath as a dictionary of residue dictionaries.

    :param discrepDirPath: path to the directory containing the discrepancy data
    '''
    discrepDict = dict()
    with os.scandir(discrepDirPath) as discrepDir:
        for dirEntry in discrepDir:
            with open(dirEntry, 'r') as discrepFile:
                # Recall that each discrepFile represents the discrepancy data for a unique PDB entry. So really, we are iterating over each PDB entry's dicsrepancy data.
                residueList = json.load(discrepFile)

                for residueDict in residueList:
                    residueID = (residueDict['PDB ID'], residueDict['model'], residueDict['chain'], residueDict['residue_name'], residueDict['residue_number'])

                    # print(f"discrepDict residueID: %s" % (residueID,))

                    discrepDict.update({residueID:residueDict})
    return discrepDict


if __name__ == '__main__':
    try:
        _, pdbIDFilePath, discrepDirPath, withinFilePath, beyondFilePath, distCutoff, metalNameList = sys.argv
        main(pdbIDFilePath, discrepDirPath, withinFilePath, beyondFilePath, float(distCutoff), metalNameList.split(','))
    except Exception as e:
        print(e)
        print(__doc__)
