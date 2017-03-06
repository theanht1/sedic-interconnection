# Systax: python [filename] [Node] [xSize] [r0] [r1] ... [rn]
# This tool is used for Grid graph.


from igraph import*
import sys
import random
import math
import time
# import xml.etree.cElementTree as ET

def main():
    beginTime = time.clock() # Check begin time
    # 1. Checking parameters
    if(len(sys.argv) < 4):
        print("Systax Error! Lack of parameters!")
        return 0
    else:
        Node = int(sys.argv[1])
        numberRandomLink = len(sys.argv) - 3

    # 2. Setting parameters
    xSize = int(sys.argv[2])
    if(xSize > 1):
        xSize = xSize
        ySize = Node / xSize
        if(ySize == int(ySize)):
            ySize = int(Node / xSize)
        else:
            ySize = int(Node / xSize) + 1
    else:
        xSize = math.sqrt(Node)
        if(xSize == math.floor(xSize)):
            xSize = int(xSize)
        else:
            xSize = int(math.sqrt(2 * Node))
        ySize = int(Node / xSize)
    Node = xSize * ySize
    diameter = xSize + ySize
    print("Grid " + str(xSize) + "x" + str(ySize))
    print("Diameter: " + str(diameter))
    print("Number of random link: " + str(numberRandomLink))
    if (Node % 2 == 0):
        outlink = 0
        print("Number of out link: 0")
    else:
        outlink = 1
        print("Number of out link: 1")

    # 3. Building Grid
    # 3.1 Base Grid
    grid = Graph()
    grid.add_vertices(Node)
    for i in range(Node):
        col = i % xSize
        row = int(i / xSize)
        if((col < (xSize - 1)) and (row < (ySize - 1))):
            grid.add_edges([(i, nodeIndex(row, (col + 1) % xSize, xSize)), (i, nodeIndex((row + 1) % ySize, col, xSize))])
        if((col == (xSize - 1)) and (row < (ySize - 1))):
            grid.add_edges([(i, nodeIndex((row + 1) % ySize, col, xSize))])
        if((row == (ySize - 1)) and (col < (xSize - 1))):
            grid.add_edges([(i, nodeIndex(row, (col + 1) % xSize, xSize))])

    # 4.2 Print edges file
    f_edges = open("network_generator/results/sw_2DGrid_n" + str(Node) + "xSize" + str(xSize) + "_r" + str(numberRandomLink) + ".edges", "w")
    f_edges.write(str(Node) + " " + str(len(grid.get_edgelist())) + " " + str(numberRandomLink) + "\n")
    for i in range(Node):
        for j in grid.neighbors(i):
            if i < j:
                f_edges.write(str(i) + " " + str(j) + "\n")


    # 3.2 Add random links
    THRESHOLD = 100
    for i in range(numberRandomLink): #  Implement for per random link
        #fi = open("listr" + str(i), "w") # Output file for per random link
        a = float(sys.argv[i + 3]) # Load power of random link
        f_edges.write(str(int(Node / 2)) + " " + str(a) + "\n")
        for u in range(outlink, Node): # Implement for per node
            if(grid.degree(u) >= (1 + nodeDegree(u, xSize, ySize) + i)):
                continue
            isStop = 0
            while(grid.degree(u) < (1 + nodeDegree(u, xSize, ySize) + i)):
                count = 0
                ui = u % xSize
                uj = int(u / xSize)
                C = 0  # Kleiberg constant
                for n in range(outlink, Node):
                    if(n != u):
                        C += pow(nodeDistance(u, n, xSize, ySize), -a)
                Cdd = [] # Candidate node list of per source U
                # Cdd[i] = Pr(u -> i) = 1/C * pow(d(u,i), -r)
                # Cdd[i] = 0 if degree(i) is full
                for v in range(outlink, Node):
                    if ((v == u) or (grid.degree(v) == (1 + nodeDegree(v, xSize, ySize) + i))):
                        Cdd.append(0)
                    else:
                        pv = 1 / C * math.pow(nodeDistance(u, v, xSize, ySize), -a)
                        Cdd.append(pv)
                S=0
                for x in Cdd:
                    S+=x
                rd = float(random.randint(0, int(1000000 * S)) / 1000000) # Check random number to find destination V for U
                for s in range(len(Cdd)): # Find destination V min with 0 < rd < Cdd[0] + Cdd[1] + ... + Cdd[v]
                    rd -= Cdd[s]
                    if(rd < 0):
                        if(Cdd[s] == 0): # Cdd[s] = 0 <=> Pr(u -> s) = 0 <=> u = s
                            while(Cdd[s] == 0):
                                s = s - 1 + outlink
                                if(Cdd[s] != 0):
                                    v = s
                                    break
                        else:
                            v = s + outlink
                        break
                if ((v != u) and (grid.degree(v) < (1 + nodeDegree(v, xSize, ySize) + i)) and (grid.neighbors(u).count(v) == 0)):
                    grid.add_edges([(u, v)])
                    f_edges.write(str(u) + " " + str(v) + "\n")
                    count += 1
                end1Time = time.clock() # Check time to restart program if too long
                '''if(end1Time - beginTime >= 6): # time to counting loop
                    print("Out of expect time. Program is restarting!")
                    return 0'''
                if(count == 1): break

                isStop += 1
                if isStop > THRESHOLD:
                    break

        print("Complete graph with r" + str(i))
    #end2Time = time.clock() # time to counting building graph
    #timeBuilding = end2Time - beginTime
    #print("Time to building Graph is: " + str(timeBuilding) + " second")

    # 4. Print result
    print("----------------------------")
    print(grid)

    # 4.1 Print geos file
    f_geos = open("network_generator/results/sw_2DGrid_n" + str(Node) + "xSize" + str(xSize) + "_r" + str(numberRandomLink) + ".geos", "w")
    f_geos.write(str(Node) + "\n")
    for i in range(Node):
        f_geos.write(str(i) + " " + str(i % xSize) + " " + str(int(i / xSize)) + "\n")
    f_geos.close()



    print("Export data to:\n")
    print("sw_2DGrid_n" + str(Node) + "_xSize" + str(xSize) + "*" + str(ySize) + "_r" + str(numberRandomLink) + ".geos")
    print("sw_2DGrid_n" + str(Node) + "xSize" + str(xSize) + "_r" + str(numberRandomLink) + ".edges")
    print("----------------------------")
    end3Time = time.clock() # timepoint to counting program time
    timeExe = end3Time - beginTime
    print("Time to run program is: " + str(timeExe) + " second")
    return 1


def nodeIndex(row, col, n):
    return row * n + col

def nodeDistance(u, v, x, y):
    ui = u % x
    uj = int(u / x)
    vi = v % x
    vj = int(v / x)
    di = abs(ui - vi)
    dj = abs(uj - vj)
    return di+dj

def nodeDegree(n, x, y):
    ni = n % x
    nj = int(n / x)
    deg = 4
    if((ni == 0) or (ni == x - 1)):
        deg -= 1
    if((nj == 0) or (nj == y - 1)):
        deg -= 1
    return deg

main()

'''while(1):
    A = main()
    if(A == 0):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    if(A == 1):
        break'''
