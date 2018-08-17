from flask import Flask
import tensorflow

app = Flask(__name__)

@app.route("/")
def hello():
	hello = tensorflow.constant('Hello, TensorFlow!')
	sess = tensorflow.Session()
	return sess.run(hello)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)