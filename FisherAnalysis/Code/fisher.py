'''
TODO: clean up this script

Perform the Fisher's test on the given contact dataset.

Usage: fisher.py <contactDataExcelFile> <outlierDef> <contactID> <distCutoff>
    contactID = 'c' if crystal contact, 'm' if metal contact, 'b' if any

Example 1: py fisherAnalysis/code/fisher.py fisherAnalysis/results/summer2022/metalAnalysis/all/mg.xlsx 0.01 m 3.5

Example 2: py fisherAnalysis/code/fisher.py fisherAnalysis/results/summer2022/crsContactAnalysis/all.xlsx 0.01 c 3.5

Example 3: python3 fisherAnalysis/code/fisher.py fisherAnalysis/results/both.xlsx 0.01 b 3.5
'''


import sys
import pandas as pd
import math
from scipy.stats import fisher_exact
# import os


def main(excelFilePath:str, outlierDef:float, contactID:str, distCutoff:float) -> None:
    '''
    :excelFilePath str: path to the Excel file containing the contact dataset
    :outlierDef float: float denoting the percentage to be used to define what an outlier is
    :contactID str: str representing the type of the contact data being processed
    :distCutoff float: float representing the distance cutoff used to distinguish between "close" and "non-close" contact distances
    '''
    contactType = 'Minimum Crystal Contact Distance' if contactID=='c' else 'Minimum Metal Distance' if contactID=='m' else 'Contact Distance'
    
    df = pd.read_excel(excelFilePath, engine='openpyxl').astype({'Absolute Significant Observed Discrepancy': float, 'Significant Observed Discrepancy':float, contactType: float})

    numResidues = len(df.index)
    numOutliers = math.ceil(numResidues*outlierDef)

    # Get the dfs containing just the outlier data, and the non-outlier data.
    outlierDF = df.nlargest(numOutliers, 'Absolute Significant Observed Discrepancy')
    nonOutlierDF = df.nsmallest(numResidues-numOutliers, 'Absolute Significant Observed Discrepancy')

    # Uncomment this to print out an entire dataframe.
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        # print(df)
        # print('outliers',outlierDF)
        # print('closeoutliers',outlierDF[outlierDF[contactType] < distCutoff])
    
    outlierClose = len(outlierDF[outlierDF[contactType] < distCutoff].index)
    outlierNonClose = len(outlierDF[outlierDF[contactType] > distCutoff].index)
    nonOutlierClose = len(nonOutlierDF[nonOutlierDF[contactType] < distCutoff].index)
    nonOutlierNonClose = len(nonOutlierDF[nonOutlierDF[contactType] > distCutoff].index)
    
    fisherTable = [[outlierClose,nonOutlierClose], [outlierNonClose, nonOutlierNonClose]]
    print('2x2 contingency table of the following form: [[outlierClose,nonOutlierClose], [outlierNonClose, nonOutlierNonClose]]')
    print(fisherTable)
    # print('outlier count:', outlierClose+outlierNonClose)
    # print('non-outlier count:', nonOutlierClose+nonOutlierNonClose)
    # print('total count:', outlierClose+outlierNonClose+nonOutlierClose+nonOutlierNonClose)
    # _,twoPVal = fisher_exact(fisherTable)
    # print('two-tailed p-value:', twoPVal)
    _,leftPVal = fisher_exact(fisherTable, alternative='less')
    print('left-sided p-value:', leftPVal)
    _,rightPVal = fisher_exact(fisherTable, alternative='greater')
    print('right-sided p-value:', rightPVal)

    print('Finished running!')


if __name__ == '__main__':
    _,excelFilePath,outlierDefStr,contactID,distCutoffStr = sys.argv
    main(excelFilePath, float(outlierDefStr), contactID, float(distCutoffStr))
