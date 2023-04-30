'''
Converts the PDB ID file taken from the PDB online database, into the format desired for this project. This format is such that each PDB ID resides on its own line in the file.

getIDFile.py rawIDFilePath finalIDFilePath
'''


import sys


def main(rawIDFilePath:str, finalIDFilePath:str) -> None:
    with open(rawIDFilePath, 'r') as rawIDFile, \
        open(finalIDFilePath, 'w') as finalIDFile:

        idList = rawIDFile.read().split(',')

        finalIDFile.write('\n'.join(idList))

    print('Finished running!')


if __name__ == '__main__':
    _,rawIDFilePath,finalIDFilePath = sys.argv

    main(rawIDFilePath,finalIDFilePath)
