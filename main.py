from fastapi import FastAPI
from REST_HEADER import REST_HEADER
from uvicorn import uvicorn
from QAModel import QuestionAnswerAI
from pydantic import BaseModel

##Setup server 
app = FastAPI()
QA = QuestionAnswerAI()

class askQuestionPayload(BaseModel):
    question:str = None

#set Up the server 
@app.get("/healthcheck")
async def healthcheck():
    args:any= {
        "message"  : "Server Up and Running" , 
        "status" : 200 ,
        "data" : ''
    }
    results= REST_HEADER(args)
    return results

@app.post("/askQuestion")
async def askQuestion(question:askQuestionPayload):
    try:
        args = {
            "message" : "QA Response" , 
            "status" : 200 , 
            "data" : QA.getAnswer(question=question.question)
        } 
    except :
        args={
            "message" : "Failed to get Response" , 
            "status" : 500 , 
            "data" : {}
        }
    results =  REST_HEADER(args)
    return results


@app.post("/test")
async def checkPayload(item:askQuestionPayload):
    print(item)
    return item
    