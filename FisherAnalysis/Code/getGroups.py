'''
Print out the aggregate of all the given group datasets.

getGroups.py group1.txt,group2.txt,group3.txt,....
'''


import sys


def main(groupPathList:list) -> None:
    groupList = []
    # count = 0
    for groupPath in groupPathList:
        with open(groupPath, 'r') as groupFile:
            rawLineList = groupFile.readlines()

            lineList = [line.rstrip('\n') for line in rawLineList]
            
            # NOTE: for debugging purposes
            # if count==0:
            #     print('non-processed list')
            #     print(rawLineList)
            #     print('\n')

            #     print('processed list')
            #     print(lineList)
            #     print('\n')
            #     count += 1

            groupList += lineList

    # print('next line is for debugging')
    # print(type(finalTable))



    print('\n'.join(groupList))

    # print('Finished running!')


if __name__ == '__main__':
    _,groupPathsStr = sys.argv
    
    main(groupPathsStr.split(','))
