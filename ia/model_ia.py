from pathlib import Path

from decouple import config

from langchain_chroma import Chroma
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


try:
    openai_api_key = config("OPENAI_API_KEY")
except Exception as e:
    print(f"Erro ao ler OPENAI_API_KEY usando decouple: {e}")
    raise ValueError("Chave da API OpenAI não encontrada via decouple")

def path_vector_store() -> str:
    db = Path('../db')
    persist_directory = str(db)
    return persist_directory

def load_existing_vector_store():
    persist_directory = path_vector_store()
    embedding = OpenAIEmbeddings(
        api_key=openai_api_key
    )
    if Path(persist_directory).exists():
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding,
        )
        return vector_store
    return None

def add_to_vector_store(chunks, vector_store=None):
    persist_directory = path_vector_store()
    embedding = OpenAIEmbeddings(api_key=openai_api_key)
    if vector_store:
        print("Adicionando novos chunks ao banco de dados")
        vector_store.add_documents(chunks)
    else:
        print("Criando banco de dados de vetores")
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            persist_directory=persist_directory,
            collection_name="diabetes_chunks",
        )
    return vector_store

def process_pdf_to_chunks(pdf_path):
    """Quebra o PDF em partes(chunks)"""
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    all_chunks = text_splitter.split_documents(
        documents=docs
    )
    # chunks = text_splitter.split_text(full_text)
    vector_store = load_existing_vector_store()
    add_to_vector_store(
        chunks=all_chunks,
        vector_store=vector_store
    )

def chatbot_ia(retriever, query):
    model_openai = config('MODEL_OPENAI')
    model = ChatOpenAI(
        api_key=openai_api_key,
        model=model_openai
    )
    system_prompt = '''
    Use o contexto para responder as perguntas.
    Contexto: {context}
    '''
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", f"{input}"),
        ],
    )
    question_answer_chain = create_stuff_documents_chain(
        llm=model,
        prompt=prompt,
    )
    chain = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=question_answer_chain
    )
    response = chain.invoke(
        {'input': query}
    )
    return response
