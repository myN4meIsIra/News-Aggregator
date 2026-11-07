#
'''

'''


import os
from cust_logging.logger import Log
Log = Log('generic_file_operators.py')


# read json file
'''
    read contents of json file
'''
def read_file(file_path):
    lines = []

    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                Log.log(f"lines = {lines}")

        except Exception as E:
            Log.error(f"{E}")
    else:
        Log.error(f"{file_path} NOT A FILE")


    return lines
