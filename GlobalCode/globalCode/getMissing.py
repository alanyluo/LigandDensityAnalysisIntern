'''
Get the PDB IDs of the PDB entries that were not acquired in the first collection of the regional discrepancy data.

getMissing.py allIDFilePath currDirPath errFilePath resFilePath
'''


import sys
import os


def main(allIDFilePath:str, currDirPath:str, errFilePath:str, resFilePath:str) -> None:
    with open(allIDFilePath, 'r') as allIDFile, \
        open(errFilePath, 'r') as errFile, \
        open(resFilePath, 'w') as resFile, \
        os.scandir(currDirPath) as currDir:

        allIDSet = set([line.rstrip('\n') for line in allIDFile])
        errIDSet = set([line[:4] for line in errFile if 'Error:' in line or 'Timeout' in line])
        currIDSet = set([file.name[:4] for file in currDir])
        noSet = currIDSet | errIDSet

        missingIDList = [fullID for fullID in allIDSet if fullID not in noSet]

        resFile.write('\n'.join(missingIDList))

    print('Finished running!')


if __name__ == '__main__':
    _,allIDFilePath,currDirPath,errFilePath,resFilePath = sys.argv

    main(allIDFilePath,currDirPath,errFilePath,resFilePath)
