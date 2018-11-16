import tensorflow as tf
from pathlib import Path
from keras import backend
from keras import regularizers
from keras.optimizers import SGD
from keras.models import load_model, Model as KerasModel
from keras.layers import add, BatchNormalization, Conv2D, Dense, Flatten, Input, LeakyReLU

def build(weights_file_path, input_dimensions, output_dimensions, hyperparameters):
	return Builder(weights_file_path, input_dimensions, output_dimensions, hyperparameters).build()

class Builder:

	def __init__(self, weights_file_path, input_dimensions, output_dimensions, hyperparameters):
		self.weights_file_path = weights_file_path
		self.input_dimensions = input_dimensions
		self.output_dimensions = output_dimensions
		self.hyperparameters = hyperparameters

	def build(self):
		backend.clear_session()

		if self.weights_file_path and Path(self.weights_file_path).is_file():
			return load_model(self.weights_file_path, custom_objects = {'keras_policy_head_loss': keras_policy_head_loss})

		input_layer = Input(shape = self.input_dimensions)

		stack = self.build_shared_stack(input_layer)
		value_head = self.build_value_head(stack)
		policy_head = self.build_policy_head(stack)

		keras_model = KerasModel(inputs = [input_layer], outputs = [value_head, policy_head])

		keras_model.compile(
			loss = {'value_head': 'mean_squared_error', 'policy_head': keras_policy_head_loss},
			optimizer = SGD(lr = self.hyperparameters.learning_rate, momentum = self.hyperparameters.momentum),
			loss_weights = {'value_head': 0.5, 'policy_head': 0.5}
		)

		return keras_model

	def build_shared_stack(self, input_layer):
		stack = self.build_convolutional_segment(input_layer)

		for h in range(self.hyperparameters.hidden_layer_count):
			stack = self.build_residual_segment(stack)

		return stack

	def build_residual_segment(self, x):
		original = x
		x = self.build_hidden_convolutional_layer(x)

		x = BatchNormalization(axis = 1)(x)
		x = LeakyReLU()(x)

		x = self.build_hidden_convolutional_layer(x)

		x = BatchNormalization(axis = 1)(x)

		x = add([original, x])

		x = LeakyReLU()(x)

		return x

	def build_convolutional_segment(self, x):
		x = self.build_hidden_convolutional_layer(x)

		x = BatchNormalization(axis = 1)(x)
		x = LeakyReLU()(x)

		return x

	def build_hidden_convolutional_layer(self, x):
		return Conv2D(
			filters = self.hyperparameters.convolution_kernel_count,
			kernel_size = self.hyperparameters.convolution_kernel_size,
			data_format = "channels_first",
			padding = 'same',
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.hyperparameters.regularization_constant)
		)(x)

	def build_value_head(self, x):
		x = Conv2D(
			filters = 1,
			kernel_size = (1, 1),
			data_format = "channels_first",
			padding = 'same',
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.hyperparameters.regularization_constant)
		)(x)

		x = BatchNormalization(axis = 1)(x)
		x = LeakyReLU()(x)
		x = Flatten()(x)
		x = Dense(
			20,
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.hyperparameters.regularization_constant)
		)(x)
		x = LeakyReLU()(x)

		x = Dense(
			1,
			use_bias = False,
			activation = 'tanh',
			kernel_regularizer = regularizers.l2(self.hyperparameters.regularization_constant),
			name = 'value_head'
		)(x)

		return x

	def build_policy_head(self, x):
		x = Conv2D(
			filters = 2,
			kernel_size = (1, 1),
			data_format = "channels_first",
			padding = 'same',
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.hyperparameters.regularization_constant)
		)(x)

		x = BatchNormalization(axis = 1)(x)
		x = LeakyReLU()(x)
		x = Flatten()(x)

		x = Dense(
			self.output_dimensions,
			use_bias = False,
			activation = 'linear',
			kernel_regularizer = regularizers.l2(self.hyperparameters.regularization_constant),
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