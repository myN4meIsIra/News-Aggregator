# news entries db operator
'''
    read/write operations for news entry db file
'''



import json
from cust_logging.logger import Log
from objects.History_of_News_Entry import History_of_News_Entry

Log = Log('json_file_operators.py')
from objects.Stories_Topic import Stories_Topic
import global_vars
import os





# read all
'''
    read contents of news entries db file
    return 
'''
def read_all_json(file_path):
    file_data = {}
    try:
        with open(file_path, 'r') as file:
            # load data directly
            file_data = json.load(file)
            #Log.log(f"previous contents of news entries db file {file_data}")

    except Exception as E:
        Log.error(f"{E}")


    return file_data




# write append
'''
    write to contents of news entries db file
    input: data - Stories Topic obj
    return     
'''
def write_append_json(data, file_path):
    Log.log('appending data...')
    # read contents of file
    previous_contents = read_all_json(file_path)

    # add json
    # confirm data is a News_Entry object
    if type(data) is Stories_Topic:
        Log.log(f"data type matches")
    else:
        Log.error(f"data {data}, type {type(data)} does not match {type(Stories_Topic)}")
        return

    new_contents = previous_contents
    Log.log(f"previous contents {previous_contents}")
    Log.log(f"additional contents {data.get}")


    # check if the title already exists
    new = 0
    for index, i in enumerate(previous_contents):
        if str(i["topic"]) == str(data.get()['topic']):
            Log.log(f"title {data.get()['topic']} already in db. Checking url")

            # check if url already is in list
            # todo does not work, so fix it
            for j in i['stories']:
                if str(j) == str(data.get()['stories']):
                    Log.log(f"url {data.get()['url']} already in db. quitting right action")
                    return

            # url must not be in stories list yet, so add it
            Log.log(f"stories to append: [{[story for story in data.get()['stories']]}]")
            for story in data.get()['stories']:
                new_contents[index]['stories'].append(story)
            new=1

    # if it's a new entry, add it
    if new==0:
        # update old contents
        new_contents.append(data.get())

    # convert to json
    Log.log(f"contents to create into json {new_contents}")
    new_contents_json = json.dumps(new_contents)

    # write contents of file
    try:
        with open(file_path, 'w') as file:
            file.write(new_contents_json)
    except Exception as E:
        Log.error(f"{E}")

    return 1




# single match multiple return
'''
    check thew json file for multiple returns of the same 
    for file format: <word> 
'''
def single_match_multiple_return(file_path, keyword):
    matches = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
                record = json.loads(f)

                # check for keyword match
                print(record)

    except Exception as E:
        Log.error(f"{E}")

    return matches






# remove entry
'''
    remove entry
'''
#todo: create temp file of db; read contents of db; populate temp file with changes; replace db file with temp file; erase temp file