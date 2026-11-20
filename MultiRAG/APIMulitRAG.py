import os
import getpass
from langchain_google_genai import ChatGoogleGenerativeAI ,GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader,TextLoader,UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

gapi_key = os.getenv("GEMINI_API_KEY")
if not gapi_key:
    gapi_key = getpass.getpass("Enter your Gemini API key: ").strip()
if not gapi_key:
    raise RuntimeError("A Gemini API key is required")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=gapi_key
    )

print("Gemini LLM started")

##Load all the files from the folder
DATA_PATH="./Knowledge"

documents=[]
for file in os.listdir(DATA_PATH):
    print(f"Processing file:{file}")

   # For processing the PDF
    if file.lower().endswith(".pdf"):
        loader=PyPDFLoader(os.path.join(DATA_PATH,file))
        documents.extend(loader.load())
   # For processing the TXT
    elif file.lower().endswith(".txt"):
        loader=TextLoader(os.path.join(DATA_PATH,file), encoding="utf-8")
        documents.extend(loader.load())
   # For processing the DOCX
    elif file.lower().endswith(".docx"):
        loader=UnstructuredWordDocumentLoader(os.path.join(DATA_PATH,file))
        documents.extend(loader.load())
   # For processing the Markdown
    elif file.lower().endswith(".md"):
        loader=TextLoader(os.path.join(DATA_PATH,file), encoding="utf-8")
        documents.extend(loader.load())
    else:
        print(f"unsupported file format :{file}")

print("\n--- Document Validation ---")

for i, doc in enumerate(documents):
    content = doc.page_content

    print(f"Document {i + 1}")
    print(f"Characters: {len(content)}")
    print(f"Preview: {content[:100]!r}")
    print("-" * 50)      
print(f"loaded {len(documents)} documents fromthe folder")

## 3. Chunking 
text_splitter =RecursiveCharacterTextSplitter(chunk_size=100 ,chunk_overlap=50)
chunks=text_splitter.split_documents(documents)
print(f"Total chunks:{len(chunks)} from {len(documents)}  documents")

noOfDocs=len(documents)

## 4. Embeddings
embeddings=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001",google_api_key=gapi_key)

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

    if isinstance(response.content, str):
        response_text = response.content
    elif isinstance(response.content, list):
        response_text = "\n".join(
            block["text"]
            for block in response.content
            if isinstance(block, dict) and isinstance(block.get("text"), str)
        )
    else:
        raise TypeError(f"Unexpected Gemini response content: {type(response.content).__name__}")

    chat_history.append(AIMessage(content=response_text))
    print(f"Assistant: {response_text}\n")
    
