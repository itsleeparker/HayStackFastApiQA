from QAModel import QuestionAnswerAI
from types import void

def main()->None:
    question:str = "Who is the father of Arya Stark?"
    qa = QuestionAnswerAI()
    qa.init()
    qa.getAnswer(question=question)
    

main()