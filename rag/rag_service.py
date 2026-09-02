#实现一个RAG服务的总结服务类：用户提问，搜索参考资料，将提问和参考资料一起提交给模型

from rag.vector_store import VectorStoreService
from utils.prompt_handler import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()    
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text= load_rag_prompts()   #加载RAG的prompt模板
        self.prompt_template= PromptTemplate.from_template(self.prompt_text)   #将prompt模板转为PromptTemplate对象
        self.model = chat_model
        self.chain = self._init_chain()


    
    def _init_chain(self): 
        """返回一个链对象"""
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str)->list[Document]:
        """根据用户的query，检索相关的文档"""
        docs = self.retriever.invoke(query)
        return docs

    def rag_summarize(self, query: str)->str:
        """根据用户的query，检索相关的文档，并将query和文档一起提交给模型，返回模型的输出"""
        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"参考资料{counter}:{doc.page_content}|参考元数据：{doc.metadata}\n"
        #直接返回执行链条，根据提示词模板将input和context注入
        return self.chain.invoke(
            {"input": query, 
             "context": context}
            )

if __name__ == "__main__":
    rag=RagSummarizeService()
    print(rag.rag_summarize("小户型适合哪种扫地机器人"))