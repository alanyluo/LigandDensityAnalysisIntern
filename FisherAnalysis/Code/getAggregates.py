'''
Print out the aggregate of all the given Fisher's test tables.

getAggregates.py table1.txt,table2.txt,table3.txt,....
'''


import sys
import numpy as np
from functools import reduce


def main(tablePathList:list) -> None:
    tableList = []
    for tablePath in tablePathList:
        with open(tablePath, 'r') as tableFile:
            tableLinesRaw = tableFile.readlines()
            if len(tableLinesRaw) == 5:
                tableLine = tableLinesRaw[1].rstrip('\n').replace('[', '').replace(']', '')
                currTable = np.fromstring(tableLine, sep=',')
                currTable = currTable.reshape((2,2))
                tableList.append(currTable)
    
    finalTable = reduce(lambda x, y:x+y, tableList)

    # TODO: Comment these two lines out once you've confirmed that finalTable is as expected.
    # print('next line is for debugging')
    # print(type(finalTable))

    print(finalTable.tolist())

    print('Finished running!')


if __name__ == '__main__':
    _,tablePathsStr = sys.argv
    
    main(tablePathsStr.split(','))
