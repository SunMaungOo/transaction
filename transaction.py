from storage import Storage
from storage import MemoryStorage
from storage import FileStorage
from command import Command
from log_data import LogData
from operation import rollback_database
from config import LOG_NAME

"""
Usage 

with Transaction() as tran:
    tran.change()
    tran.commit()

or 

with Transaction() as tran:
    tran.change()
    tran.rollback()

Optimization which can be done.

Mark the log file with "USE" when it called commit.

In recovery process , don't recovery when the log file
is not "USE". This is to prevent recovery when the 
exception just occur in change() and we don't
actually change original data yet with commit()

"""
class Transaction:
    
    def __init__(self,database:Storage):
        self.__database = database
        self.__commands = list()
        self.__is_begin = False
        self.__is_commited = False
        self.__is_rollbacked = False
         
    def __enter__(self):
        self.__begin()
        return self
    
    def __exit__(self,type,value,traceback):
        #We should not rollback if it been commited or
        #already been rollback 
        if not(self.__is_commited or self.__is_rollbacked):
            self.rollback()
      
    def __begin(self):
        
        self.__is_begin=True
        
        #self.__log = MemoryStorage()
        self.__log = FileStorage(LOG_NAME,True)
            
    def change(self,
               from_id:int,
               from_data:str,
               to_data:str):
        """
        Change the data from the database.
        The data will 
        """
        
        
        if not self.__is_begin:
            raise Exception("You must first call transaction begin")
           
        try:
            
            if not self.__database.contains(from_data):
                return False
        
            #save the original data into log file
    
            self.__log.add(LogData(from_id,from_data))

            #create the command which actually change the data
            
            self.__commands.append(Command(from_id,
                                           from_data,
                                           to_data))
        except Exception as e:
            raise Exception("Internal exception occur") from e
        
        return True
                     
    def commit(self)->bool:
        """
        Return true when we can guranteee that database have been successfully
        updated.
        
        Question : Do we actually need to know return value of commit.
        Maybe the commit should happen async , and the user doesn't 
        really need to know whether we have commited or not
        """
        
        self.__is_commited = True
        
        for command in self.__commands:
            
            from_id = command.get_from_id()
            
            from_data = command.get_from_data()
            
            to_data = command.get_to_data()
            
            try:
                #Integrity check
                if self.__is_data(self.__database,from_id,from_data):
                    self.__database.change(from_id,to_data)
                else:
                    #If the integrity check fail , we rollback 
                    # by throwing an exception
                    raise Exception("Integrity check fail")
                    
            except Exception:
                                                                
                #If something fail, we rollback
                #If we can successfully rollback , we delete the transaction log file
                
                if rollback_database(self.__database,self.__log):
                    self.__log.remove()
                
                #commit fail when the error occur
                                
                return False
            
        #at this point,we are successfully change the file , all it left
        #it do remove the log file
            
        return self.__log.remove() 
            
    def __is_data(self,
                  storage:Storage,
                  index:int,
                  data:str)->bool:
        """
        Whether the data in the index is the same
        """
        return storage.get(index)==data
    
    def rollback(self):
        """
        Manually rollback the transaction instead of commiting [commit()]
        """
        self.__is_rollbacked = True
        self.__log.remove()
        self.__commands.clear()
        