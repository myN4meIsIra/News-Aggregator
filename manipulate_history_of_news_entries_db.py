# created by Ira Garrett
'''


'''



import global_vars
from cust_logging.logger import Log
Log = Log('manipulate_history_of_news_entries_db.py')
from objects.Stories_Topic import Stories_Topic
import global_vars
import os
import json
from objects.History_of_News_Entry import History_of_News_Entry
import file_manipulators.json_file_operators


# update history of news entries
'''
    
'''
def update_history_of_news_entries_db(entry):

    # the contents of this db are
    '''
    story_text.append({
        'title':entry['title'],
        'url':entry['url'],
        'body':body,
        'date':entry['published']
    })
    '''


    return 1



# entry in database
'''
    bool return for if {data} is in db
'''
def entry_title_in_db(title):

    # iterate over lines in the file, testing against data.title
    chunk_size = 1024 * 1024  # 1 MB chunks
    try:
        with open(global_vars.history_of_news_entries, 'r') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                header = "{\"title\": \""
                for i,chr in enumerate(chunk):
                    # check if first char in header matches the chr in this chunk
                    if chr == header[0]:
                        Log.log(f"first char of header string detected")
                        offset = i+len(header)
                        if chunk[i:offset] == header:
                            if chunk[i+offset:i+offset+len(title)]:
                                Log.log(f"header {title} found")
                                return 1

    except Exception as E:
        Log.error(f"error {E}")

    return 0



# write append
'''
    write to contents of news entries db file
    input: data - Stories Topic obj
    return     
'''
def write_append_history_of_news_entries_json(data):
    '''
    format of data:
    ({
        'title':entry['title'],
        'url':entry['url'],
        'body':body,
        'date':entry['published']
    })
    '''

    Log.log('appending data...')

    # read contents of file
    previous_contents = file_manipulators.json_file_operators.read_all_json(global_vars.history_of_news_entries)

    # add json
    # confirm data is a News_Entry object
    if type(data) is History_of_News_Entry:
        Log.log(f"data type matches")
    else:
        Log.error(f"data {data}, type {type(data)} does not match {type(History_of_News_Entry)}")
        return

    new_contents = previous_contents
    #Log.log(f"previous contents {previous_contents}")
    #Log.log(f"additional contents {data.get}")


    # check if the title already exists
    for index, i in enumerate(previous_contents):
        if str(i["title"]) == str(data.get()['title']):
            Log.log(f"title {data.get()['title']} already in db. Skipping")
            return

    Log.log(f"appending {data.get()['title']}")
    new_contents.append(data.get())

    # convert to json
    #Log.log(f"contents to create into json {new_contents}")
    new_contents_json = json.dumps(new_contents)

    # write contents of file
    try:
        with open(global_vars.history_of_news_entries, 'w') as file:
            file.write(new_contents_json)
    except Exception as E:
        Log.error(f"{E}")

    return 1

