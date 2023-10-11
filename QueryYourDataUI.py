import tkinter as tk
from tkinter import filedialog
from tkinter import Text, scrolledtext
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.chains import LLMChain
from langchain.chains import RetrievalQA
from langchain.chains import SequentialChain
from langchain.prompts import ChatPromptTemplate
from IPython.display import display, Markdown, Latex
import openai
import os
import sys

print(sys.version) 

sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
 # read local .env file
_ = load_dotenv(find_dotenv())
openai.api_key  = os.environ['OPENAI_API_KEY']

class LLM_Parser:
    def __init__(self, pdf_name, llm):
        self.pdf_loader = PyPDFLoader(pdf_name)
        agb_pages = self.pdf_loader.load()
        embeddings = OpenAIEmbeddings()
        db = DocArrayInMemorySearch.from_documents(agb_pages, embedding=embeddings)
        self.retrieval_chain = RetrievalQA.from_chain_type(chain_type="stuff", llm=llm4, retriever = db.as_retriever())
    
    def display(self):
        print(f"Name: {self.name}, Age: {self.age}, Grade: {self.grade}")

llm4 = ChatOpenAI(temperature=0.0, model_name="gpt-4")
llm_parser = LLM_Parser('./resources/AGB1.pdf', llm4)
pdf_loader = PyPDFLoader('./resources/AGB1.pdf')
agb_pages = pdf_loader.load()
embeddings = OpenAIEmbeddings()
db = DocArrayInMemorySearch.from_documents(agb_pages, embedding=embeddings)

llm_parser.retrieval_chain = RetrievalQA.from_chain_type(chain_type="stuff", llm=llm4, retriever = db.as_retriever())

def set_retrieval_chain(pdf_file): 
    pdf_loader = PyPDFLoader(pdf_file)
    agb_pages = pdf_loader.load()
    embeddings = OpenAIEmbeddings()
    db = DocArrayInMemorySearch.from_documents(agb_pages, embedding=embeddings)  
    llm_parser.retrieval_chain = RetrievalQA.from_chain_type(chain_type="stuff", llm=llm4, retriever = db.as_retriever())  

def useQuery(query):
    # Implement your method logic here
    # e.g., perform some operation with the query and return the result
    print("query:{}".format(query))
    result = llm_parser.retrieval_chain(query)
    print(result)
    print(type(result))
    return result.get('result')

def on_execute():
    query = input_text.get()
    result = useQuery(query)
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.INSERT, result + "\n")

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        file_path_var.set(file_path)
        set_retrieval_chain(file_path)

# Create main window
root = tk.Tk()
root.title("PDF Query Tool")
root.geometry("600x400")

# Add components
# 1. File chooser element
file_path_var = tk.StringVar()
choose_file_button = tk.Button(root, text="Choose PDF", command=open_file)
choose_file_button.pack(pady=5)
file_path_label = tk.Label(root, textvariable=file_path_var)
file_path_label.pack(pady=5)

# 2. Input text field
input_text = tk.Entry(root, width=50)
input_text.pack(pady=5)

# 3. Text area
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=10)
text_area.pack(pady=5)

# 4. Execution button
execute_button = tk.Button(root, text="Execute", command=on_execute)
execute_button.pack(pady=5)

# Start the main loop
root.mainloop()