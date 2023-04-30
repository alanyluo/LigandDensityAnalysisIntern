'''
getMetalResults.py
    Get the spreadsheets for the metal datasets.

Usage: python3 getMetalResults.py <withinFilePath> <beyondFilePath> <datasetName>

Parameters:
    <withinFilePath> - file path to text file of within dataset
    <beyondFilePath> - file path to text file of beyond dataset
    <datasetName> - name of the dataset being run on (e.g. "first")

Example 1: python3 metalAnalysis/code/getMetalResults.py metalAnalysis/results/firstWithin.txt metalAnalysis/results/firstBeyond.txt first

Example 2: python3 metalAnalysis/code/getMetalResults.py metalAnalysis/results/secondWithin.txt metalAnalysis/results/secondBeyond.txt second

Example 3: python3 metalAnalysis/code/getMetalResults.py metalAnalysis/results/thirdWithin.txt metalAnalysis/results/thirdBeyond.txt third

    Run all three example commands in LigandDensityAnalysis.
'''


import sys
import xlsxwriter


def main(withinFilePath: str, beyondFilePath: str, datasetName: str) -> None:
    '''
    :param withinFilePath: path to text file containing within dataset
    :param beyondFilePath: path to text file containing beyond dataset
    :param datasetName: name of the dataset to be collected (e.g. "first")
    '''
    with open(withinFilePath, 'r') as withinFile, \
        open(beyondFilePath, 'r') as beyondFile:

        # NOTE: These are lists of lists.
        withinList = [line.rstrip('\n').split(',') for line in withinFile]
        beyondList = [line.rstrip('\n').split(',') for line in beyondFile]
    
    writeData(withinList, datasetName+'Within')
    writeData(beyondList, datasetName+'Beyond')

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
    _, withinFilePath, beyondFilePath, datasetName = sys.argv
    main(withinFilePath, beyondFilePath, datasetName)
