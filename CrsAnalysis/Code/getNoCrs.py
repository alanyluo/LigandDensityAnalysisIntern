'''
getNoCrs.py
    Get the residues that have no crystal contacts.

Usage: getNoCrs.py <discrepDataDirPath> <crsDirPath> <resultFilePath> <maxDist>

Parameters:
    <discrepDataDirPath> - path to directory containing discrepancy data
    <crsDirPath> - path to directory containing crystal contact data
    <resultFilePath> - file path to the text file in which to store the dataset
    <maxDist> - the maximum observed crystal contact distance amongst all ATP residues

Example: python3 crsContactAnalysis/code/getNoCrs.py results/standalone_01-04-22 crsContactAnalysis/results/within_10_2022-01-04 crsContactAnalysis/results/noCrs.txt 10
    
    Run this example commands in LigandDensityAnalysis.
'''


import sys
import Bio.PDB as bioPDB
import numpy as np
import json
import os


def main(discrepDirPath: str, crsDirPath: str, resultFilePath: str, maxDist: float) -> None:
    """
    :param discrepDirPath: path to directory of discrepancy data
    :param crsDirPath: path to directory containing crystal contact data
    :param resultFilePath: path to text file of beyond results
    :param maxDist: maximum observed metal contact distance
    """
    # Get the regional discrepancy dictionary discrepDict.
    discrepDict = getDiscrepDict(discrepDirPath)

    # Add crystal contact distances to discrepDict.
    discrepDict = updateDiscrepDict(crsDirPath, discrepDict)

    with open(resultFilePath, 'w') as resultFile:
        resultList = []

        for ((pdbID, _, _, _, _), residueDict) in discrepDict.items():
            absDiscrep = residueDict['num_electrons_actual_abs_significant_regional_discrepancy']
            nonabsDiscrep = residueDict['num_electrons_actual_significant_regional_discrepancy']

            if'crystal_contact_distance' not in residueDict.keys():
                crsData = ','.join(str(val) for val in [pdbID, absDiscrep, nonabsDiscrep, maxDist])
                resultList.append(crsData)
        
        resultFile.write('\n'.join(resultList))

    print('Finished running!')


def updateDiscrepDict(crsDirPath, discrepDict):
    '''
    Add crystal contact distances from the dataset at crsDirPath to the dictionary discrepDict.
    '''
    with os.scandir(crsDirPath) as crsDir:
        for crsFilePath in crsDir:
            with open(crsFilePath, 'r') as crsFile:
                atomList = json.load(crsFile)
                for atomDict in atomList:
                    residueID = (atomDict['pdbid'], atomDict['model'], atomDict['chain'], atomDict['residue_name'], atomDict['residue_number'])

                    if residueID in discrepDict.keys():
                        if 'crystal_contact_distance' not in discrepDict[residueID].keys():
                            discrepDict[residueID].update({'crystal_contact_distance':atomDict['crystal_contact_distance']})
                        else:
                            atomDist = atomDict['crystal_contact_distance']
                            currDist = discrepDict[residueID]['crystal_contact_distance']

                            if atomDist < currDist:
                                discrepDict[residueID]['crystal_contact_distance'] = atomDist
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

                for residueDict in residueList:
                    residueID = (residueDict['PDB ID'], residueDict['model'], residueDict['chain'], residueDict['residue_name'], residueDict['residue_number'])
                    discrepDict.update({residueID:residueDict})
    return discrepDict


if __name__ == '__main__':
    try:
        _, discrepDirPath, crsDirPath, resultFilePath, maxDistStr = sys.argv
        main(discrepDirPath, crsDirPath, resultFilePath, float(maxDistStr))
    except AssertionError:
        raise
    except Exception as e:
        print(e)
        print(__doc__)
