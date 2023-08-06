"""
These are functions 
"""
import json
import uuid
from opensearchpy import helpers, OpenSearch

from Config.settings import 

def initialise_os_client():
    """
    This function takes the SERVICE_URI for our opensearch setup and the instantiate the client
    """
    os_client = OpenSearch(hosts=SERVICE_URI, ssl_enable=True)
    
    return os_client

def upload_os_document(os_client, index_name, document):
    """
    This funciton takes a dictionary and all other relevant information and then pushes to the opensearch collection
    """
    doc_id = str(uuid.uuid4())
    response = os_client.index(
        index = index_name,
        body = document,
        id = doc_id,
        refresh = True
    )
    
    return response

def delete_os_document(os_client, index_name, doc_id):
    """
    This funciton takes a dictionary and all other relevant information and then pushes to the opensearch collection
    """
    # Delete the document.
    response = os_client.delete(
        index = index_name,
        id = doc_id
    )
    
    # Delete the index.
    response = client.indices.delete(
        index = index_name
    )

    return response


def search_for_os_document(os_client, INDEX_NAME, search_term, num_results, search_field_list):
    """
    This function builds out the query based on the input fields provided and searches the database
    """
    query = {
      'size': num_results,
      'query': {
        'multi_match': {
          'query': search_term,
          'fields': search_field_list
        }
      }
    }
    
    response = os_client.search(
    body = query,
    index = INDEX_NAME
    )
    
    return response