#
"""


"""
from sklearn.feature_extraction.text import TfidfVectorizer

from cust_logging.logger import Log
Log = Log(f'cosine_similarity.py')
import pandas as pd

# data to vector
'''
    convert data into a vector for cosine similarity analysis
'''
def data_to_vector(input_list):

    # perform parameter validation
    if not isinstance(input_list, list):
        Log.error(f"input list ({input_list}) is of type {type(input_list)}, not List")

    working_list = [entry.get()['body'] for entry in input_list]



    # get downweighted vector (to account for frequently-used words) of words for the inputs
    count_vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),  # for 1,2,and 3-word phrases
        stop_words='english',   # exclude these words
    )
    #count_vectorizer = TfidfVectorizer()


    for i, str in enumerate(working_list):
        if type(str) != type('string'):
            Log.error(f"entry {i} is of type {type(str)}, but needs to be a string. It is populated with data: {str}")


    sparse_matrix = count_vectorizer.fit_transform(working_list)


    # OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix,
                      columns=count_vectorizer.get_feature_names_out(),
                      index=[f"{term.get()['title']}" for i,term in enumerate(input_list)])
    Log.log(f"df = {df}")


    return sparse_matrix



# cosine similarity
'''
    find similarity between two different vector entries
'''
def cosine_similarity(data_frame):


    #Compute Cosine Similarity
    from sklearn.metrics.pairwise import cosine_similarity
    similarity_matrix = cosine_similarity(data_frame, data_frame)

    Log.log(f"cosine similarity {similarity_matrix}")

    return similarity_matrix
