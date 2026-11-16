## Start local LLM
## PDF,TEXT,word,.md Readers
## Chunking :4 types of Chunking fixed,paragraph,semantic,Overlapping
## Embeddings
## Vector DB(Chroma DB)
## LLM for processing the extracted content 
## conversation loop/engine

import os
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader,TextLoader,UnstructuredWordDocumentLoader,UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

## 1. Start local LLM
llm = ChatOllama(
    model="llama3.2:1b",
    base_url="http://localhost:11434/"
)
print("Local LLM Started")

##Load all the files from the folder
DATA_PATH="./Knowledge"
documents=[]
for file in os.listdir(DATA_PATH):
    print(f"Processing file:{file}")

   #for Processing the pdf 
    if file.endswith(".pdf"):
        loader=PyPDFLoader(os.path.join(DATA_PATH,file))
        documents.extend(loader.load())
   #For processing the .txt
    if file.endswith(".txt"):
        loader=TextLoader(os.path.join(DATA_PATH,file))
        documents.extend(loader.load())
   #For processing the .docx
    if file.endswith(".docx"):
        loader=UnstructuredWordDocumentLoader(os.path.join(DATA_PATH,file))
        documents.extend(loader.load())
   #For processing the .md
    if file.endswith(".md"):
        loader=UnstructuredFileLoader(os.path.join(DATA_PATH,file))
        documents.extend(loader.load())     

    else:
        print(f"unsupported file format :{file}")
print(f"loaded {len(documents)} documents fromthe folder")        
            
## 3. Chunking 
text_splitter =RecursiveCharacterTextSplitter(chunk_size=100 ,chunk_overlap=50)
chunks=text_splitter.split_documents(documents)
print(f"Total chunks:{len(chunks)} from {len(documents)}  documents")

noOfDocs=len(documents)

## 4. Embeddings
embeddings=OllamaEmbeddings(model="nomic-embed-text")

## 5. Vector DB
vectorstore=Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory="./Multirag_demo")
retriever =vectorstore.as_retriever(search_kwargs={"k":2})
print("Vector DB Created")

## 6. LLM for processing the extracted content 
prompt =ChatPromptTemplate.from_messages([
    ("system","You area helpful assistant that provides information from the uploaded file"),
    ("system","history:{history}"),
    ("system","context:{context}"),
    ("human","{input}")
])

chat_history =[]
print("\n Pdf conversation RAG,(Type 'exit' to end he conversation \n")

while True:
    user_input=input("User: ")
    if user_input.lower()=="exit":
        print("Conversation ended ,see you soon")
        break

    retrieved_docs=retriever.invoke(user_input)
    context="\n".join([doc.page_content for doc in retrieved_docs])

    print(f"Retrieved context:\n{context}")

    chat_history.append(HumanMessage(content=user_input))
    response=llm.invoke(prompt.format(history=chat_history,context=context,input=user_input))
    
    chat_history.append(AIMessage(content= response.content))
    print(f"Assitant: {response.content}\n")
    
