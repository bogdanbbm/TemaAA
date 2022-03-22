#!/usr/bin/python3
#© Butnariu Bogdan-Mihai
import sys

def parseFile(file):
    with open(file) as f:
        lines = f.readlines()

    lst = []
    matrix = []
    for i in range(0, int(lines[1])):
        for j in range(0, int(lines[1])):
            lst.append(0)
        matrix.append(lst)
        lst = []

    for i in range(3, len(lines)):
        listOfNumbers = lines[i].split(sep=" ")
        matrix[int(listOfNumbers[0]) - 1][int(listOfNumbers[1]) - 1] = 1 
        matrix[int(listOfNumbers[1]) - 1][int(listOfNumbers[0]) - 1] = 1

    return int(lines[0]), int(lines[1]), int(lines[2]), matrix    

def SAT(matrix, k, v):
    strToReturn = ''

    #1
    for i in range(1, k + 1):
        for j in range(1, k + 1):
            for v in range(1, v + 1):
                if i != j:
                    strToReturn = strToReturn + '(~x' + str(i) + str(v) + 'V~x' + str(j) + str(v) + ')^'

    #2
    for i in range(1, k + 1):
        for j in range(1, k + 1):
            for v in range(1, v + 1):
                for u in range(1, v + 1):
                    if matrix[v - 1][u - 1] == 0 and u != v:
                        strToReturn = strToReturn + '(~x' + str(i) + str(v) + 'V~x' + str(j) + str(u) + ')^'

    #3
    for i in range(1, k + 1): #1
        strToReturn = strToReturn + '('
        for v in range(1, v + 1):
            strToReturn = strToReturn + 'x' + str(i) + str(v) + 'V'

        strToReturn = strToReturn[:-1]
        strToReturn = strToReturn + ')^'
    
    strToReturn = strToReturn[:-1]
    
    return strToReturn

if __name__ == '__main__':
    k, v, numOfEdges, matrix = parseFile(sys.argv[1])
    satStr = SAT(matrix, k, v)
    print(satStr)