import logging
import os
from pprint import pprint
from haystack import document_stores 
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import DenseRetriever  , Seq2SeqGenerator
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.utils import fetch_archive_from_http
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline


class QuestionAnswerAI():
    outDir:str
    question:str
    document_store:document_stores
    reader:FARMReader
    retriver:BM25Retriever
    pipeline:ExtractiveQAPipeline
    def __init__(self) -> None:
        self.init()
    
    def __initLogger(self)->None:
        logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
        logging.getLogger("haystack").setLevel(logging.INFO)
        print("Logs Setted")
    
    def __initDocumentStore(self)->None:
        self.document_store  = InMemoryDocumentStore(use_bm25=True)
        print("Document Store set")
    
    def __fetchAndSetSource(self):
        #Remove the fetch after first fetch 
        self.outDir = "data/src"
        fetch_archive_from_http(
            url="https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt1.zip" , 
            output_dir=self.outDir
        )
        files_to_index = [self.outDir + "/" + f for f in os.listdir(self.outDir)]
        indexing_pipeline = TextIndexingPipeline(self.document_store)
        indexing_pipeline.run_batch(file_paths=files_to_index)
        print("External Data set")
    
    def __initReaderAndRetriver(self)->None:
        self.retriver = BM25Retriever(document_store=self.document_store)
        self.reader =   FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
    
    def __setUpPipline(self)->None:
        self.pipeline = ExtractiveQAPipeline(reader=self.reader , retriever=self.retriver)
        pass
    
    def init(self) -> None:
        self.__initLogger()         #set Up Logger
        self.__initDocumentStore()  #set Up Document store 
        self.__fetchAndSetSource()  #set up all the resources
        self.__initReaderAndRetriver() #setUp reader and retriver 
        self.__setUpPipline()          #setUp Pipline 
    
    def getAnswer(self , question:str)->any:
        predictions:any = self.pipeline.run(
            query=question ,
            params={
            "Retriever": {"top_k": 10},
            "Reader": {"top_k": 5}
            }
        )
        return predictions['answers'][0].answer