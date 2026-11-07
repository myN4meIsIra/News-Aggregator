# news title
'''
    object to hold news stories/entries which all are basically the same topic
'''

from cust_logging.logger import Log
Log = Log('Stories_Topic.py')


class Stories_Topic():
    def __init__(self, topic):
        self.topic = topic
        self.stories = []



    # add story
    '''
        if another news story is found to share the same topic, add it to the story list
    '''
    def add_story(self, url):
        if url not in self.stories:
            self.stories.append(url)
            Log.log(f"adding to topic {self.topic} <- {url}")

        else:
            Log.log(f"news article already exists in topic {self.topic} <- {url}")

        return 1


    # getter
    def get(self):
        return {
            "topic":self.topic,
            'stories':self.stories
        }

