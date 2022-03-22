#!/usr/bin/python3
#© Butnariu Bogdan-Mihai
from collections import defaultdict
import sys
  
graph = defaultdict(set)

def parseFile(file):
    with open(file) as f:
        lines = f.readlines()

    for i in range(3, len(lines)):
        listOfNumbers = lines[i].split(sep=" ")
        graph[int(listOfNumbers[0])].add(int(listOfNumbers[1]))
        graph[int(listOfNumbers[1])].add(int(listOfNumbers[0]))

    return int(lines[0]), int(lines[1]), int(lines[2])    

def cliques_recursive(clique, vertexes):
    if not vertexes:
        yield clique

    else:
        for vertex in min((vertexes - graph[u] for u in vertexes), key=len):
            yield from cliques_recursive(clique | {vertex}, vertexes & graph[vertex])
            vertexes.remove(vertex)

def kCliques(k):
    for clique in cliques_recursive(set(), set(graph)):
        if len(clique) >= k:
            return True
    return False

if __name__ == '__main__':
    k, v, numOfEdges = parseFile(sys.argv[1])
    print(kCliques(k))