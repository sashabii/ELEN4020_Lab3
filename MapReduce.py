from mrjob.job import MRJob
from mrjob.step import MRStep
import os


class Algorithm1(MRJob):

    # Mapping function
    def mapFn(self, _, line):
        row, col, value = line.split()
        value = float(value)
        filename = os.environ['map_input_file']
        if filename == '.\matrix1.txt':
            yield col, (0, row, value)
        elif filename == '.\matrix2.txt':
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
        return [MRStep(mapper=self.mapFn,
                        reducer=self.reduceFn),
                MRStep(mapper=self.keyValPair,
                        reducer=self.addition)]

Algorithm1.run()