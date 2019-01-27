import sys
import numpy as np
import GenerateNormalData as gnd


def sortData(data):
	'''
	sorts data by labels and returns it as list of lists
	'''

	newList = []
	seen = []

	for instance in data[0]:
		if instance.label not in seen:
			#add it to the check list
			seen.append(instance.label)
			#make a new row in newList add the instance to it and put it in newList
			newRow = []
			newRow.append(instance)
			newList.append(newRow)

		else:
			index = seen.index(instance.label)
			newList[index].append(instance)

	return newList

def single_multinorm_logLike(classInstances):

	'''
	finds the maximum likelyhood parameters for a single bivariate normal distrubiton
	with no correlation at all
	'''
	instanceAtts = [inst.attributes for inst in classInstances]
	At_matrix = np.transpose(instanceAtts)
	
	numAtt = len(instanceAtts[0])
	numInst = len(instanceAtts)

	#for instance in instanceAtts:
		#print(instance)

	Means = []
	Covs = [[0 for _ in range(numAtt)] for _ in range(numAtt)]

	#means
	for i in range(numAtt):
		Means.append(sum(At_matrix)/numInst)

	#covariances
	cov = np.cov(At_matrix)
	
	print(cov)



	return Means, Covs


def probClass(sortedData):
	'''
	returns estimated as uniform probability of being in class
	'''
	return [len(Class)/len(sortedData) for Class in sortedData]




def main():
	
	data = gnd.readData(sys.argv[1])
	anws = str(input('Would you like to graph the data? [y/n]\n'))
	if anws == 'y':
		gnd.graphData(data[0])





	data = sortData(data)

	for Class in data:
		single_multinorm_logLike(Class)

main()