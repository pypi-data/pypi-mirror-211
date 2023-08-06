import sys
from pymg import display_error_message
sys.excepthook = display_error_message
import sys

def div(a, b):
	return a / b

print(div(int(sys.argv[1]), int(sys.argv[2])))
