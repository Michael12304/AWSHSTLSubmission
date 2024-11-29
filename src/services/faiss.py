from langchain.vectorstores import FAISS

import pandas as pd

import time


def load_csv_faq(csv_files: list[str]):
    faq_vectors = []

    for csv_file in csv_files:
        # Load CSV file from the given path
        df = pd.read_csv(csv_file)

        # Store first column in an array for all the questions
        question_list = df.iloc[:, 0].tolist()

        # Store second column in an array for all the answers
        answers_list = df.iloc[:, 1].tolist()

        len_faq = len(question_list)

        i = 0
        while i < len_faq:
            question = question_list[i]
            answer = answers_list[i]

            vector = f"""Question: {question}
Answer: {answer}"""
            faq_vectors.append(vector)
            i += 1

    return faq_vectors

def create_knowledge_base(documents_list):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    def populate_faq_db(faq_vectors, num):
        start = time.time()
        ##print (f'Now you have {len(faq_vectors)} faq documents')

        db = FAISS.from_texts(faq_vectors, embeddings)
        end = time.time()

        ##print("KB Base Population Time: ", end - start)

        index_name = "faq_" + str(num)
        db.save_local(index_name)

        return index_name

    def populate_docs_db(documet, num):
        index_name = "docs_" + str(num)
        # Chunk into pieces of 500 characters with x overlap
        return index_name

    # Create main db
    ##print("Creating Main Database (1)")
    doc_type = documents_list[0]["type"]
    doc_content = documents_list[0]["content"]

    if doc_type == "FAQ":
        main_index_name = populate_faq_db(doc_content, 0)
        main_db = FAISS.load_local(main_index_name, embeddings)

    i = 1
    # Go through dbs and merge them
    num_docs = len(documents_list)
    ##print("num docs: ", num_docs)

    while i < num_docs:
        ##print("Creating Database ", i+1)
        doc = documents_list[i]
        doc_type = doc["type"]
        doc_content = doc["content"]
        ##print(f"Document Type: {doc_type}")
        ##print(f"Document Content: {doc_content}\n")

        if doc_type == "FAQ":
            # ##print("Adding in Texts")
            # new_db = FAISS.from_texts(doc_content, embeddings)

            # # Merge Database into Main DB
            # main_db.merge_from(new_db)

            new_db_name = populate_faq_db(doc_content, i)
            new_db = FAISS.load_local(new_db_name, embeddings)
            main_db.merge_from(new_db)

        i += 1

    return main_db

def create_kb(urls):
    gdrive_urls = urls
    documents = []
    for gdrive_url in gdrive_urls:
        # Extract the file ID from the Google Drive URL
        if "/view" in gdrive_url:
            file_id = gdrive_url.split("/d/")[1].split("/view")[0]
        else:
            file_id = gdrive_url.split("/d/")[1].split("/edit")[0]
        # Construct the direct CSV download URL for Google Sheets
        download_url = (
            f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
        )
        faq_vectors = load_csv_faq([download_url])
        #####print("faq_vectors: ", faq_vectors)

        # Any Documnets - docx, pdf, txt
        # FAQ - list of string with faq info
        documents.append({"type": "FAQ", "content": faq_vectors})

    return create_knowledge_base(documents)
