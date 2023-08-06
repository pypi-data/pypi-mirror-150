from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
import numpy as np
import time

def data_preprocess(df):
    """
Args:
    df: Dataframe in the format of cognino id with a single specialty.

Returns:
    df with cognino id and all specialties in one string.

Raises:
    KeyError: No exception raised.
    """
    df['spec'] = df.groupby(['cogent_id'])['ic_spec_name'].transform(lambda x : ','.join(x)) # Get specs into a single string.
    df.drop('ic_spec_name', axis=1, inplace=True)
    df.drop_duplicates(inplace=True)
    return df


def create_index(df, model):
    """
Args:
    df: df with cognino id and all specialties in one string.
    model: Transformer model to create embeddings.

Returns:
    faiss index

Raises:
    KeyError: No exception raised.
    """
    encoded_data = model.predict(df.spec.tolist())
    encoded_data = np.asarray(encoded_data.astype('float32'))
    index = faiss.IndexIDMap(faiss.IndexFlatIP(768))
    index.add_with_ids(encoded_data, np.array(range(0, len(df))))
    faiss.write_index(index, 'spec.index')
    return index

def fetch_spec_info(dataframe_idx, df):
    """
Args:
    dataframe_idx: row index of dataframe at the point at which we want to retrive the company specialties etc.
    df: df with cognino id and all specialties in one string.

Returns:
    cognino id of company at that index.

Raises:
    KeyError: No exception raised.
    """

    info = df.iloc[dataframe_idx]
    id = info['cogent_id']
    # meta_dict = dict()
    # meta_dict['cogent_id'] = info['cogent_id']
    # meta_dict['spec'] = info['spec'][:500]
    return int(id) #meta_dict
    
def search(query, max_k, index, model, threshold, df):
    """
Args:
    query: search string used to find top k results.
    max_k: max number of results we want to retrieve.
    index: Faiss index
    threshold: confidence threshold we use to calculate whether a result is semantically similar to query.

Returns:
    results of search process

Raises:
    KeyError: No exception raised.
    """
    t=time.time()
    query_vector = model.predict([query])
    top_k = index.search(query_vector, max_k) # index.search() also returns the squared distances of the query and the k results.
    top_k_ids = top_k[1].tolist()[0]
    top_k_conf = top_k[0].tolist()[0]
    top_k_num_list = [conf for conf in top_k_conf if conf > threshold]
    top_k_num = len(top_k_num_list)
    top_k_list = top_k_ids[0:top_k_num]
    top_k_ids = list(top_k_ids)
    results =  [fetch_spec_info(idx, df) for idx in top_k_ids[0:top_k_num]]
    print('>>>> Results in Total Time: {}'.format(time.time()-t))
    return results