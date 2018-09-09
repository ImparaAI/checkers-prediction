import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential, load_model
from keras.models import Model as KerasModel
from keras.layers import Input, Dense, Conv2D, Flatten, BatchNormalization, Activation, LeakyReLU, add
from keras.optimizers import SGD
from keras import regularizers
import keras.backend as K
import tensorflow as tf


def softmax_cross_entropy_with_logits(y_true, y_pred):

	p = y_pred
	pi = y_true

	zero = tf.zeros(shape = tf.shape(pi), dtype=tf.float32)
	where = tf.equal(pi, zero)

	negatives = tf.fill(tf.shape(pi), -100.0)
	p = tf.where(where, negatives, p)

	loss = tf.nn.softmax_cross_entropy_with_logits(labels = pi, logits = p)

	return loss

class Model():

	def __init__(self, reg_const, learning_rate, input_dim, output_dim, hidden_layers):
		self.momentum = 0.9
		self.reg_const = reg_const
		self.learning_rate = learning_rate
		self.input_dim = input_dim
		self.output_dim = output_dim
		self.hidden_layers = hidden_layers
		self.num_layers = len(hidden_layers)
		self.model = self.build()

	def predict(self, x):
		return self.model.predict(x)

	def train(self, inputs):
		return 'training is happening'

	def build(self):
		main_input = Input(shape = self.input_dim, name = 'main_input')

		x = self.build_convolutional_layer(main_input, self.hidden_layers[0]['filters'], self.hidden_layers[0]['kernel_size'])

		if len(self.hidden_layers) > 1:
			for h in self.hidden_layers[1:]:
				x = self.build_residual_layer(x, h['filters'], h['kernel_size'])

		vh = self.build_value_head(x)
		ph = self.policy_head(x)

		model = KerasModel(inputs=[main_input], outputs=[vh, ph])
		model.compile(
			loss = {'value_head': 'mean_squared_error', 'policy_head': softmax_cross_entropy_with_logits},
			optimizer = SGD(lr=self.learning_rate, momentum = self.momentum),
			loss_weights = {'value_head': 0.5, 'policy_head': 0.5}
		)

		return model

	def build_residual_layer(self, input_block, filters, kernel_size):

		x = self.build_convolutional_layer(input_block, filters, kernel_size)

		x = Conv2D(
			filters = filters,
			kernel_size = kernel_size,
			data_format="channels_first",
			padding = 'same',
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.reg_const)
		)(x)

		x = BatchNormalization(axis=1)(x)

		x = add([input_block, x])

		x = LeakyReLU()(x)

		return (x)

	def build_convolutional_layer(self, x, filters, kernel_size):

		x = Conv2D(
			filters = filters,
			kernel_size = kernel_size,
			data_format = "channels_first",
			padding = 'same',
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.reg_const)
		)(x)

		x = BatchNormalization(axis=1)(x)
		x = LeakyReLU()(x)

		return (x)

	def build_value_head(self, x):

		x = Conv2D(
			filters = 1,
			kernel_size = (1,1),
			data_format = "channels_first",
			padding = 'same',
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.reg_const)
		)(x)


		x = BatchNormalization(axis=1)(x)
		x = LeakyReLU()(x)
		x = Flatten()(x)
		x = Dense(
			20,
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.reg_const)
		)(x)
		x = LeakyReLU()(x)

		x = Dense(
			1,
			use_bias = False,
			activation = 'tanh',
			kernel_regularizer = regularizers.l2(self.reg_const),
			name = 'value_head'
		)(x)

		return (x)

	def policy_head(self, x):

		x = Conv2D(
			filters = 2,
			kernel_size = (1,1),
			data_format = "channels_first",
			padding = 'same',
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.reg_const)
		)(x)

		x = BatchNormalization(axis=1)(x)
		x = LeakyReLU()(x)
		x = Flatten()(x)

		x = Dense(
			self.output_dim,
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.reg_const),
			name = 'policy_head'
		)(x)

		return (x)

