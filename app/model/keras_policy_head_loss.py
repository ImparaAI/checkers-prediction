import tensorflow

def keras_policy_head_loss(y_true, y_pred):
	p = y_pred
	pi = y_true

	zeros = tensorflow.zeros(shape = tensorflow.shape(pi), dtype = tensorflow.float32)
	where = tensorflow.equal(pi, zeros)

	negatives = tensorflow.fill(tensorflow.shape(pi), -100.0)
	logits = tensorflow.where(where, negatives, p)

	return tensorflow.nn.softmax_cross_entropy_with_logits_v2(labels = pi, logits = logits)