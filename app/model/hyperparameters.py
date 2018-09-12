class HyperParameters(object):

	def __init__(self):
		self.momentum = 0.9
		self.hidden_layer_count = 5
		self.convolution_kernel_count = 75
		self.convolution_kernel_size = (4, 4)
		self.regularization_constant = 0.0001
		self.learning_rate = 0.1