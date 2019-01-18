# outside packages
import numpy as np
import matplotlib.pyplot as plt
import random

# my modules
import GenerateNormalData as data


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

def percepOut(x, w_i, b_i, thresh):
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
	return threshold(w_i @ x + b_i, thresh)


def nomCost(l_i,y_i):
	'''
	Subraction Cost function:
	parameters:
	l_i : the value of label at i
	y_i : the predicted value of label at i

	returns:
	the difference between the two
	'''

	return r-y


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
		# place holder for new class
		pLabel = []
		#for each perceptron
		for i in range(len(W)):
			pLabel.append(percepOut(data[i].attributes, W[i], B[i], threshold))

		#add label to total labels	
		Y.append(pLabel)






#def KlabelClassifyer(data):































def graphBoundaries(w_i, b_i, x1Bounds, x2Bounds):
	''' graphs a boundaries for each perceptron '''

	to_graph = []

	# for each perceptron
	for j in range(len(w_i)):
		points = []

		# to to find the slope of the boundary 
		try:
			slope = w_i[j][0]/w_i[j][1]
			inter = b_i[j]
		except ZeroDivisionError:
			slope = None
			inter = b_i[j]/w_i[j][0]

		plotLine(slope, inter, x1Bounds, x2Bounds)		



def plotLine(slope, intercept, x1Bounds, x2Bounds):
	'''Plots a line with known slope and intercept in x1Bounds and x2Bounds range'''

	plt.axhline(y=0, color='k')
	plt.axvline(x=0, color='k')

	# if the line is not vertical
	if slope != None:
		x2Vals = intercept + slope * x1Bounds
		plt.plot(x1Bounds, x2Vals, '--')
    # if the line is vertical
	else:
		x1Vals = [intercept,intercept]
		plt.plot(x1Vals, x2Bounds, '--')




# plots the data and the current dividing lines only for 2d
#def plot():













'''
def e42_44():

	##########################

	#def vecs
	p_list = [[pd.Series([-1,1]), 0], [pd.Series([-1,-1]), 0], [pd.Series([1,0]), 1], [pd.Series([1,1]), 1], [pd.Series([-.5, 1]), 1], [pd.Series([-.75, -.75]),1]]
	num_tests = len(p_list)
	
	#inital weights
	w = pd.Series([-.1, .1])
	#intial bias
	b = .1


	convergent = False

	while not convergent:


		train_class = []
		random.shuffle(p_list)

		for i in range(num_tests):

			#print(w)
			#print(b)

			result = classify(p_list[i][0],w,b)
			train_class.append(result)
			w, b = train(w, b, p_list[i][0], p_list[i][1], result)
			

			# convergent condition
			if i == num_tests - 1:
				count = 0
				for j in range(num_tests):
					if train_class[j] == p_list[j][1]:
						print(train_class, [p[1] for p in p_list], j)
						count += 1

				if count == num_tests:
					print(count)
					convergent = True


		boundary = getBoundary(w,b)
		plot(p_list, w, boundary)
'''	
