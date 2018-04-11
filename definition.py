import os

class ROOT():
	ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
	DATA_ROOT = ROOT_DIR+'/data' # This is your Data Root
	
