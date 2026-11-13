## Start local LLM
## PDF Readers
## Chunking :4 types of Chunking fixed,paragraph,semantic,Overlapping
## Embeddings
## Vector DB(Chroma DB)
## LLM for processing the extracted content 
## conversation loop/engine

from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
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

## 2. PDF Reader
loader=PyPDFLoader("rag_intro.pdf")
pages=loader.load()
print(f"Total pages:{len(pages)}")

## 3. Chunking 
text_splitter =RecursiveCharacterTextSplitter(chunk_size=100 ,chunk_overlap=50)
chunks=text_splitter.split_documents(pages)
print(f"Total chunks:{len(chunks)}")

## 4. Embeddings
embeddings=OllamaEmbeddings(model="nomic-embed-text")

## 5. Vector DB
vectorstore=Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory="./rag_demo")
retriever =vectorstore.as_retriever(search_kwargs={"k":3})
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

## conversation loop/engine
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

    
