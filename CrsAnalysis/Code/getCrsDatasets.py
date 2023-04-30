'''
TODO: clean up

Get the within_3_5, between_3_5_10, within_10, and beyond_10 datasets.

Command: python3 code/getCrsDatasets.py discrepDirPath within35DirPath within10DirPath beyond10FilePath betweenFilePath within35FilePath within10FilePath
'''


import os
import sys
import json


def getDiscrepDict():
    '''
    Return the discrepancy data as a dictionary of residue dictionaries.
    '''
    discrepDict = dict()
    discrepDirPath = sys.argv[1]
    with os.scandir(discrepDirPath) as discrepDir:
        for dirEntry in discrepDir:
            with open(dirEntry, 'r') as discrepFile:
                # Recall that each discrepFile represents the discrepancy data for a unique PDB entry. So really, we are iterating over each PDB entry's dicsrepancy data.
                residueList = json.load(discrepFile)

                for residueDict in residueList:
                    residueID = (residueDict['PDB ID'], residueDict['model'], residueDict['chain'], residueDict['residue_name'], residueDict['residue_number'])

                    discrepDict.update({residueID:residueDict})
    return discrepDict


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


def main():
    # Get the discrepancy data as a dictionary of dictionaries discrepDict.
    discrepDict = getDiscrepDict()

    # Add crystal contact distances to discrepDict.
    within35DirPath = sys.argv[2]
    discrepDict = updateDiscrepDict(within35DirPath, discrepDict)
    within10DirPath = sys.argv[3]
    discrepDict = updateDiscrepDict(within10DirPath, discrepDict)

    # Get the datasets.
    beyond10FilePath = sys.argv[4]
    betweenFilePath = sys.argv[5]
    within35FilePath = sys.argv[6]
    within10FilePath = sys.argv[7]
    with open(beyond10FilePath, 'w') as beyond10File, \
        open(betweenFilePath, 'w') as betweenFile, \
        open(within35FilePath, 'w') as within35File, \
        open(within10FilePath, 'w') as within10File:

        within35List = []
        within10List = []
        betweenList = []
        beyond10List = []
        
        for ((pdbID, _, _, _, _), residueDict) in discrepDict.items():
            absDiscrep = residueDict['num_electrons_actual_abs_significant_regional_discrepancy']
            nonabsDiscrep = residueDict['num_electrons_actual_significant_regional_discrepancy']

            if 'crystal_contact_distance' not in residueDict.keys():
                beyond10List.append(','.join(str(val) for val in [pdbID, absDiscrep, nonabsDiscrep]))
            else:
                crsData = ','.join(str(val) for val in [pdbID, absDiscrep, nonabsDiscrep, residueDict['crystal_contact_distance']])

                within10List.append(crsData)

                if residueDict['crystal_contact_distance'] > 3.5:
                    betweenList.append(crsData)
                else:
                    within35List.append(crsData)
        
        within35File.write('\n'.join(within35List))
        betweenFile.write('\n'.join(betweenList))
        within10File.write('\n'.join(within10List))
        beyond10File.write('\n'.join(beyond10List))

    print('Finished running!')
    return 0


if __name__ == '__main__':
    main()
