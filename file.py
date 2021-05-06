import os

def file_write(file_location:str,data:str)->bool:
    with open(file_location,mode="a") as file:
        try:
             file.write(data+"\n")
             return True
        except Exception:
            return False

def file_write_lines(file_location:str,lines:list)->bool:
    with open(file_location,mode="w") as file:
        try:
             file.writelines(lines)
             return True
        except Exception:
            return False
        
def file_exist(file_location:str)->bool:
    return os.path.exists(file_location)

def file_read(file_location:str)->list:    
    try:
        with open(file_location,mode="rt") as file:
            return file.readlines()
    except Exception:
        return list()
    
def file_delete(file_location:str)->bool:
    
    if not file_exist(file_location):
        return True
    
    try:
        os.remove(file_location)
        return True
    except Exception:
        return False
    
def file_change(file_location:str,line_index:int,data:str)->bool:
    if line_index<0:
        return False
    
    lines = file_read(file_location)
    
    if line_index>=len(lines):
        return False
    
    lines[line_index] = data+"\n"
        
    file_write_lines(file_location,lines)
    
    return True
     
