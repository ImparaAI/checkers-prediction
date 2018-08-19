from model import builder

def predict(request):
	return builder.build().predict(request)