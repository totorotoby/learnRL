import numpy as np
import random
import matplotlib.pyplot as plt
import sys

class instance:
	''' class for a single data point '''

	def __init__(self, attributes, label):

		self.attributes = attributes
		self.label = label

	def __str__(self):

		string = "attributes: " + str(self.attributes) + '\n'
		string += 'label' + str(self.label)

		return string

def genSamples(mean, cov, num):
	'''generates num number of samples from normal with mean and std'''
	print(cov)
	samples = np.random.multivariate_normal(mean,cov,num)
	samples = [[round(i,2) for i in samples[j]] for j in range(len(samples))]
	return samples


def genNdimSamples(mean, cov, num):
	'''generates N dimensional num samples from normal with mean and std as vectors'''

	return genSamples(mean, cov, num)



def getClassArray(i, lenClasses):
	''' just makes class array '''

	label = [0 for _ in range(lenClasses)]
	label[i] = 1
	return label



def genData(numClass, numSamples ,dim, meanRange, stdRange, covRange):
	'''
	generates numClass clumps of num samples with data in dim dimensions,
   	with means and stds ranging in meanRange and stdRange
	'''

	# generating all he data
	data = []
	for _ in range (numClass):

		mean = random.sample(range(-meanRange, meanRange), dim)

		cov = [[0 for _ in range(dim)] for _ in range(dim)]
		
		for i in range(dim):
			for j in range(i, dim):
				if i == j:
					cov[i][j] =  random.sample(range(1,stdRange), 1)[0]
				else:
					samp = random.sample(range(-covRange, covRange), 1)[0]
					cov[i][j] = samp
					cov[j][i] = samp

		#for row in cov:
		#	print(row)
		#print('\n\n\n')

		data.append(genNdimSamples(mean, cov, numSamples))

	# reformating to create instances
	classes = []
	for i in range(len(data)):
		cList = []
		label = getClassArray(i, len(data))

		for inst in data[i]:

			cList.append(instance(inst,label))

		classes.append(cList)

	return classes


def graphData(data, ax=None):
	'''
	graphs data points (only works for 2 diminesion data)
	'''
	
	if type(data) != list:
		if data.ndim > 1:
			data.ravel()
	else:
		data = sum(data,[])
	
	for inst in data:
		if ax == None:
			plt.plot(inst.attributes[0], inst.attributes[1], getColor(inst.label))
		else:
			ax.plot(inst.attributes[0], inst.attributes[1], getColor(inst.label))


	if ax == None:
		plt.show()
	else:
		return ax


def getColor(label):
	'''
	helper for plotting points with colors
	'''
	colors = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko']
	for i in range(len(label)):
		if label[i] == 1:
			return colors[i]



def writeData(data, filename):
	''' writes all instances in class order to csv
		att top of file can find:

		dim = 
		numClass = 
		numinstance=

		then single line is:
		 x_1, x_2 ... x_dim , l_1, l_2, ... l_numclass
	'''
	with open(filename, 'w+') as file:

		file.write('dim = ' + str(len(data[0][0].attributes)) + '\n')
		file.write('numclass = ' + str(len(data)) + '\n')

		for Class in data:
			for instance in Class:
				for attribute in instance.attributes:
					file.write(str(attribute) +',')
				for l in instance.label:
					file.write(str(l) + ',')
				file.write('\n')


def readData(filename):
	'''
	reads in data from format created in writeData
	'''
	with open(filename, 'r') as file:

		vars = []
		# getting variables for parsing data
		for _ in range(2):
			vars.append(int(file.readline().replace('\n', '').split('=')[1]))
		
		data=[]
	
		for line in file:
			# list magic to parse each line into arributes and labels
			attributes = [float(i) for i in line.split(',')[:vars[0]]]
			label = [int(i) for i in line.split(',')[vars[0]:vars[0] + vars[1]]]
			data.append(instance(attributes,label))

	data = np.array(data)

	return data, vars[0], vars[1]

def main():

	'''
	command line arguments:
	1. number of classes
	2. number of samples
	3. dimension of attributes
	4.range of means
	5. range of stds
	6. covarience matrix
	6. write flag
	7. write filename
	'''

	variables = [ int(i) for i in sys.argv[1:7]]
	
	data = genData(*variables)

	if sys.argv[7] == 'w':
		
		writeData(data, sys.argv[8])
	
	if variables[2] == 2:
		graphData(data)
		write = str(input('Save data? [y/n]\n'))
		if write == 'y':
			filename = str(input('Filename?\n'))
			writeData(data, filename)


#readData('test.txt')
if __name__ == '__main__':
	main()