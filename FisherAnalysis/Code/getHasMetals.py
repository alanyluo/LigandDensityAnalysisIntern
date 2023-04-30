'''
Get the hasMetals dataset.

Usage: getHasMetals.py <pdbIDFilePath> <discrepDirPath> <ligandName> <resultFilePath> <metalNameList> <structFileDirPath>

Example 1: python3 fisherAnalysis/code/getHasMetals.py results/standalone_01-04-22.txt results/standalone_adp_01-04-22 ADP fisherAnalysis/results/hasMetalsMg.txt MG globalData/structFiles_adp_07-22-22

Example 2: python3 fisherAnalysis/code/getHasMetals.py results/standalone_01-04-22.txt results/standalone_adp_01-04-22 ADP fisherAnalysis/results/hasMetalsTopSix.txt ZN,MG,CA,FE,NA,MN globalData/structFiles_adp_07-22-22

Example 3: python3 fisherAnalysis/code/getHasMetals.py results/standalone_01-04-22.txt results/standalone_adp_01-04-22 ADP fisherAnalysis/results/hasMetalsAll.txt ZN,MG,CA,FE,NA,MN,K,CU,NI,CO,CD,HG,PT,MO,AL,V,BA,SR,RU,CS,W,YB,AU,Y,LI,PB,GD,TL,RB,SM,IR,PR,RH,EU,PD,AG,OS,LU,HO,TB,CR,GA,LA,SB,CE,ER,IN,BI,DY,BE,ZR,SN,HF,TA,RE,PA,U globalData/structFiles_adp_07-22-22
'''


import sys
import Bio.PDB as bioPDB
import numpy as np
import json
import os


# pdbFolderPath = 'globalData/structFiles_01-04-22/'


def main(pdbIDFilePath: str, discrepDirPath: str, ligandName:str, resultFilePath: str, metalNameList: list, structFileDirPath:str) -> None:
    """
    :param pdbIDFilePath: path to text file of PDB IDs
    :param discrepDirPath: path to directory of discrepancy data
    :param ligandName: name of the ligand to search for
    :param resultFilePath: path to the text file in which to record the final dataset
    :param metalNameList: list of metals to collect
    :param structFileDirPath: path to the directory containing the struct files for the ligand dataset
    """
    # print('entered main')
    discrepDict = getDiscrepDict(discrepDirPath)
    # print('got discrepDict')
    
    discrepDict = getMetalDists(discrepDict, metalNameList, ligandName, pdbIDFilePath, structFileDirPath)
    # print('got metal dists')

    resultList = []
    for ((pdbID, _, _, _, _), residueDict) in discrepDict.items():
        absDiscrep = residueDict['num_electrons_actual_abs_significant_regional_discrepancy']
        nonabsDiscrep = residueDict['num_electrons_actual_significant_regional_discrepancy']

        # print('got discreps')
        if 'metalDist' in residueDict.keys():
            # print('has metalDist')
            metalDist = residueDict['metalDist']

            # NOTE: strictly for debugging
            assert(metalDist < sys.maxsize)

            finalData = ','.join(str(val) for val in [pdbID, absDiscrep, nonabsDiscrep, metalDist])

            resultList.append(finalData)
    
    # print('resultList len', len(resultList))
    with open(resultFilePath, 'w') as resultFile, \
        open(pdbIDFilePath, 'r') as pdbIDFile:
        resultFile.write('\n'.join(resultList))

        # NOTE: The following lines in this with block are just a sanity check.
        print('num of residues:', len(resultList))
        numEntries = len([entryName for entryName in pdbIDFile])
        print('num of entries:', numEntries)

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


def getMetalDists(discrepDict:dict, metalNameList: list, ligandName:str, pdbIDFilePath: str, structFileDirPath:str) -> dict:
    '''
    Add metal contact distances to the residues in discrepDict.

    :param discrepDict: dictionary of residues paired with basic info about them along with discrepancy data
    :param metalNameList: list of names of metals
    :param ligandName: name of the ligand to search for
    :param pdbIDFilePath: path to the file containing the list of PDB IDs
    :param structFileDirPath: path to the directory containing the struct files for the ligand dataset
    '''

    with open(pdbIDFilePath, 'r') as pdbIDFile:
        pdbIDList = [line.rstrip('\n') for line in pdbIDFile]
        for pdbid in pdbIDList:
            pdbID = pdbid.lower()
            structFilePath = structFileDirPath + 'pdb' + pdbID + '.ent'

            if os.path.isfile(structFilePath):
                parser = bioPDB.PDBParser(QUIET=True)
                bioPDBObj = parser.get_structure(pdbID, structFilePath)
            
                atomList = list(bioPDBObj.get_atoms())
                metalList = [atom for atom in atomList if atom.element in metalNameList]
                resList = list(bioPDBObj.get_residues())
                ligandResList = [res for res in resList if res.resname == ligandName]

                # print('ligand name', ligandName)
                # print('ligandResList len', len(ligandResList))

                for res in ligandResList:
                    resID = (pdbID, res.parent.parent.id, res.parent.id, res.resname, res.id[1])
                    # print('modelID type', type(res.parent.parent.id))

                    if resID in discrepDict.keys():
                        # print('has resID')
                        ligandAtomList = list(res.get_atoms())

                        # # NOTE: This is just an initial value for minDist.
                        # minDist = getInitDist(metalList, ligandAtomList)

                        distList = [np.linalg.norm(atom.coord - metal.coord) for atom in ligandAtomList for metal in metalList if not np.array_equal(atom.coord, metal.coord)]

                        minDist = np.min(distList) if len(distList) > 0 else sys.maxsize

                        # If there is a minimum distance
                        if minDist < sys.maxsize:
                            # print('has metalDist')
                            discrepDict[resID]['metalDist'] = minDist
            
            else:
                print('no struct file for ' + pdbID)
            
    return discrepDict


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

                # print('residueLIst len', len(residueList))

                for residueDict in residueList:
                    # NOTE: change the key "pdbid" to "PDB ID" if you are collecting data for standalone_atp_01-04-22
                    modelID = '1' if 'model' not in residueDict.keys() else residueDict['model']
                    residueID = (residueDict['pdbid'], modelID, residueDict['chain'], residueDict['residue_name'], residueDict['residue_number'])
                    
                    # print(f"discrepDict residueID: %s" % (residueID,))

                    discrepDict[residueID] = residueDict
    return discrepDict


if __name__ == '__main__':
    try:
        _, pdbIDFilePath, discrepDirPath, ligandName, resultFilePath, metalNameList, structFileDirPath = sys.argv
        # print('got argv')
        main(pdbIDFilePath, discrepDirPath, ligandName, resultFilePath, metalNameList.split(','), structFileDirPath)
    except AssertionError:
        raise
    except Exception as e:
        raise
        # print('got here error')
        # print(e)
        # print(__doc__)

