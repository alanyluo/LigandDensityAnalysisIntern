'''
Get the both dataset.

Usage: getBoth.py <pdbIDFilePath> <discrepDirPath> <crsDirPath> <resultFilePath> <metalNameList> <maxMetalDist> <maxCrsDist>

Example: python3 fisherAnalysis/code/getBoth.py results/standalone_01-04-22.txt results/standalone_01-04-22 crsContactAnalysis/results/within_10_2022-01-04 fisherAnalysis/results/both.txt ZN,MG,CA,FE,NA,MN,K,CU,NI,CO,CD,HG,PT,MO,AL,V,BA,SR,RU,CS,W,YB,AU,Y,LI,PB,GD,TL,RB,SM,IR,PR,RH,EU,PD,AG,OS,LU,HO,TB,CR,GA,LA,SB,CE,ER,IN,BI,DY,BE,ZR,SN,HF,TA,RE,PA,U 87.38854217529297 10
'''


import sys
import Bio.PDB as bioPDB
import numpy as np
import json
import os


pdbFolderPath = 'results/structFiles_01-04-22/'


def main(pdbIDFilePath: str, discrepDirPath: str, crsDirPath:str, resultFilePath: str, metalNameList: str, maxMetalDist:float, maxCrsDist:float) -> None:
    """
    :param pdbIDFilePath: path to text file of PDB IDs
    :param discrepDirPath: path to directory of discrepancy data
    :param crsDirPath: path to the directory containing the crystal contact data
    :param resultFilePath: path to the text file in which to record the final dataset
    :param metalNameList: list of metals to collect
    :param maxMetalDist: maximum metal contact distance observed in the entire dataset
    :param maxCrsDist: maximum crystal contact distance observed in the entire dataset
    """
    discrepDict = getDiscrepDict(discrepDirPath)

    discrepDict = getCrsDists(crsDirPath, discrepDict)

    discrepDict = getMetalDists(discrepDict, metalNameList, pdbIDFilePath)

    # Add contact distances to discrepDict.
    for (resID, resDict) in discrepDict.items():
        metalDist = maxMetalDist
        crsDist = maxCrsDist

        if 'metalDist' in resDict.keys():
            metalDist = float(resDict['metalDist'])
            # print(resID,'has metal dist', metalDist)
        if 'crystal_contact_distance' in resDict.keys():
            crsDist = float(resDict['crystal_contact_distance'])
            # print(resID,'has crs dist', crsDist)
        # print('about to compare', metalDist, type(metalDist), 'and', crsDist, type(crsDist), '\n')
        contactDist = min(metalDist, crsDist)

        # NOTE: strictly for debugging
        assert(metalDist <= maxMetalDist and crsDist <= maxCrsDist)

        discrepDict[resID]['contact_distance'] = contactDist

    # Aggregate the final data into one big list (resultList).
    resultList = []
    for ((pdbID, _, _, _, _), residueDict) in discrepDict.items():
        absDiscrep = residueDict['num_electrons_actual_abs_significant_regional_discrepancy']
        nonabsDiscrep = residueDict['num_electrons_actual_significant_regional_discrepancy']

        # NOTE: This line is strictly for debugging
        # print('checking', pdbID)
        assert('contact_distance' in residueDict.keys())
        # print('finished checking', pdbID, '\n')

        contactDist = residueDict['contact_distance']
        
        # NOTE: This line is strictly for debugging
        assert(contactDist <= max(maxMetalDist,maxCrsDist))

        finalData = ','.join(str(val) for val in [pdbID, absDiscrep, nonabsDiscrep, contactDist])

        resultList.append(finalData)
    
    with open(resultFilePath, 'w') as resultFile:
        resultFile.write('\n'.join(resultList))

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


def getMetalDists(discrepDict:dict, metalNameList: list, pdbIDFilePath: str) -> dict:
    '''
    Add metal contact distances to the residues in discrepDict.

    :param discrepDict: dictionary of residues paired with basic info about them along with discrepancy data
    :param metalNameList: list of names of metals
    :param pdbIDFilePath: path to the file containing the list of PDB IDs
    '''

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
                prelimAtpResList = [res for res in resList if res.resname == 'ATP']

                # Filter out any ATP residues that are not in discrepDict.
                atpResList = []
                for res in prelimAtpResList:
                    resID = (pdbID, res.parent.parent.id, res.parent.id, res.resname, res.id[1])
                    if resID in discrepDict.keys():
                        atpResList.append(res)

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
                        resID = (pdbID, res.parent.parent.id, res.parent.id, res.resname, res.id[1])
                        discrepDict[resID]['metalDist'] = minDist
            
            else:
                print('no struct file for ' + pdbID)
            
    return discrepDict


def getCrsDists(crsDirPath, discrepDict):
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
                            discrepDict[residueID]['crystal_contact_distance'] = atomDict['crystal_contact_distance']
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

                    # print(f"discrepDict residueID: %s" % (residueID,))

                    discrepDict[residueID] = residueDict
    return discrepDict


if __name__ == '__main__':
    try:
        _, pdbIDFilePath, discrepDirPath, crsDirPath, resultFilePath, metalNameList, maxMetalDistStr, maxCrsDistStr = sys.argv
        main(pdbIDFilePath, discrepDirPath, crsDirPath, resultFilePath, metalNameList.split(','), float(maxMetalDistStr), float(maxCrsDistStr))
    except AssertionError:
        raise
    except Exception as e:
        print(e)
        print(__doc__)

