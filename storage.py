from file import file_write,file_read,file_exist,file_delete,file_change
from abc import ABC,abstractmethod

class Storage(ABC):

    @abstractmethod
    def add(self,data:str)->bool:
        pass
    
    @abstractmethod
    def remove(self)->bool:
        pass
    
    @abstractmethod
    def is_removed(self)->bool:
        pass
    
    @abstractmethod
    def contains(self,data)->bool:
        pass
    
    @abstractmethod
    def get(self,index:int)->str:
        pass
    
    @abstractmethod
    def change(self,index:int,data)->bool:
        pass
    
    @abstractmethod
    def get_internal(self)->list:
        pass
    
    @abstractmethod
    def print(self):
        pass

class MemoryStorage(Storage):
    def __init__(self):
        self.__lst = list()
        
    def add(self,data:str)->bool:
        self.__lst.append(data)
        return True
    
    def remove(self)->bool:
        self.__lst.clear()
        self.__is_removed = True
        return True
    
    def is_removed(self)->bool:
        return self.__is_removed
    
    def contains(self,data)->bool:
        return data in self.__lst
    
    def get(self,index:int)->str:
        return self.__lst[index]
    
    def change(self,index:int,data)->bool:
        if index>=len(self.__lst):
            return False
        
        self.__lst[index] = data
        
        return True
    
    def get_internal(self)->list:
        return self.__lst
    
    def print(self):
        print(self.__lst)


class FileStorage(MemoryStorage):
    """
    Storage which have file as it internal implementation
    """
    def __init__(self,
                 file_name,
                 is_clear_previous=False,
                 line_converter:callable=None):
        """
        line_converter:convert a line into a object format
        """
        super().__init__()
        
        self.__is_str_data = True
                
        self.__file_name = file_name
        
        self.__line_converter = line_converter
        
        if is_clear_previous:
            file_delete(file_name)
        else:        
            #cache all the data into memory
            for line in file_read(file_name):
                if line_converter is None:
                    super().add(line)
                else:
                    super().add(line_converter(line))
                    
    def add(self,data)->bool:
        
        file_data = data
                
        self.__is_str_data = type(data)==str
        
        if not self.__is_str_data:
            file_data=str(data)
                        
        return super().add(data) and file_write(self.__file_name,file_data)
    
    def remove(self)->bool:
        return super().remove() and file_delete(self.__file_name)
    
    def is_removed(self)->bool:
        return super().is_removed() and not file_exist(self.__file_name)
    
    def contains(self,data)->bool:
        return super().contains(data)
    
    def get(self,index:int)->str:
        return super().get(index)
    
    def change(self,index:str,data)->bool:
        
        is_list_changed = super().change(index,data)
        
        if not is_list_changed:
            return False
          
        if self.__is_str_data:
            is_file_changed = file_change(self.__file_name,index,data)
        else:
            is_file_changed = file_change(self.__file_name,index,str(data))
        
        return is_file_changed
    
    def get_internal(self)->list:
        return super().get_internal()
    
    def print(self):
        super().print()
        
class WrapStorage(MemoryStorage):
    
    def __init__(self):     
        super().__init__()
        self.before_add()
        self.after_add()
        self.before_change()
        self.after_change()
        self.before_contain()
        self.after_contain()
        self.__is_before_change_time = False
        self.__current_before_change_time = 0
        self.__before_change_time = 0
            
    def before_add(self,func:callable=None):    
        self.__before_add = func
    
    def after_add(self,func:callable=None):    
        self.__after_add = func
        
    def before_change(self,func:callable=None):
        self.__before_change = func
    
    def before_change_time(self,func:callable=None,time:int=0):
        self.__is_before_change_time = True
        self.__before_change = func
        self.__before_change_time = time
        
    def after_change(self,func:callable=None):
        self.__after_change = func
        
    def before_contain(self,func:callable=None):
        self.__before_contain = func
    
    def after_contain(self,func:callable=None):
        self.__after_contain = func
           
    def __call(self,func:callable):
        """
        Call a function if it is valid
        """
        if func is not None:
            func()      
    
    def __call_clean(self,func:callable,cleanup:callable):
        """
        After calling a function , cleanup a function
        """
        try:
            self.__call(func)
        finally:
            self.__call(cleanup)
    
    def __null_before_change(self):
        self.__before_change = None
        self.__is_before_change_time = False
            
    def add(self,data:str)->bool:
        
        self.__call(self.__before_add)
        
        result = super().add(data)
        
        self.__call(self.__after_add)
        
        return result

    def change(self,index:str,data:str)->bool:
        
        if self.__is_before_change_time:
            
            self.__current_before_change_time += 1
                        
            if self.__current_before_change_time>=self.__before_change_time:
                self.__call_clean(self.__before_change,
                                  self.__null_before_change)
        else:    
            self.__call(self.__before_change)
   
        super().change(index,data)
        
        self.__call(self.__after_change)

        return True
    
    def contains(self,data)->bool:
        self.__call(self.__before_contain)
        
        result = super().contains(data)
        
        self.__call(self.__after_contain)
        
        return result