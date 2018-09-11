import tensorflow as tf
from keras import regularizers
from keras.optimizers import SGD
from keras.models import Model as KerasModel
from keras.models import Sequential, load_model
from keras.layers import Input, Dense, Conv2D, Flatten, BatchNormalization, Activation, LeakyReLU, add

class Model():

	def __init__(self, regularization_constant, learning_rate, input_dimensions, output_dimensions):
		self.momentum = 0.9
		self.regularization_constant = regularization_constant
		self.learning_rate = learning_rate
		self.input_dimensions = input_dimensions
		self.output_dimensions = output_dimensions
		self.hidden_layers = [
			{'filters': 75, 'kernel_size': (4, 4)},
			{'filters': 75, 'kernel_size': (4, 4)},
			{'filters': 75, 'kernel_size': (4, 4)},
			{'filters': 75, 'kernel_size': (4, 4)},
			{'filters': 75, 'kernel_size': (4, 4)},
			{'filters': 75, 'kernel_size': (4, 4)}
		]
		self.keras_model = self.build()

	def predict(self, x):
		return self.keras_model.predict(x)

	def train(self, inputs):
		return 'training is happening'

	def build(self):
		main_input = Input(shape = self.input_dimensions)

		x = self.build_convolutional_layer(main_input, self.hidden_layers[0]['filters'], self.hidden_layers[0]['kernel_size'])

		if len(self.hidden_layers) > 1:
			for h in self.hidden_layers[1:]:
				x = self.build_residual_layer(x, h['filters'], h['kernel_size'])

		value_head = self.build_value_head(x)
		policy_head = self.build_policy_head(x)

		model = KerasModel(inputs = [main_input], outputs = [value_head, policy_head])
		model.compile(
			loss = {'value_head': 'mean_squared_error', 'policy_head': self.keras_policy_head_loss},
			optimizer = SGD(lr = self.learning_rate, momentum = self.momentum),
			loss_weights = {'value_head': 0.5, 'policy_head': 0.5}
		)

		return model

	def build_residual_layer(self, input, filters, kernel_size):
		x = self.build_convolutional_layer(input, filters, kernel_size)

		x = Conv2D(
			filters = filters,
			kernel_size = kernel_size,
			data_format = "channels_first",
			padding = 'same',
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.regularization_constant)
		)(x)

		x = BatchNormalization(axis = 1)(x)

		x = add([input, x])

		x = LeakyReLU()(x)

		return x

	def build_convolutional_layer(self, x, filters, kernel_size):
		x = Conv2D(
			filters = filters,
			kernel_size = kernel_size,
			data_format = "channels_first",
			padding = 'same',
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.regularization_constant)
		)(x)

		x = BatchNormalization(axis=1)(x)
		x = LeakyReLU()(x)

		return x

	def build_value_head(self, x):
		x = Conv2D(
			filters = 1,
			kernel_size = (1, 1),
			data_format = "channels_first",
			padding = 'same',
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.regularization_constant)
		)(x)

		x = BatchNormalization(axis=1)(x)
		x = LeakyReLU()(x)
		x = Flatten()(x)
		x = Dense(
			20,
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.regularization_constant)
		)(x)
		x = LeakyReLU()(x)

		x = Dense(
			1,
			use_bias = False,
			activation = 'tanh',
			kernel_regularizer = regularizers.l2(self.regularization_constant),
			name = 'value_head'
		)(x)

		return x

	def build_policy_head(self, x):
		x = Conv2D(
			filters = 2,
			kernel_size = (1,1),
			data_format = "channels_first",
			padding = 'same',
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.regularization_constant)
		)(x)

		x = BatchNormalization(axis=1)(x)
		x = LeakyReLU()(x)
		x = Flatten()(x)

		x = Dense(
			self.output_dimensions,
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.regularization_constant),
			name = 'policy_head'
		)(x)

		return x

	def keras_policy_head_loss(y_true, y_pred):
		predictions = y_pred
		labels = y_true

		zeros = tf.zeros(shape = tf.shape(labels), dtype = tf.float32)
		where = tf.equal(labels, zeros)

		negatives = tf.fill(tf.shape(labels), -100.0)
		logits = tf.where(where, negatives, predictions)

		return tf.nn.softmax_cross_entropy_with_logits_v2(labels = labels, logits = logits)