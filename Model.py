## importing neccessary library

import openai
from llama_index.core import SimpleDirectoryReader ,VectorStoreIndex
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.indices.postprocessor import SimilarityPostprocessor
from llama_index.core.query_engine import RetrieverQueryEngine
import llama_index

'''
This is the initial setup method
This method is used to create a documents and then get document parsed to node ,which is then 
indexed using vectorstoreindex class and then we create a query engine out of index. 

'''
class Model:

    def init(self):
        global queryEngine
        # loading data through reader and create a documnet
        reader = SimpleDirectoryReader(input_dir="./dataPDF")
        documents = reader.load_data()

        # create parser and parse document into nodes
        parser = SimpleNodeParser.from_defaults()
        nodes = parser.get_nodes_from_documents(documents=documents)

        #  build index
        index = VectorStoreIndex(nodes)
        # Construct Query Engine
        queryEngine = index.as_query_engine()



    '''
    This method is used  to classify query engine response  sentiment as Positive or Negative
    '''


    def get_response(self,example):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with a paragraph, and your task is to classify its sentiment as Positive or Negative"
                },
                {
                    "role": "user",
                    "content": "I'm sorry, but I am unable to provide a relevant answer to the query gvchj based on the context information provided"
                },
                {
                    "role": "assistant",
                    "content": "Negative"
                },
                {
                    "role": "user",
                    "content": "I'm sorry, I couldn't find any relevant information or answer to the query provided."
                },
                {
                    "role": "assistant",
                    "content": "Negative"
                },
                {
                    "role": "user",
                    "content": "To create a permit application, you need to define permit types by setting up permit categories, defining permit statuses, setting up workflows and fee models, creating permit types, designing permit application forms, and more"
                },
                {
                    "role": "assistant",
                    "content": "Positive"
                },
                {
                    "role": "user",
                    "content": "To delete a contact, you should follow these steps:\n1. Select Common Setup > Contact Type.\n2. Click a row on the Contact Type page."
                },
                {
                    "role": "assistant",
                    "content": "Positive"
                },
                {
                    "role": "user",
                    "content": "Oracle Corporation and its affiliates are not responsible for and expressly disclaim all warranties of any kind with respect to third-party content, products, and services unless otherwise set forth in an applicable agreement between you and Oracle"
                },
                {
                    "role": "assistant",
                    "content": "Positive"
                },
                {
                    "role": "user",
                    "content": "I'm sorry, I couldn't find any relevant information or answer to the query provided. If you have any other questions or need assistance, feel free to ask."
                },
                {
                    "role": "assistant",
                    "content": "Negative"
                },
                {
                    "role": "user",
                    "content": f"""{example} """
                }
            ]
        )
        return response.choices[0].message.content


    ## Query response function
    '''
    This method takes user input and get result from query engine and analyze it and then it produce
    result in a given format that includes <response fetched>+<document from where this reponse is fetched>  
    '''
    def query_response(self,user_input):
        response = queryEngine.query(user_input)
        analyzed_response = self.get_response(response.response)
        final_response = 'I am not having sufficent resource available.Please connect with admin for any information on it.'
        if analyzed_response == 'Positive':
            file_name = response.source_nodes[0].node.metadata['file_name']
            final_response = response.response + '\n Check further at ' + file_name + ' document'

        return final_response


    def __init__(self):
        print(__name__)