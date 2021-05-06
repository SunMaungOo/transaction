class LogData:
    def __init__(self,from_id:int,from_data:str):
        self.__from_id = from_id
        self.__from_data = from_data
        
    def get_from_id(self)->int:
        return self.__from_id
    
    def get_from_data(self)->str:
        return self.__from_data
    
    def __str__(self):
        return str.format("{0},{1}",self.__from_id,self.__from_data)
    