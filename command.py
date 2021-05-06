class Command:
    def __init__(self,from_id:int,from_data:str,to_data:str):
        self.__from_id = from_id
        self.__from_data = from_data
        self.__to_data = to_data
        
    def get_from_id(self)->int:
        return self.__from_id
    
    def get_from_data(self)->str:
        return self.__from_data
    
    def get_to_data(self)->str:
        return self.__to_data
    
    