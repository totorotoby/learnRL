#N outside packages
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import sys


# my modules
import GenerateNormalData as Gendata

def threshold(inp, thresh):
	'''
	threshold function
		parameters:
		inp    : the number to threshold
		thresh : the threshold
	'''

	if inp >= threshold:
		return 1
	else:
		return 0

def mapRegion(x, nMax, nMin):
	'''
	maps all points in x into new range max and min
	'''
	
	return [((x_i - min(x)) * (nMax-nMin) / max(x)-min(x)) + nMin for x_i in x]


def sigmoid(x):
	'''
	sigmoid funcition from n to n dimensions
	'''
	#x = mapRegion(x, 8, -8)

	out = [1/(1 + np.exp(-point)) for point in x]

	return out


def compMax(input):
	'''
	changes output of each perceptron into a [0,0,0,1] like label
	by making the maximum a 1 and everyting else a 0
	'''
	
	out = [0 for _ in range(len(input))]

	index = np.argmax(input)
	out[index] = 1

	return out


def percepOut(x, w_i, b_i):
	'''
	function that returns output of perceptron i on a single instance x:
	parameters:
	w_i    : the current weights of this perceptron
	b_i    : the current bias of this perceptron
	x      : the instance
	thresh : threshold for hardlim

	returns:
	y_i  : the predicted value of perceptron i

	'''
	return w_i @ x + b_i

def networkOut(x, W, B):
	'''
	same as percept out but just does for entire W
	'''

	return W @ x + B

def nomCost(l_i,y_i):
	'''
	Subraction Cost function:
	parameters:
	l_i : the value of label at i
	y_i : the predicted value of label at i

	returns:
	the difference between the two
	'''

	return l_i-y_i


def trainSPSI(i, w_i, b_i, x, y_t, cost, lRate):
	'''trains a single perceptron for a single instance

		parameters:
		i    : the number perceptron being trained
		w_i  : the current weights of this perceptron
		b_i  : the current bias of this perceptron
		x    : the single instance that is used for training (includes label (example [0,0,1,0]))
		y_t  : the predicted label (example [0,1,0,0])
		cost : the cost function that will be used
		lRate: the learning rate

		returns:
		w_i: the updated weight values for this perceptron
		b_i: the updated bias value for this perceptron

	'''
	# predicted value for this perceptron
	y_it = y_t[i]
	# the actual value of label for this perceptron
	l_i = x.label[i]

	# for each weight of this perceptron
	for j in range(len(w_i)):

		# the new weight is old weight plus the learning rule
		w_i[j] = w_i[j] + (lRate * cost(l_i,y_it) * x.attributes[j])
	
	# the bias is the old bias plus learning rule
	b_i = b_i + (lRate * cost(l_i,y_it))

	return w_i, b_i

def trainNetwork(W, B, Y, data, cost, lRate):

	'''
	Does a single round of training on network with everything in data:

		parameters:
		W     : the weight matrix (rows are indexed by i, columns are indexed by j)
		B     : the bias vector (rows are indexed by i, no columns)
		Y     : the list of predicted labels (indexed by t number of instances)
		data  : the full set of instances (x's) that will be trained on
		cost  : the cost function used to train
		lRate : the learning rate of training

		returns:
		W: the weight matrix but updated with new w_ij's
		B: the bias matrix but with updated b_i's
	'''

	# for each perceptron
	for i in range(len(W)):
		# for each instance in data
		for t in range(len(data)):
			# update that perceptron using that training instance
			W[i], B[i] = trainSPSI(i, W[i], B[i], data[t], Y[t], cost, lRate)

	return W, B


def Classify(W, B, data):

	'''
	Classifies each instance in data
	Parameters:
	W     : the weight matrix (rows are indexed by i, columns are indexed by j)
	B     : the bias vector (rows are indexed by i, no columns)
	data  : the full set of instances (x's) that will be trained on

	Returns:
	Y     : the a list of all predicted classes for each instance

	'''

	Y = []

	# setting threshold value
	threshold = 0
	# for each instance
	for t in range(len(data)):
		#for each perceptron
		value = networkOut(data[t].attributes, W, B)
		Y.append(compMax(value))

	return Y
		

def accuracy(label, Y):
	'''
	give percentage of predictions that are right
	'''
	right = 0
	for t in range(len(label)):
		if label[t] == Y[t]:
			right += 1

	return right/len(label)



def KlabelClassifyer(data, dataBounds, dim, numClass, lRate, accuracyThresh):

	'''
	trains network till a certain accuracy give a data set
	Parameters:
	data           : data to train on
	dim            : dimensions of data
	numClass       : number of classes to choose from
	lRate          : learning rate
	accuracyThresh : threshold to achieve before training is over
	'''

	# make sure that data array is 1d
	if data.ndim != 1:
		data.ravel()

	# starting accuracy
	ac = 0

	# randomly intizalzing W and B
	W = np.random.rand(numClass, dim)
	B = np.random.rand(1, numClass)
	B = B[0]
	
	# array to collect lines to be graphed
	if dim == 2:
		graphLines = []
	else:
		graphLines = None


	while ac < accuracyThresh:

		#shuffle data
		np.random.shuffle(data)

		# classify data
		Y  = Classify(W, B, data)

		W, B = trainNetwork(W, B, Y, data, nomCost, lRate)

		ac = accuracy([inst.label for inst in data], Y)

		if dim == 2:
			graphLines.append(collectGraphData(W,B, dataBounds))

		print(ac)

	return W,B, graphLines


def getDataBounds(data, dim):

	if dim == 2:

		bounds = np.array([[max([x.attributes[i] for x in data]) for i in range(dim)], [min([x.attributes[i] for x in data]) for i in range(dim)]])
		bounds =bounds.T

		return bounds

	return None




def collectGraphData(W,B, dataBounds):

	linePoints = []

	for i in range(len(W)):
		linePoints.append(getPoints(*getLine(W[i],B[i]), dataBounds))

	return linePoints

def getLine(w_i, b_i):
	''' 
	returns slope and intercept of line

	'''
	# to find the slope of the boundary 
	try:
		slope = w_i[0]/w_i[1]
		inter = b_i

	except ZeroDivisionError:
		slope = None
		inter = b_i/[0]

	return slope, inter

def getPoints(slope, intercept, dataBounds):
	'''
	returns 2 points on each line that are at the bounds,
	so that 2Dline object can be created
	'''
	if slope != None:

		x1 = dataBounds[0]
		x2 = []

		for bound in dataBounds[0]:
			x2.append(slope*bound + intercept)

	else:

		x1 = [intercept,intercept]
		x2 = dataBounds[1]

	return [x1, x2]


def plotLine(x,y):
	'''Plots a line with known slope and intercept in x1Bounds and x2Bounds range'''

	plt.axhline(y=0, color='k')
	plt.axvline(x=0, color='k')

	plt.plot(x, y, '--')


def updatefig(i, ax, lineGraphs, data):

	#Gendata.graphData(data)
	ax.clear()
	lines = []
	for j in range(len(lineGraphs[i])):
		lines.append(ax.plot(lineGraphs[j][0], lineGraphs[j][1]))

	return lines

def makeAnimation(data, lineGraphs):

	fig, ax = plt.subplots()
	
	mation = animation.FuncAnimation(fig, updatefig, len(lineGraphs), fargs=(ax, lineGraphs, data))

	plt.show()


def showPlotTimeStep(data, lineGraphs, index):

	fig, ax = plt.subplots()

	colors = ['b-', 'g-', 'r-', 'c-', 'm-', 'y-', 'k-']
	ax = Gendata.graphData(data, ax)

	count = 0 
	for line in lineGraphs[index]:
		ax.plot(line[0], line[1], colors[count])
		count += 1 

	plt.show()


def main():
	'''
	commandline arguments:
	1. filename
	'''

	filename = sys.argv[1]

	data, dim, numClass = Gendata.readData(filename)

	dataBounds = getDataBounds(data, dim)

	W, B, lineGraphs = KlabelClassifyer(data, dataBounds, dim, numClass, .5, 1)

	#confused and buggy...
	#makeAnimation(data, lineGraphs)
	Gendata.graphData(data)
	showPlotTimeStep(data, lineGraphs, len(lineGraphs)-2)
	showPlotTimeStep(data, lineGraphs, len(lineGraphs)-1)
		


main()
