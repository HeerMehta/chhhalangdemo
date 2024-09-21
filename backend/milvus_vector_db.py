import re
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from sentence_transformers import SentenceTransformer
from pymilvus import MilvusClient


# Function to read and print the content of a file
def read_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()  # Read the entire file content
            return content
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return None
    except IOError:
        print(f"Error reading file {file_name}.")
        return None


# Extract the paragraphs from the file content
def extract_paragraphs(file_content):
    matches = re.findall(r'Paragraphs:\n(.*?)\n\nLinks:', file_content, re.DOTALL)
    if matches:
        documents = matches[0].split('\n\n')  # Split paragraphs based on double newlines
        documents = [doc.strip() for doc in documents if doc.strip()]  # Clean up empty lines
        return documents
    else:
        print("No paragraphs found in the file.")
        return []


# Insert documents into Milvus
def insert_into_milvus(documents):
    # Prepare metadata and IDs
    metadatas = [{"item_id": i} for i in range(len(documents))]
    ids = list(range(1, len(documents) + 1))

    # Connect to Milvus server
    client = MilvusClient(uri="http://localhost:19530")
    connections.connect("default", host="localhost", port="19530")

    # Check if collection exists and drop it if necessary
    collection_name = "converstaional_chatbot_ai"
    if utility.has_collection(collection_name):
        client.drop_collection(collection_name)

    # Define the schema
    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=65534),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=384)
    ]
    schema = CollectionSchema(fields, description="simple for questions embedding")

    # Create the collection
    converstational_chatbot_ai = Collection(collection_name, schema)

    # Create an index for the embeddings field
    index = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128},
    }
    converstational_chatbot_ai.create_index("embeddings", index)

    # Generate embeddings using SentenceTransformer
    sentence_transformer = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = sentence_transformer.encode(documents)

    # Prepare the data for insertion
    entities = [
        ids,  # Primary key field
        documents,  # Source field
        embeddings.tolist()  # Embeddings field
    ]

    # Insert the data into the collection
    converstational_chatbot_ai.insert(entities)
    converstational_chatbot_ai.flush()
    converstational_chatbot_ai.load()

    print('Data inserted into Milvus successfully.')


if _name_ == "_main_":
    # Read the file content
    file_content = read_file("scraped_data.txt")

    # Process the content and create documents
    if file_content:
        documents = extract_paragraphs(file_content)

        # Proceed only if documents are found
        if documents:
            # Insert the documents into Milvus
            insert_into_milvus(documents)
        else:
            print("No documents to insert.")