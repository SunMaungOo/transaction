from storage import Storage

def rollback_database(database:Storage,log:Storage)->bool:
    """
    Rollback the database with data from log
    Return whether we have successfully rollback or not
    log : storage which contain LogData
    """
    try:
        for data in log.get_internal():
            database.change(data.get_from_id(),
                            data.get_from_data())
    except Exception:
        #Fail to rollback
        return False
        
    return True

def recover_database(database:Storage,log:Storage)->bool:
    """
    Recover a database
    True if we have recover it.
    False if we fail to recover it.
    """
    if not rollback_database(database,log):
        return False
    
    return log.remove()

    
    
