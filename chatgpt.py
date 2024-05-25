'''
import os
import sys
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import Chroma
import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = True
query = None
if len(sys.argv) > 1:
    query = sys.argv[1]

if PERSIST and os.path.exists("persist"):
    print("Reusing index...\n")
    vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    loader = DirectoryLoader("data/")
    embeddings = OpenAIEmbeddings()
    if PERSIST:
        index = VectorstoreIndexCreator(embedding=embeddings, vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
    else:
        index = VectorstoreIndexCreator(embedding=embeddings).from_loaders([loader])

chat_history = []
while True:
    if not query:
        query = input("Prompt: ")
    if query in ['quit', 'q', 'exit']:
        sys.exit()

    # Call the index.query with the custom LLM and temperature
    result = index.query(query, llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7))
    print(result)
    chat_history.append((query, result))
    query = None
'''
import constants
import os
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
import warnings
warnings.filterwarnings('ignore')


def get_chatgpt_response(query):
    os.environ["OPENAI_API_KEY"] = constants.APIKEY

    loader = TextLoader('data/comments.txt')
    # loader = DirectoryLoader(".", glob="*.txt")

    # Create an instance of the OpenAIEmbeddings class
    embeddings = OpenAIEmbeddings()

    # Pass the embeddings instance to the VectorstoreIndexCreator
    index = VectorstoreIndexCreator(embedding=embeddings).from_loaders([loader])

    return index.query(query, llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.4))


def get_chatgpt_script(query):
    os.environ["OPENAI_API_KEY"] = constants.APIKEY

    loader = TextLoader('data/comments.txt')
    # loader = DirectoryLoader(".", glob="*.txt")

    # Create an instance of the OpenAIEmbeddings class
    embeddings = OpenAIEmbeddings()

    # Pass the embeddings instance to the VectorstoreIndexCreator
    index = VectorstoreIndexCreator(embedding=embeddings).from_loaders([loader])

    return index.query(query, llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.4))