'''
Perform the Fisher's exact test needed for the group analysis. This test is still the Fisher's exact test, except that the parameters required are now different. Instead of taking in an outlier definition, this script always compares the top 1% to the rest of the 99%. So, outlier is always defined as top 1%.

groupFisher.py fullDataExcelFilePath outlierDataExcelFilePath distCutoff
'''


import sys
import pandas as pd
import math
from scipy.stats import fisher_exact


def main(fullDataExcelFilePath:str, outlierDataExcelFilePath:str, distCutoff:float) -> None:
    outlierDF = pd.read_excel(outlierDataExcelFilePath, engine='openpyxl').astype({'Absolute Significant Observed Discrepancy': float, 'Significant Observed Discrepancy':float, 'Minimum Metal Distance':float})

    fullDF = pd.read_excel(fullDataExcelFilePath, engine='openpyxl').astype({'Absolute Significant Observed Discrepancy': float, 'Significant Observed Discrepancy':float, 'Minimum Metal Distance':float})

    numResidues = len(fullDF.index)
    numNonOutliers = math.ceil(0.99*numResidues)
    nonOutlierDF = fullDF.nsmallest(numNonOutliers, 'Absolute Significant Observed Discrepancy')

    outlierClose = len(outlierDF[outlierDF['Minimum Metal Distance'] < distCutoff].index)
    outlierNonClose = len(outlierDF[outlierDF['Minimum Metal Distance'] > distCutoff].index)
    nonOutlierClose = len(nonOutlierDF[nonOutlierDF['Minimum Metal Distance'] < distCutoff].index)
    nonOutlierNonClose = len(nonOutlierDF[nonOutlierDF['Minimum Metal Distance'] > distCutoff].index)
    
    fisherTable = [[outlierClose,nonOutlierClose], [outlierNonClose, nonOutlierNonClose]]
    print('2x2 contingency table of the following form, where "target" means the kind of outlier in question (e.g. 1% positive): [[targetClose,nonOutlierClose], [targetNonClose, nonOutlierNonClose]]')
    print(fisherTable)

    _,leftPVal = fisher_exact(fisherTable, alternative='less')
    print('left-sided p-value:', leftPVal)
    _,rightPVal = fisher_exact(fisherTable, alternative='greater')
    print('right-sided p-value:', rightPVal)

    print('Finished running!')


if __name__ == '__main__':
    _,fullDataExcelFilePath,outlierDataExcelFilePath,distCutoffStr = sys.argv
    main(fullDataExcelFilePath,outlierDataExcelFilePath,float(distCutoffStr))
