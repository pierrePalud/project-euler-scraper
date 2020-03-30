import os

# raw url to get project euler problems data
URL_ROOT = 'https://projecteuler.net/problem={}'

# url to the archive PE page
URL_ARCHIVE = 'https://projecteuler.net/archives'

# name of the directory with history txt file 
DATA_DIR = 'data'

# name of the output directory
RESULT_DIR = 'result'


PATH_TO_GRAPH_FILE = os.path.join(RESULT_DIR, 'project-euler-progression.png')