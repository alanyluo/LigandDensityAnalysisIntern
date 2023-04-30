'''
Group the residues in the given hasMetal dataset into high positive (pos), high negative (neg), or neither (neutral).

group.py hasMetalsDataFilePath posFilePath negFilePath neuFilePath
'''


import sys
import pandas as pd
import math


def main(hasMetalsDataFilePath:str, posFilePath:str, negFilePath:str, neuFilePath:str) -> None:
    with open(hasMetalsDataFilePath, 'r') as  hasMetalsDataFile:

        # NOTE: dataList is a list of lists. Each sublist is the data for some residue.
        dataList = [resData.split(',') for resData in hasMetalsDataFile.readlines()]

        dataDF = pd.DataFrame(dataList, columns=['pdbid', 'absDiscrep', 'nonAbsDiscrep', 'metalDist']).astype({'absDiscrep': float, 'nonAbsDiscrep':float, 'metalDist':float})

        numResidues = len(dataDF.index)
        numOutliers = math.ceil(numResidues*0.01)
        outlierDF = dataDF.nlargest(numOutliers, 'absDiscrep')

        # print('sumAbsDiscrep', sumAbsDiscrep)
        # print('thresholdVal', thresholdVal)

        cutoffPercent = 0.5
        posDF = outlierDF[outlierDF['nonAbsDiscrep'] >= (cutoffPercent * outlierDF['absDiscrep'])]
        negDF = outlierDF[outlierDF['nonAbsDiscrep'] <= -1 * (cutoffPercent * outlierDF['absDiscrep'])]
        neuDF = outlierDF[(outlierDF['nonAbsDiscrep'] < (cutoffPercent * outlierDF['absDiscrep'])) & (outlierDF['nonAbsDiscrep'] > -1 * (cutoffPercent * outlierDF['absDiscrep']))]
        # neuDF = outlierDF - posDF - negDF

        # NOTE: for debugging purposes
        assert(len(outlierDF.index) == len(neuDF.index) + len(posDF.index) + len(negDF.index))

        # Write the data.
        # The first row and first column are both removed, as neither holds useful information.
        # First row holds the column labels, and first column holds the row labels.
        posDF.to_csv(posFilePath, index=False, header=False)
        negDF.to_csv(negFilePath, index=False, header=False)
        neuDF.to_csv(neuFilePath, index=False, header=False)


    print('Finished running!')



if __name__ == '__main__':
    _,hasMetalsDataFilePath,posFilePath,negFilePath,neuFilePath = sys.argv

    main(hasMetalsDataFilePath,posFilePath,negFilePath,neuFilePath)
