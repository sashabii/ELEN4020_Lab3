from mrjob.job import MRJob
from mrjob.step import MRStep
import os

# Setting input file names
matrixFile1 = 'matrix1.txt'
matrixFile2 = 'matrix2.txt'

class Algorithm2(MRJob):

    # Mapping function
    def mapFn(self, _, data):

        splitData = data.split()

        # Extracting matrix dimensions from first line of files
        if len(splitData) == 2:
            global matrixACols

            filename = os.environ['map_input_file']
            if filename == '.\\' + matrixFile1:
                matrixARows = splitData[0]
                matrixACols = splitData[1]
                return
            else:
                matrixBRows = splitData[0]
                return


        row, col, value = data.split()
        matrixAData = []
        matrixBData = []

        filename = os.environ['map_input_file']
        if filename == '.\\' + matrixFile1:
            matrixAData.append((row, col, value))
            for a in range(matrixBRows):
                yield (row,a),(0,col,value)
        elif filename == '.\\' + matrixFile2:
            matrixBData.append((row, col, value))
            for a in range(matrixARows):
                yield (a,col),(1,row,value)

    # Reduce funtion
    def reduceFn(self, y, values):
        global matrixACols

        rowVals =[]
        colVals =[]
        ansVals=[]
        for a in values:
            if a[0] == 0:
                rowVals.append(a[2])
            else:
                colVals.append(a[2])

        # Transposition Calculation
        for a in range(0,matrixACols):
           ansVals.append(rowVals[a]*colVals[a])

        yield y, sum(ansVals)
    
    # 'steps' function to run algorithms
    def steps(self):
        print("---- %s seconds ----" % (time.time() - startTime))
        return [MRStep(mapper=self.mapFn,
                        reducer=self.reduceFn))] 

Algorithm2.run()