'''TODO (when time for codebase submission): Make this script's docstrings (including this one) widely-usable.

Perform the b-factor analysis.

A template of the command that you probably want to run (here, ATP is used as the target ligand):
% time python3 bfactorAnalysis/code/main.py globalData/standalone_atp_01-04-22 ATP 0.01 globalData/standalone_atp_01-04-22.txt globalData/structFiles_atp_01-04-22/ 0.5 checkAny 3.5 1> bfactorAnalysis/results/bfacATPOut.out 2> bfactorAnalysis/results/bfacATPErr.err

discrepDirPath,ligandName,outlierDef,pdbIDFilePath,structFileDirPath,rankCutoff,methodOption,distRadius
'''


import sys
import os
import json
import Bio.PDB as bioPDB
from pdb_eda.utils import _testXyzWithinDistance as checkTwoXyzs
import heapq
from scipy.stats import fisher_exact
import math


def main(discrepDirPath:str, ligandName:str,outlierDef:float,pdbIDFilePath:str,structFileDirPath:str,rankCutoff:float,methodOption:str,radiusCutoff:float) -> None:
    # Get the data.
    discrepDict = getDiscrepDict(discrepDirPath,ligandName)
    discrepDict = getbFactors(discrepDict, ligandName, pdbIDFilePath, structFileDirPath, rankCutoff, methodOption, radiusCutoff)
    discrepDict = getOutliers(discrepDict,outlierDef)
    
    # Filter out any residues that do not have b-factors.
    discrepDictItems = [(resID,resDict) for (resID,resDict) in discrepDict.items() if 'bfactor' in resDict.keys()]

    # Do the Fisher's test on these data.
    outlierAbove = len([resID for (resID,_) in discrepDictItems if discrepDict[resID]['outlier'] == 'outlier' and discrepDict[resID]['bfactor'] == 'above'])
    outlierBelow = len([resID for (resID,_) in discrepDictItems if discrepDict[resID]['outlier'] == 'outlier' and discrepDict[resID]['bfactor'] == 'below'])
    nonOutlierAbove = len([resID for (resID,_) in discrepDictItems if discrepDict[resID]['outlier'] == 'non-outlier' and discrepDict[resID]['bfactor'] == 'above'])
    nonOutlierBelow = len([resID for (resID,_) in discrepDictItems if discrepDict[resID]['outlier'] == 'non-outlier' and discrepDict[resID]['bfactor'] == 'below'])

    print('rankCutoff:',rankCutoff)
    totalNumSites = outlierAbove+nonOutlierAbove+outlierBelow+nonOutlierBelow
    print('totalNumSites:',totalNumSites)

    fisherTable = [[outlierAbove,nonOutlierAbove],[outlierBelow,nonOutlierBelow]]
    print('2x2 contingency table of the following form: [[outlierAbove,nonOutlierAbove], [outlierBelow, nonOutlierBelow]]')
    print(fisherTable)
    _,leftPVal = fisher_exact(fisherTable, alternative='less')
    print('left-sided p-value:', leftPVal)
    _,rightPVal = fisher_exact(fisherTable, alternative='greater')
    print('right-sided p-value:', rightPVal)

    print('Finished running!')


def getDiscrepDict(discrepDirPath:str, ligandName:str) -> dict:
    '''Return the discrepancy data referenced at discrepDirPath as a dictionary of residue dictionaries.

    :param discrepDirPath: path to the directory containing the discrepancy data
    :param ligandName: name of the ligand being analyzed
    '''
    discrepDict = dict()
    with os.scandir(discrepDirPath) as discrepDir:
        for dirEntry in discrepDir:
            with open(dirEntry, 'r') as discrepFile:
                # Recall that each discrepFile represents the discrepancy data for a unique PDB entry. So really, we are iterating over each PDB entry's dicsrepancy data.
                residueList = json.load(discrepFile)

                for residueDict in residueList:
                    modelID = '1' if 'model' not in residueDict.keys() else residueDict['model']
                    # TODO (when it is time to incorporate this as a public repo): Change the pdbidKey in the ATP discrepancy file so that 'pdbid' is used, not 'PDB ID'.
                    pdbidKey = 'PDB ID' if ligandName == 'ATP' else 'pdbid'
                    residueID = (residueDict[pdbidKey], modelID, residueDict['chain'], residueDict['residue_name'], residueDict['residue_number'])

                    discrepDict[residueID] = residueDict

    return discrepDict


def getbFactor(currAtom:bioPDB.Atom) -> float:
    '''
    Return the isotropic b-factor of currAtom.
    NOTE: This is a very simple function. However, it is needed for getFracRanking.
    '''
    return currAtom.get_bfactor()


def isWithinDist(atom:bioPDB.Atom, ligandAtomSet:set, radiusCutoff:float) -> bool:
    '''Return if atom is within radiusCutoff of any atoms in ligandAtomSet.

    :param atom: the current atom to be checked
    :param ligandAtomSet: the set of ligand atoms to which to compare atom
    :param radiusCutoff: the radius cutoff to be used
    '''
    return any(checkTwoXyzs(atom.get_coord(),ligandAtom.get_coord(),radiusCutoff) for ligandAtom in ligandAtomSet)


def getFracRanking(atomList:list) -> list:
    ''' Return the fractional ranking of atomList.'''
    ranking = enumerate(sorted(atomList, key=getbFactor))
    atomListSize = len(atomList)
    return [(rank/atomListSize, currAtom) for (rank,currAtom) in ranking]


def getbFactors(discrepDict:dict, ligandName:str, pdbIDFilePath: str, structFileDirPath:str, rankCutoff:float, methodOption:str, radiusCutoff:float) -> dict:
    '''Add b-factors to the residues in discrepDict.

    :param discrepDict: dictionary of residues paired with basic info about them along with discrepancy data
    :param ligandName: name of the ligand to search for
    :param pdbIDFilePath: path to the file containing the list of PDB IDs
    :param structFileDirPath: path to the directory containing the struct files for the ligand dataset
    :param rankCutoff: fractional ranking cutoff
    :param methodOption: which method to use for the analysis (ligandAny,ligandAvg,ligandPlusAny,ligandPlusAvg,otherAny,otherAvg)
    :param radiusCutoff: the desired search radius around the ligand atoms
    '''
    with open(pdbIDFilePath, 'r') as pdbIDFile:
        atomCountList = []
        for line in pdbIDFile:
            pdbID = line.lower().strip()
            structFilePath = structFileDirPath + 'pdb' + pdbID + '.ent'
            if os.path.isfile(structFilePath):
                bioPDBObj = bioPDB.PDBParser(QUIET=True).get_structure(pdbID, structFilePath)
                atomList = list(bioPDBObj.get_atoms())
                resList = list(bioPDBObj.get_residues())
                ligandResList = [res for res in resList if res.resname == ligandName]
                fracRanking = getFracRanking(atomList)
                atomCountList.append(len(atomList))

                for res in ligandResList:
                    resID = (pdbID, res.parent.parent.id, res.parent.id, res.resname, res.id[1])
                    if resID in discrepDict.keys():
                        ligandAtomSet = set(res.get_atoms())
                        ligandAtomSetSize = len(ligandAtomSet)
                        if methodOption.startswith('ligand') and not methodOption.startswith('ligandPlus'): ### case: ligand
                            if methodOption.endswith('Any'):
                                discrepDict[resID]['bfactor'] = 'above' if any(currAtom.parent == res and fracRank >= rankCutoff for (fracRank,currAtom) in fracRanking) else 'below'
                            else: ### case: ligandAvg
                                atomListSize = len(atomList)
                                avgRank = sum([fracRank for (fracRank,currAtom) in fracRanking if currAtom in ligandAtomSet]) / ligandAtomSetSize
                                discrepDict[resID]['bfactor'] = 'above' if avgRank >= rankCutoff else 'below'
                        elif methodOption.startswith('other'):
                            newAtomList = [currAtom for currAtom in atomList if isWithinDist(currAtom,ligandAtomSet,radiusCutoff)]
                            newAtomSet = set(newAtomList)
                            otherAtomSet = newAtomSet - ligandAtomSet
                            if methodOption.endswith('Any'):
                                discrepDict[resID]['bfactor'] = 'above' if any(currAtom in otherAtomSet and fracRank >= rankCutoff for (fracRank,currAtom) in fracRanking) else 'below'
                            else: ### case: otherAvg
                                otherAtomSetSize = len(otherAtomSet)
                                avgRank = sum([fracRank for (fracRank,currAtom) in fracRanking if currAtom in otherAtomSet]) / otherAtomSetSize
                                discrepDict[resID]['bfactor'] = 'above' if avgRank >= rankCutoff else 'below'
                        else: ### case: ligandPlus
                            newAtomList = [currAtom for currAtom in atomList if isWithinDist(currAtom,ligandAtomSet,radiusCutoff)]
                            newAtomSet = set(newAtomList)
                            if methodOption.endswith('Any'):
                                discrepDict[resID]['bfactor'] = 'above' if any(currAtom in newAtomSet and fracRank >= rankCutoff for (fracRank,currAtom) in fracRanking) else 'below'
                            else: ### case: ligandPlusAvg
                                newAtomSetSize = len(newAtomSet)
                                avgRank = sum([fracRank for (fracRank,currAtom) in fracRanking if currAtom in newAtomSet]) / newAtomSetSize
                                discrepDict[resID]['bfactor'] = 'above' if avgRank >= rankCutoff else 'below'
            else:
                print('no struct file:',pdbID)
        print('minAtomCount:',min(atomCountList))
        print('maxAtomCount:',max(atomCountList))

    return discrepDict


def getOutliers(discrepDict:dict, outlierDef:float) -> dict:
    '''
    Assign "outlier" or "non-outlier" to each residue in discrepDict.
    '''
    numResidues = len(discrepDict)
    numOutliers = math.ceil(numResidues*outlierDef)
    outlierDict = dict(heapq.nlargest(numOutliers, discrepDict.items(), key=lambda dictItem: dictItem[1]['num_electrons_actual_abs_significant_regional_discrepancy']))
    for resID,resDict in discrepDict.items():
        resDict['outlier'] = 'outlier' if resID in outlierDict else 'non-outlier'
    return discrepDict


if __name__ == '__main__':
    # TODO (when time for codebase submission): use doc.docopt to get the command-line arguments, and use a try-except block to catch a potential datatype mismatch when passing in these arguments into main() (e.g. strOutlierDef may not be parsible into a float, e.g. 'turtles' is not parsible into a float)
    _,discrepDirPath,ligandName,strOutlierDef,pdbIDFilePath,structFileDirPath,strRankCutoff,methodOption,strRadiusCutoff = sys.argv
    
    main(discrepDirPath,ligandName,float(strOutlierDef),pdbIDFilePath,structFileDirPath,float(strRankCutoff),methodOption,float(strRadiusCutoff))
