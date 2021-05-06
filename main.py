from transaction import Transaction
from storage import FileStorage
from log_data import LogData
from config import DATABASE_NAME

if __name__ == "__main__":
        
    database = FileStorage(DATABASE_NAME,True)    
    database.add("A")
    database.add("B")
    database.add("C")    
    
    with Transaction(database) as tran:    
        tran.change(2,"C","D")
        tran.change(1,"B","E")
        print(tran.commit())
    
    database.print()
    
    