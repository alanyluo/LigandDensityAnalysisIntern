'''
TODO: make this script more usable in the real world

Get the spreadsheet for the noCrs dataset.

Command: python3 crsContactAnalysis/code/getNoCrsResults.py crsContactAnalysis/results/noCrs.txt
'''


import sys
import xlsxwriter


def writeData(dataList, outFileName):
    '''
    Write the data stored in dataList into a spreadsheet with the name outFileName.
    '''
    outFilePath = 'crsContactAnalysis/results/' + outFileName + '.xlsx'
    with xlsxwriter.Workbook(outFilePath) as workbook:
        worksheet = workbook.add_worksheet()
        worksheet.write(0,0,'PDB ID')
        worksheet.write(0,1,'Absolute Significant Observed Discrepancy')
        worksheet.write(0,2,'Significant Observed Discrepancy')

        currRow = 1
        worksheet.write(0,3,'Minimum Crystal Contact Distance')
        for [pdbID, absDiscrep, nonabsDiscrep, crsDist] in dataList:
            worksheet.write(currRow,0,pdbID)
            worksheet.write(currRow,1,float(absDiscrep))
            worksheet.write(currRow,2,float(nonabsDiscrep))
            worksheet.write(currRow,3,float(crsDist))
            currRow += 1
        assert(len(dataList) == (currRow-1))


def main():
    # Retrieve the data from the result file.
    resultFilePath = sys.argv[1]
    with open(resultFilePath, 'r') as resultFile:
        # NOTE: These is a list of lists.
        resultList = [line.rstrip('\n').split(',') for line in resultFile]
    
    # Write these data into a spreadsheet.
    writeData(resultList, 'noCrs')

    print('Finished running!')
    return 0


if __name__ == '__main__':
    main()
