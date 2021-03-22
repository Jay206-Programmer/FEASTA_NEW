
#* Importing Libraries
import logging
import traceback

#* Relative Imports
from common.utils.database.db import DBClass

#* Initializing Logs
from common.utils.logging.logger import LogClass

user_name = 'admin'
log_enable = True
LogObject = LogClass(user_name,log_enable)
LogObject.log_setting()
logger = logging.getLogger('authentication')

#* Defining Objects

DB_OBJECT = DBClass()

class AuthenticationClass:
    '''
        This Class Handles Authentication related Functionalities.
            - Login
            - Register
    '''
    
    def get_db_connection(self):
        '''
            To get Database Connection object.
            
            Returns:
            --------
            connection (`object`): Postgres Connection Object.
            connection_string (`String`): Postgres Connection url.
        '''
        
        logging.info("Authentication : AuthenticationClass : get_db_connection : function called")
        return DB_OBJECT.database_connection()
    
    def get_user_tbl_params(self):
        '''
            To get user_tbl related parameters.
            
            Args:
            ----
            None
            
            Returns:
            -------
            table_name (`String`): Name of the user table.
            column_names (`String`): String containing column names saperated by a ",".
        '''
        
        logging.info("Authentication : AuthenticationClass : get_user_tbl_params : execution start")
        
        table_name = "feasta.users"
        column_names = \
            "first_name, \
            last_name, \
            email_id, \
            password, \
            mobile_number"
        
        logging.info("Authentication : AuthenticationClass : get_user_tbl_params : execution stop")
        
        return table_name, column_names
    
    def register_user(self, first_name, last_name, password, email, mobile_number):
        '''
            For user regestration.
            
            Args:
            ----
            first_name (`String`): First Name of the user.
            last_name (`String`): Last Name of the user.
            password (`String`): Password of the user.
            email (`String`): Email of the user.
            phone_number (`String`): Phone Number of the user.
            
            Returns:
            --------
            Status (`Boolean`): Status of Insertion.
        '''

        logging.info("Authentication : AuthenticationClass : register_user : execution start")
        
        data = tuple(first_name,last_name,email,password,mobile_number)
        table_name,cols = self.get_user_tbl_params()
        
        connection,_ = self.get_db_connection()
        
        status = DB_OBJECT.insert_records(connection, table_name, data, cols)
        
        logging.info(f"Authentication : AuthenticationClass : register_user : execution stop : status = {str(status)}")
        
        return status