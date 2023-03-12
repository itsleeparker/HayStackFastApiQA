class REST_HEADER():
    message:str
    status:int
    data : any
    def __init__(self , params) -> None:
        print(params)
        self.message = params['message']
        self.status = params['status'] 
        self.data = params['data']
