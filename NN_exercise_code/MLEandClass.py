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
	'''
	instanceAtts = [inst.attributes for inst in classInstances]
	At_matrix = np.transpose(instanceAtts)
	
	numAtt = len(instanceAtts[0])
	numInst = len(instanceAtts)


	Means = []

	#means
	for i in range(numAtt):
		Means.append(sum(At_matrix[i])/numInst)

	#covariances
	Covs = np.cov(At_matrix)

	return Means, Covs


def probClass(sortedData):
	'''
	returns estimated as uniform probability of being in class
	'''
	return [len(Class)/len(sortedData) for Class in sortedData]


def predict(estParams, instance):
	'''
	predicts which class a data point will be in from using the enstimated parameters from 
	labeled data. Using Ethem Alpaydin page 101, but would be interesting to just use
	numpy pdfs.
	'''

	







def main():
	
	data = gnd.readData(sys.argv[1])
	anws = str(input('Would you like to graph the data? [y/n]\n'))
	if anws == 'y':
		gnd.graphData(data[0])


	data = sortData(data)



	# getting all estimated parameters for multi variate distributions
	# TODO something is messed up with the covariences
	probClasses = probClass(data)
	estDistParam = []
	for Class in data:
		estDistParam.append(single_multinorm_logLike(Class))


main()