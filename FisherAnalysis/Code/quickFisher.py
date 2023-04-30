'''
Perform the Fisher's test for left and right-tailed p-values.
'''


import sys
import ast
from scipy.stats import fisher_exact


def main(fisherTableFilePath:str) -> None:
    with open(fisherTableFilePath, 'r') as fisherTableFile:
        fileLines = fisherTableFile.readlines()
        fisherTable = ast.literal_eval(fileLines[0])

    print('2x2 contingency table of the following form: [[outlierClose,nonOutlierClose], [outlierNonClose, nonOutlierNonClose]]')
    print(fisherTable)
    _,leftPVal = fisher_exact(fisherTable, alternative='less')
    print('left-sided p-value:', leftPVal)
    _,rightPVal = fisher_exact(fisherTable, alternative='greater')
    print('right-sided p-value:', rightPVal)
    
    print('Finished running!')


if __name__ == '__main__':
    _,fisherTableFilePath = sys.argv
    main(fisherTableFilePath)
