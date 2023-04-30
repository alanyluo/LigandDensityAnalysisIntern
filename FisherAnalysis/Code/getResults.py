'''
TODO: clean up

getResults.py
    Get the spreadsheet for a contact distance dataset.

Usage: python3 getResults.py <contactDataFilePath> <outName> <contactType>

Parameters:
    <contactDataFilePath> - file path to text file of contact dataset

Example: python3 fisherAnalysis/code/getResults.py fisherAnalysis/results/hasMetalsMg.txt hasMetalsMg m

    Run this example commands in LigandDensityAnalysis.
'''


import sys
import xlsxwriter


def main(contactDataFilePath: str, outFilePath:str, contactType:str) -> None:
    '''
    :param contactDataFilePath: path to text file containing both dataset
    :param outName: name of the Excel file to be produced
    :param contactType: name of the type of contact data
    '''
    with open(contactDataFilePath, 'r') as contactFile:
        # NOTE: These are lists of lists.
        dataList = [line.rstrip('\n').split(',') for line in contactFile]
        writeData(dataList, outFilePath, contactType)

    print('Finished running!')


def writeData(dataList: list, outFilePath: str, contactType:str) -> None:
    '''
    Write the data stored in dataList into a spreadsheet with the name outFileName.

    :param dataList: list of the desired data to be written
    :param outFileName: name of the spreadsheet to be made
    :param contactType: name of the type of contact data
    '''
    with xlsxwriter.Workbook(outFilePath) as workbook:
        worksheet = workbook.add_worksheet()
        worksheet.write(0,0,'PDB ID')
        worksheet.write(0,1,'Absolute Significant Observed Discrepancy')
        worksheet.write(0,2,'Significant Observed Discrepancy')
        
        contactTitle = 'Minimum Metal Distance' if contactType=='m' else 'Minimum Crystal Contact Distance' if contactType=='c' else 'Contact Distance'
        worksheet.write(0,3,contactTitle)

        currRow = 1
        for [pdbID, absDiscrep, nonabsDiscrep, contactDist] in dataList:
            worksheet.write(currRow,0,pdbID)
            worksheet.write(currRow,1,float(absDiscrep))
            worksheet.write(currRow,2,float(nonabsDiscrep))
            worksheet.write(currRow,3,float(contactDist))
            currRow += 1
        assert(len(dataList) == (currRow-1))


if __name__ == '__main__':
    _, contactDataFilePath, outName, contactType = sys.argv
    main(contactDataFilePath, outName, contactType)
