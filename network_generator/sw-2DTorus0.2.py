########################################
# Create by NguyenTT on 23.Feb.2016
# Updated on 21.April.2016
# This tool help to
# 1. Generate Smallworld datacenter topology with 2D-Torus as based-line. power 1.6
#	+ n node
#	+ r: number of random-links per node
# sw-2DTorus.py [n] [ar]
# Output: Edges files of topology.
#####################################

import re
import string
import sys
import math
import pprint
import random
import Queue


##--------MAIN FUNCTION-----------
def main():
	# 1. Checking syntax
	if len(sys.argv) <= 1:
		print 'Syntax error. Lack of parameters:'
		return

	# 2. Get the argument	
	totalNode = int(sys.argv[1])
	numberOfRandomLink = 2	
	if len(sys.argv) >= 3:
		numberOfRandomLink = int(sys.argv[2])
		
	xSize = 1
	ySize = 1
	xSize = math.sqrt(totalNode)
	if xSize == math.floor(xSize):
		xSize = int(xSize)
	else:
		xSize = int(math.sqrt(totalNode*2))
	ySize = totalNode/xSize
	gridDiameter = (xSize + ySize)/2
	print xSize
	print ySize
	print gridDiameter
	print numberOfRandomLink
	numberOutRandomLink = int(round(numberOfRandomLink/2))
	print numberOutRandomLink
	# 3. Build baseline graph
	#3.1. Initiallize
	THRESH_HOLE = 5
	currentGraph = {}
	freeInport = []
	missingNode = []
	CDF = []
	CDF.append(0)
	C = 1/(math.log(totalNode,2))
	for i in range(1,gridDiameter): #CDF[1] = Pr(d=2), CDF[2] = Pr(d=2) + Pr(d=3)
		candidate = candidates_at_distance({'X':0,'Y':0},i+1,xSize,ySize)
		CDF.append(CDF[i-1] + C*len(candidate)/pow((i+1),1.6))  #there are 4d nodes has distance d like this in 2D-grid
	print CDF
		
	for i in range(0,totalNode):
		currentGraph[i] = []
		freeInport.append(numberOutRandomLink)
	
	#3.2. Add links
	for i in range(0,totalNode):
		node = index_2_node(i,xSize,ySize)
		print "-----------------------------"
		print i, node
		#3.2.1 Regular 2DTorus links: x direction
		if node['X'] < xSize - 1:
			nextNode = {'X':node['X'] + 1, 'Y': node['Y']}
			nextIdx = node_2_index(nextNode,xSize,ySize)
			currentGraph = add_link(i,nextIdx,currentGraph)			
		else: # equals to xSize-1
			nextNode = {'X':0, 'Y': node['Y']}
			nextIdx = node_2_index(nextNode,xSize,ySize)
			currentGraph = add_link(i,nextIdx,currentGraph)			
		
		#3.2.2 Regular 2DTorus links: y direction 
		if node['Y'] < ySize - 1:
			nextNode = {'X':node['X'], 'Y': node['Y'] + 1}
			nextIdx = node_2_index(nextNode,xSize,ySize)
			currentGraph = add_link(i,nextIdx,currentGraph)			
		else: # equals to ySize-1
			nextNode = {'X': node['X'], 'Y':  0}
			nextIdx = node_2_index(nextNode,xSize,ySize)
			currentGraph = add_link(i,nextIdx,currentGraph)			

		#3.3. Random links (2k random links/node. k link out and k link in)
		# Probability of given {u,v| distance(u,v) = d} have link is pr(u-->v) = (logn)^-1 * d^(-2)
		# Method:
		# + Step 1: Generate a Cumulative Distribution Function
		#			CDF(r) = Pr(d=2) + Pr(d=3) +... + Pr(d=r+1) with r>=1
		# + Step 2: Search in CDF
		# 			Pick up a uniform random value v for node i in range of (0,max_of_CDF))
		# 			distance d is smallest number that  CDF(d) >= v > CDF(d-1) 
		# Random select a node from nodes which has distance to i = d
		for outlink in range(0,numberOutRandomLink):		
			count = 0
			while count < THRESH_HOLE:		
				randomValue =  random.uniform(0.0, CDF[len(CDF)-1])
				distance = len(CDF)-1 #default value in case of bad floating point accuracy
				for index in range(0,len(CDF)):
					upper = CDF[index]
					if upper >= randomValue:
						distance = index + 1
						break			
				#print randomValue
				#print distance
				candidates = candidates_at_distance(node,distance,xSize,ySize)
				#print candidates
				while len(candidates)>0:
					randomIdx = random.randint(0,len(candidates)-1)
					destIdx = candidates[randomIdx]
					if (destIdx <> i) and (freeInport[destIdx] > 0) and (destIdx not in currentGraph[i]):
						#connect link
						currentGraph = add_link(i,destIdx,currentGraph)
						#print "Add link " + str(i) + "-" + str(destIdx)
						freeInport[destIdx] = freeInport[destIdx] - 1
						break
					else:
						del candidates[randomIdx]
						
				if len(candidates) == 0:
					count = count + 1
				else:
					break
			
			if count >= THRESH_HOLE:	
				print "Warning: miss random link for " + str(i)
				missingNode.append(i)
	print missingNode
	print freeInport
	#3.3 connect available outport (missingNode) with freeInport
	for inPortIdx in range(0,len(freeInport)-1):
		if freeInport[inPortIdx] > 0:
			if(len(missingNode) > 0):
				sourceIdx = missingNode[len(missingNode)-1]
				currentGraph = add_link(sourceIdx,inPortIdx,currentGraph)
				del missingNode[len(missingNode)-1]
			else:
				break
	
	#4. Add node by node into graph
	# while True:
		# print "$$$$$$$$$$$$$$$$$$" 
		# print currentGraph
		# newGraph = add_a_node(currentGraph,maxDiameter,maxDegree)
		# if newGraph == False:
			# break
		# else:
			# currentGraph = newGraph
	#5. Print result
	print "$$$$$$$$$$$$$$$$$$"
	total_link = 0
	distance_range = {}
	for i in range (0, len(currentGraph)):
		linksOfI = currentGraph[i]
		for j in range(0,len(linksOfI)):
			if linksOfI[j] > i:
				total_link += 1
				distance = node_distance(i,linksOfI[j],xSize,ySize)
				if distance not in distance_range:
					distance_range[distance] = 1
				else:
					distance_range[distance] += 1
	for i in distance_range:
		print str(i) + ": " + str(int(distance_range[i])) + " - " + str(float(distance_range[i])*100/total_link)
	print distance_range
	print total_link
	print "$$$$$$$$$$$$$$$$$$" 
	#print currentGraph
	print "Latest number of node " + str(len(currentGraph))
	outputFileName = "sw_2DTorus0.2_n" + str(len(currentGraph)) + "_r" + str(numberOfRandomLink) + ".edges"
	write_links(outputFileName,currentGraph)
	outputFileName = outputFileName.replace(".edges",".geo")
	write_geoIndex(outputFileName,totalNode,xSize,ySize)

def candidates_at_distance(node,distance,xSize,ySize):
	candidates = []
	maxX = xSize/2
	if distance < maxX:
		maxX = distance
	maxY = ySize/2
	minX = distance - maxY
	if minX < 0:
		minX = 0
	for x in range(minX,maxX+1):
		canIdx = node_2_index({"X": (node["X"] + x)%xSize,"Y": (node["Y"] + distance - x)%ySize},xSize,ySize)
		if canIdx not in candidates:
			candidates.append(canIdx)
		canIdx = node_2_index({"X": (node["X"] + x)%xSize,"Y": (node["Y"] - distance + x)%ySize},xSize,ySize)
		if canIdx not in candidates:
			candidates.append(canIdx)
		canIdx = node_2_index({"X": (node["X"] - x)%xSize,"Y": (node["Y"] + distance - x)%ySize},xSize,ySize)
		if canIdx not in candidates:
			candidates.append(canIdx)
		canIdx = node_2_index({"X": (node["X"] - x)%xSize,"Y": (node["Y"] - distance + x)%ySize},xSize,ySize)
		if canIdx not in candidates:
			candidates.append(canIdx)
	return candidates
	
def node_2_index(node,xSize,ySize):
	index = int(node['Y']) * xSize + int(node['X'])
	return index

def index_2_node(index,xSize,ySize):
	x = index % xSize
	y = index / xSize
	node = {'X':x,'Y':y}
	return node
	
def	node_distance(nodeIdx1,nodeIdx2,xSize,ySize):
	node1 = index_2_node(nodeIdx1,xSize,ySize)
	node2 = index_2_node(nodeIdx2,xSize,ySize)
	distance = 0
	xDistance = (node1['X'] - node2['X'])%xSize
	if xDistance > xSize/2:
		distance += xSize - xDistance
	else:
		distance += xDistance
	yDistance = (node1['Y'] - node2['Y'])%ySize
	if yDistance > ySize/2:
		distance += ySize - yDistance
	else:
		distance += yDistance
	return distance

def write_geoIndex(outputFileName,totalNode,xSize,ySize):
	outputFileName = 'network_generator/results/' + outputFileName
	print 'Write geoIndix into ' + outputFileName
	fo = open(outputFileName, "w")
	option = "T_" + str(totalNode) + "_" + str(xSize) + "_" + str(ySize) + "\r\n"
	# fo.writelines(option)
	for i in range(0,totalNode):
		node = node = index_2_node(i,xSize,ySize)
		line = str(i) + ' ' + str(node['X']) + ' ' + str(node['Y']) + "\r\n"
		fo.writelines(line)
	fo.close()
		
##-----------GENERAL FUNCTION--------	
def add_link(idx1,idx2,links):
	#print "add link " + str(idx1) + "_" + str(idx2)
	if idx1 not in links.keys():
		links[idx1] = []
		
	if idx2 not in links.keys():
		links[idx2] = []
	
	links[idx1].append(idx2)
	links[idx2].append(idx1)

	return links
	
def add_directed_link(idx1,idx2,links):
	print "add directed link " + str(idx1) + "_" + str(idx2)
	if idx1 not in links.keys():
		links[idx1] = []
	links[idx1].append(idx2)

	return links	

def remove_link(idx1,idx2,links):
	for idx,item in enumerate(links[idx1]):
		if item == idx2:
			del links[idx1][idx]
			break
			
	for idx,item in enumerate(links[idx2]):
		if item == idx1:
			del links[idx2][idx]
			break
	return links

def write_links(outputFileName,links):
	outputFileName = 'network_generator/results/' + outputFileName
	print 'Write links into ' + outputFileName
	fo = open(outputFileName, "w")
	for i in range (0, len(links)):
		linksOfI = links[i]
		for j in range(0,len(linksOfI)):
			if linksOfI[j] > i:
				line = str(i) + ' ' + str(linksOfI[j]) + "\r\n"
				fo.writelines(line)
	fo.close()

main()
