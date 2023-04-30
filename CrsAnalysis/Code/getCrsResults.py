'''
TODO: clean up

Get the spreadsheets for the four datasets (i.e. within_3_5, within_10, between_3_5_10, and beyond_10).

Command: python3 code/getCrsResults.py within35FilePath betweenFilePath within10FilePath beyond10FilePath
'''


import sys
import xlsxwriter


def writeData(dataList, outFileName):
    '''
    Write the data stored in dataList into a spreadsheet with the name outFileName.
    '''
    outFilePath = 'results/' + outFileName + '.xlsx'
    with xlsxwriter.Workbook(outFilePath) as workbook:
        worksheet = workbook.add_worksheet()
        worksheet.write(0,0,'PDB ID')
        worksheet.write(0,1,'Absolute Significant Observed Discrepancy')
        worksheet.write(0,2,'Significant Observed Discrepancy')

        currRow = 1

        if outFileName != 'beyond10':
            worksheet.write(0,3,'Minimum Crystal Contact Distance')
            for [pdbID, absDiscrep, nonabsDiscrep, crsDist] in dataList:
                worksheet.write(currRow,0,pdbID)
                worksheet.write(currRow,1,float(absDiscrep))
                worksheet.write(currRow,2,float(nonabsDiscrep))
                worksheet.write(currRow,3,float(crsDist))
                currRow += 1

        else:
            for [pdbID, absDiscrep, nonabsDiscrep] in dataList:
                worksheet.write(currRow,0,pdbID)
                worksheet.write(currRow,1,float(absDiscrep))
                worksheet.write(currRow,2,float(nonabsDiscrep))
                currRow += 1
        
        assert(len(dataList) == (currRow-1))


def main():
    # Retrieve the data from within_3_5, between_3_5_10, and within_10 files.
    within35FilePath = sys.argv[1]
    betweenFilePath = sys.argv[2]
    within10FilePath = sys.argv[3]
    beyond10FilePath = sys.argv[4]

    with open(within35FilePath, 'r') as within35File, \
        open(betweenFilePath, 'r') as betweenFile, \
        open(within10FilePath, 'r') as within10File, \
        open(beyond10FilePath, 'r') as beyond10File:

        # NOTE: These are lists of lists.
        within35List = [line.rstrip('\n').split(',') for line in within35File]
        betweenList = [line.rstrip('\n').split(',') for line in betweenFile]
        within10List = [line.rstrip('\n').split(',') for line in within10File]
        beyond10List = [line.rstrip('\n').split(',') for line in beyond10File]
    
    # Write these data into a spreadsheet.
    writeData(within35List, 'within35')
    writeData(within10List, 'within10')
    writeData(betweenList, 'between')
    writeData(beyond10List, 'beyond10')

    print('Finished running!')
    return 0


if __name__ == '__main__':
    main()
