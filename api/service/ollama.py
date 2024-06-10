from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_community.llms import Ollama

from . import shell
from .retriever import Retriever
from .utils import system_template_str


class ChatBot:
    def __init__(self, chat_model: str = "llama3", ollama_base_url: str = r"http://localhost:11434",
                 chroma_host: str = "localhost", chroma_port: int = 8000, chroma_collection: str = "test"):
        self.chat_model = Ollama(model=chat_model, base_url=ollama_base_url)
        shell.print_green_message(f"Ollama model loaded: {chat_model} at URL {ollama_base_url}")

        self.chroma_collection = chroma_collection
        self.chroma_host = chroma_host
        self.chroma_port = chroma_port
        self.retriever = Retriever(chroma_host=chroma_host, chroma_port=chroma_port,
                                   chroma_collection=chroma_collection)
        shell.print_green_message(f"Retriever loaded for collection: {chroma_collection}")

        self.system_template_str = system_template_str

        self.system_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["context"], template=self.system_template_str
            )
        )
        self.human_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=["question"], template="{question}")
        )

        self.messages = [self.system_prompt, self.human_prompt]

        self.prompt_template = ChatPromptTemplate(
            input_variables=["context", "question"],
            messages=self.messages,
        )

        self.review_chain = self.prompt_template | self.chat_model

    def get_context(self, query):
        response = self.retriever.retrieve(query=query)
        ids = response["ids"]
        symbols = response["symbols"]
        dates = response["dates"]
        titles = response["titles"]
        documents = response["documents"]

        final_string = ""
        for i in range(len(ids)):
            final_string += (f"BEGIN OF EXTRACT\n\n"
                             f"Symbol: {symbols[i]}\n"
                             f"Document Title: {titles[i]}\n"
                             f"Date: {dates[i]}\n"
                             f"Extract:\n{documents[i]}\n\nEND OF EXTRACT\n"
                             )
        return final_string

    def invoke(self, question):
        context = self.get_context(question)
        for s in self.review_chain.stream({"context": context, "question": question}):
            yield s
