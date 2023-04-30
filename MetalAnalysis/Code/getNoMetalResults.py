'''
getNoMetalResults.py
    Get the spreadsheets for the metal datasets.

Usage: python3 getNoMetalResults.py <resultFilePath> <datasetName>

Parameters:
    <resultFilePath> - file path to text file of the result dataset
    <datasetName> - name of the dataset being run on (e.g. "first")

Example 1: python3 metalAnalysis/code/getNoMetalResults.py metalAnalysis/results/firstNoMetals.txt firstNoMetals

Example 2: python3 metalAnalysis/code/getNoMetalResults.py metalAnalysis/results/secondNoMetals.txt secondNoMetals

Example 3: python3 metalAnalysis/code/getNoMetalResults.py metalAnalysis/results/thirdNoMetals.txt thirdNoMetals

    Run all three example commands in LigandDensityAnalysis.
'''


import sys
import xlsxwriter


def main(resultFilePath: str, datasetName: str) -> None:
    '''
    :param resultFilePath: path to text file containing result dataset
    :param datasetName: name of the dataset to be collected (e.g. "first")
    '''
    with open(resultFilePath, 'r') as resultFile:

        # NOTE: This is a list of lists.
        resultList = [line.rstrip('\n').split(',') for line in resultFile]
    
    writeData(resultList, datasetName)

    print('Finished running!')


def writeData(dataList: list, outFileName: str) -> None:
    '''
    Write the data stored in dataList into a spreadsheet with the name outFileName.

    :param dataList: list of the desired data to be written
    :param outFileName: name of the spreadsheet to be made
    '''
    outFilePath = 'metalAnalysis/results/' + outFileName + '.xlsx'
    with xlsxwriter.Workbook(outFilePath) as workbook:
        worksheet = workbook.add_worksheet()
        worksheet.write(0,0,'PDB ID')
        worksheet.write(0,1,'Absolute Significant Observed Discrepancy')
        worksheet.write(0,2,'Significant Observed Discrepancy')
        worksheet.write(0,3,'Minimum Metal Distance')

        currRow = 1
        for [pdbID, absDiscrep, nonabsDiscrep, metalDist] in dataList:
            worksheet.write(currRow,0,pdbID)
            worksheet.write(currRow,1,float(absDiscrep))
            worksheet.write(currRow,2,float(nonabsDiscrep))
            worksheet.write(currRow,3,float(metalDist))
            currRow += 1
        assert(len(dataList) == (currRow-1))


if __name__ == '__main__':
    _, resultFilePath, datasetName = sys.argv
    main(resultFilePath, datasetName)
