class NullValue(Exception):
    """ Null Value Exception """
    def __init__(self,status_code):
        self.msg = "Null Value"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg
    def __str__(self):
        return (self.msg)

class UserAuthenticationFailed(Exception):
    """User Authentication Failed Exception"""
    def __init__(self,status_code):
        self.msg = "User authentication failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class ArrayIndexOutOfBound(Exception):
    """ Array Index Out Of Bound Exception """
    def __init__(self,status_code):
        self.msg = "Array Index Out Of Bound"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg
    def __str__(self):
        return (self.msg)

class ValueError(Exception):
    """ Value Error Exception """
    def __init__(self,status_code):
        self.msg = "Value Error"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg
    def __str__(self):
        return (self.msg)

class DatabaseConnectionFailed(Exception):
    """ Database Connection Failed Exception """
    def __init__(self,status_code):
        self.msg = "Database Connection Failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class EntryNotFound(Exception):
    """  Entry Not Found Exception"""
    def __init__(self,status_code):
        self.msg = "Entry Not Found"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class DatabaseSchemaAlreadyExist(Exception):
    """ Database Schema Already Exist Exception """
    def __init__(self,status_code):
        self.msg = "Database Schema Already Exist"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class DatabaseTableAlreadyExist(Exception):
    """ Database Table Already Exist Exception """
    def __init__(self,status_code):
        self.msg = "Database Table Already Exist"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg


    def __str__(self):
       return (self.msg)

class DataInsertionFailed(Exception):
    """ Data Insertion Failed Exception"""
    def __init__(self,status_code):
        self.msg = "Data Insertion Failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg


    def __str__(self):
        return (self.msg)

class DataNotFound(Exception):
    """ Data Not Found Exception"""
    def __init__(self,status_code):
        self.msg = "Data Not Found"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg


    def __str__(self):
        return (self.msg)
    
class TableNotFound(Exception):
    """ Table Not Found Exception"""
    def __init__(self,status_code):
        self.msg = "Table Not Found"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class DataDeletionFailed(Exception):
    """ Data Deletion Failed Exception """
    def __init__(self,status_code):
        self.msg = "Data Deletion Failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class  TooBigFileSize(Exception):
    """  Too Big File Size Exception"""
    def __init__(self,status_code):
        self.msg = "FileSize is very large"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class  FileNotFound(Exception):
    """  File Not Found Exception"""
    def __init__(self,status_code):
        self.msg = "File Not Found"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class RecordNotFound(Exception):
    """  Record Not Found Exception"""
    def __init__(self,status_code):
        self.msg = "Records Not Found"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class RowsAndColumnsRequired(Exception):
    """  Record Not Found Exception"""
    def __init__(self,status_code):
        self.msg = "CSV must have multiple rows and columns"
        self.status_code = status_code
        self.msg = self.msg
    
    def __str__(self):
        return (self.msg)

class TableCreationFailed(Exception):
    """  Table Creation Failed Exception"""
    def __init__(self,status_code):
        self.msg = "Activity table creation failed"
        self.status_code = status_code
        self.msg = self.msg
    
    def __str__(self):
        return (self.msg)

class ActivityUpdateFailed(Exception):
    """  Activity Update Failed Exception"""
    def __init__(self,status_code):
        self.msg = "Activity update failed"
        self.status_code = status_code
        self.msg = self.msg
    
    def __str__(self):
        return (self.msg)