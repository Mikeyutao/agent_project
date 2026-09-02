#文本->向量存储功能
from langchain_chroma import Chroma
from utils.config_handler import chroma_conf
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from utils.path_tool import get_abs_path
from utils.file_handler import txt_loader,pdf_loader,\
    listdir_with_allowed_type,get_file_md5_hex
from utils.logger_handler import logger
from langchain_core.documents import Document
class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name = chroma_conf["collection_name"],   #表名
            embedding_function = embed_model,    #指定模型
            persist_directory = chroma_conf["persist_directory"]    #数据库路径
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = chroma_conf["chunk_size"], 
            chunk_overlap= chroma_conf["chunk_overlap"],
            separators = chroma_conf["separators"],
            length_function = len
        )

    #获取检索器
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def Load_document(self):
        """
        从数据文件夹内读取文件，转为向量存入向量库
        计算文件的MD5做去重
        """

        def check_md5_hex(md5_for_check:str):
            #如果md5记录文件不存在，当前文件肯定没处理过，先创建一个存放文件的md5的文件
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]),"w",encoding="utf-8").close()
                return False

            with open(get_abs_path(chroma_conf["md5_hex_store"]),"r",encoding="utf-8") as f:
                for line in f:
                    if line.strip() == md5_for_check:
                        return True    #表示md5被处理过
                #没找到md5，说明没处理过
                return False

        #保存md5
        def save_md5_hex(md5_for_save:str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]),"a",encoding="utf-8") as f:
                f.write(md5_for_save+"\n")

        #获取文件
        def get_file_documents(read_path:str):
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            elif read_path.endswith(".txt"):
                return txt_loader(read_path)
            else:
                return []
            
        #获取允许文件列表
        allowed_files_path = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"])
            )

        
        #开始遍历，加载文件
        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):   #如果md5被处理过，则跳过
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue

            try:
                documents:list[Document] = get_file_documents(path)

                if not documents:   #如果没内容，则跳过
                    logger.info(f"[加载知识库]{path}内容为空，跳过")
                    continue

                split_document:list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}没有有效文本内容，跳过")
                    continue

                self.vector_store.add_documents(split_document)

                #记录已经处理好的文件md5值
                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库]{path}内容加载成功")

            except Exception as e:
                #exc_info为True会记录详细的报错堆栈，如果为False则只记录错误信息
                logger.error(f"[加载知识库]{path}发生错误：{str(e)}", exc_info=True)
                continue


if __name__ == "__main__":
    vector_store = VectorStoreService()
    vector_store.Load_document()

    retriever = vector_store.get_retriever()

    res = retriever.invoke("手机APP连接问题")

    for r in res:
        print(r.page_content)
        print("*"*20)
        



