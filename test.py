from transaction import Transaction
from storage import MemoryStorage
from storage import WrapStorage

def raise_exception(msg:str):
    raise Exception(msg)


def test_happy_path():
    
    database = MemoryStorage()
    database.add("A")
    database.add("B")
    database.add("C")
    
    with Transaction(database) as tran: 
        tran.change(1,"B","E")     
        tran.change(2,"C","D")
        tran.commit()
    
    assert database.get(0)=="A"
    assert database.get(1)=="E"
    assert database.get(2)=="D"
   
def test_self_rollback():
    """
    Test if we call exit.rollback when there is an exception
    in commit function
    """
    
    database = WrapStorage()
    database.add("A")
    database.add("B")
    database.add("C")
    
    with Transaction(database) as tran:      
        tran.change(2,"C","D")
        #artifically throw exception
        database.before_change(lambda : raise_exception("Exception thrown"))
        tran.commit()
        
    assert database.get(0)=="A"
    assert database.get(1)=="B"
    assert database.get(2)=="C"

def test_self_rollback2():
    """
    Test if we call exit.rollback when the 
    transaction is not commited
    """
    
    database = WrapStorage()
    database.add("A")
    database.add("B")
    database.add("C")
    
    with Transaction(database) as tran:      
        tran.change(2,"C","D")
        
    assert database.get(0)=="A"
    assert database.get(1)=="B"
    assert database.get(2)=="C" 
    
def test_self_rollback3():
    """
    Test if we call exit.rollback when there is an exception
    in commit function.
    
    Testing what happen when 1 change is successful and another change
    fail
    """
    
    database = WrapStorage()
    database.add("A")
    database.add("B")
    database.add("C")
    
    with Transaction(database) as tran: 
        tran.change(1,"B","E")
        tran.change(2,"C","D")
        #artifically throw exception
        database.before_change_time(lambda : raise_exception("Exception thrown"),2)
        tran.commit()
            
    assert database.get(0)=="A"
    assert database.get(1)=="B"
    assert database.get(2)=="C"

def test_rollback():
    """
    Test if we can call rollback manually
    """
    database = WrapStorage()
    database.add("A")
    database.add("B")
    database.add("C")
    
    with Transaction(database) as tran:       
        tran.change(2,"C","D")
        tran.rollback()
        
    assert database.get(0)=="A"
    assert database.get(1)=="B"
    assert database.get(2)=="C"   


def test_internal_rollback():
    """
    Test if the exit.rollback is called on internal exception
    """
    database = WrapStorage()
    database.add("A")
    database.add("B")
    database.add("C")
    
    with Transaction(database) as tran:
        database.before_contain(lambda : raise_exception("Exception thrown"))
        try:
            tran.change(2,"C","D")
            tran.commit()
        except Exception as e:
            pass
        finally:
            assert database.get(0)=="A"
            assert database.get(1)=="B"
            assert database.get(2)=="C"

def test_integrity_check():
    
    database = MemoryStorage()
    database.add("A")
    database.add("B")
    database.add("C")
    
    with Transaction(database) as tran:
        tran.change(0,"A","X")
        tran.change(1,"B","Y")
        #force the integrity fail
        database.change(1,"K")
        tran.commit()
        
    assert database.get(0)=="A"
    assert database.get(1)=="B"
    assert database.get(2)=="C"

def run_tests():
    test_happy_path()
    test_self_rollback()
    test_self_rollback2()
    test_self_rollback3()
    test_rollback()
    test_internal_rollback()
    test_integrity_check()

if __name__ == "__main__":
    run_tests()
