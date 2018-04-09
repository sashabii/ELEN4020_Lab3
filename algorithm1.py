from mrjob.job import MRJob
from mrjob.step import MRStep
import os
import re

import time
startTime = time.time()

# Setting input file names
matrixFile1 = 'matrix1.txt'
matrixFile2 = 'matrix2.txt'

class Algorithm1(MRJob):

    # Mapping function
    def mapFn(self, _, data):
        row, col, value = data.split()
        value = float(value)
        filename = os.environ['map_input_file']
        if filename == '.\\' + matrixFile1:
            yield col, (0, row, value)
        elif filename == '.\\' + matrixFile2:
            yield row,(1,col,value)
            

    # Reduce function
    def reduceFn(self, y, values):
        rowVals = []
        colVals = []
        for x in values:
            if x[0] == 0:
                rowVals.append(x)
            if x[0] == 1:
                colVals.append(x)
   
        for (a, b, row) in rowVals:
            for (a, key, col) in colVals:
                yield (b, key), int(row)*int(col)
                

    # Key-value pair generation
    def keyValPair(self, key, value):
        yield key, value

    # Addition for calculation
    def addition(self, key, values):
        yield key, sum(values)

    # 'steps' function to run algorithms
    def steps(self):
        print("---- %s seconds ----" % (time.time() - startTime))
        return [MRStep(mapper=self.mapFn,
                        reducer=self.reduceFn),
                MRStep(mapper=self.keyValPair,
                        reducer=self.addition)]                
        
        
Algorithm1.run()