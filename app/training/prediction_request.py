class PredictionRequest:
	def __init__(self):
		self._input = None
		self._response = None
		self._needs_response = False

	def set_input(self, input):
		self._input = input
		self._response = None
		self._needs_response = True

	def get_input(self):
		return self._input

	def set_response(self, response):
		self._response = response
		self._needs_response = False

	def get_response(self):
		return self._response

	def needs_response(self):
		return self._needs_response