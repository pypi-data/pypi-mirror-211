__version__ == "0.1.0"

import chromadb

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="user_instructprompt_collection")

def add(instruction: str): 
    collection.add(
        documents=[instruction],
        ids=[str(id)]
    )
    print("✅ instruction added")
    return

def list_instructions(): 
    return collection.get()["documents"]

def query_instructions(query: str): 
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    instructions = ""
    for document in results["documents"][0]: 
        instructions += document + "\n"
    return instructions

