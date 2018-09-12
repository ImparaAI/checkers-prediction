import sys, os
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from keras import regularizers
sys.stderr = stderr