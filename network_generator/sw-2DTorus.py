#Systax: python [filename] [Node] [xSize] [p1] [p2] ... [pn]

from igraph import*
import sys
import random
import math
import time
# import xml.etree.cElementTree as ET

def main():
    beginTime = time.clock()
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
    diameter = int((xSize + ySize) / 2)
    print("Torus " + str(xSize) + "x" + str(ySize))
    print("Diameter: " + str(diameter))
    print("Number of random link: " + str(numberRandomLink))
    if (Node % 2 == 0):
        outlink = 0
        print("Number of out link: 0")
    else:
        outlink = 1
        print("Number of out link: 1")

    # 3. Building Torus
    # 3.1 Base Torus
    tor = Graph()
    tor.add_vertices(Node)
    for i in range(Node):
        col = i % xSize
        row = int(i / xSize)
        tor.add_edges([(i, nodeIndex(row, (col + 1) % xSize, xSize)), (i, nodeIndex((row + 1) % ySize, col, xSize))])
    # 3.2 Add random links
    THRESHOLD = 100
    for i in range(numberRandomLink):
        fi = open("network_generator/results/listr" + str(i), "w")
        # fi.write("Random links of r" + str(i) + ":\n")
        a=float(sys.argv[i+3])
        C=0
        for n in range(1,Node):
            C+=pow(nodeDistance(0,n,xSize,ySize), -a)
        for u in range(outlink, Node):
            if(tor.degree(u) >= 5 + i):
                continue
            #print('u='+str(u))
            willBreak = 0
            while(tor.degree(u) < 5 + i):
                count = 0
                ui = u % xSize
                uj = int(u / xSize)
                Cdd = []
                for v in range(outlink, Node):
                    if (v == u):
                        Cdd.append(0)
                    else:
                        pv = 1 / C * math.pow(nodeDistance(u, v, xSize, ySize), -a)
                        Cdd.append(pv)
                #print(Cdd)

                rd = float(random.randint(int(1000000*min(Cdd)), 1000000) / 1000000)
                #print(rd)
                for s in range(len(Cdd)):
                    rd-=Cdd[s]
                    if(rd<0):
                        if(Cdd[s]==0):
                            v=s-1+outlink
                        else:
                            v=s+outlink
                        break
                #print("v=")
                #print(v)
                if ((v!=u) and (tor.degree(v) < 5 + i) and (tor.get_edgelist().count((u, v)) == 0) and (tor.get_edgelist().count((v, u)) == 0)):
                    tor.add_edges([(u, v)])
                    fi.write(str(u) + "\t" + str(v) + "\n")
                    count+=1
                #else: continue
                # endTime = time.cslock()
                # if(endTime - beginTime >= 6):
                #     print("Out of expect time. Program is restarting!")
                #     return 0
                if(count == 1): break

                willBreak += 1
                if willBreak > THRESHOLD:
                    break
        print("Complete graph with r" + str(i))

    # 4. Print result
    print("----------------------------")
    print(tor)

    # 4.1 Print geos file
    f_geos = open("network_generator/results/sw_2DTorus_n" + str(Node) + "xSize" + str(xSize) + "_r" + str(numberRandomLink) + ".geos", "w")
    # f_geos.write("Torus " + str(Node) + "=" + str(xSize) + "col" + "*" + str(ySize) + "row" + "\n")
    for i in range(Node):
        f_geos.write(str(i) + "\t" + str(i % xSize) + "\t" + str(int(i / xSize)) + "\n")
    f_geos.close()

    # 4.2 Print edges file
    f_edges = open("network_generator/results/sw_2DTorus_n" + str(Node) + "xSize" + str(xSize) + "_r" + str(numberRandomLink) + ".edges", "w")
    for i in range(Node):
        col = i % xSize
        row = int(i / xSize)
        for j in range(i,Node):
            if (tor.get_edgelist().count((i, j)) == 1):
                f_edges.write(str(i) + "\t" + str(j) + "\n")

    print("Export data to:\n")
    print("sw_2DTorus2_n" + str(Node) + "xSize" + str(xSize) + "_r" + str(numberRandomLink) + ".geos")
    print("sw_2DTorus_n" + str(Node) + "xSize" + str(xSize) + "_r" + str(numberRandomLink) + ".edges")
    print("----------------------------")
    return 1


def nodeIndex(row, col, n):
    return row * n + col

def nodeDistance(u, v, x, y):
    ui = u % x
    uj = int(u / x)
    vi = v % x
    vj = int(v / x)
    if (abs(ui - vi) <= int(x / 2)):
        di = abs(ui - vi)
    else:
        di = x - abs(ui - vi)
    if (abs(uj - vj) <= int(y / 2)):
        dj = abs(uj - vj)
    else:
        dj = y - abs(uj - vj)
    return di+dj

while(1):
    A = main()
    if(A == 0):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    if(A == 1):
        break
