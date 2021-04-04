
#* Importing Libraries
import traceback
import pandas as pd
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

#* Relative Imports
from common.utils.database.db import DBClass
from .users import UsersClass
from Feasta.settings import *

#* Initializing Logs
from common.utils.logging.logger import *
logger = LogClass().get_logger('authentication')

#* Defining Objects

DB_OBJECT = DBClass()

class AuthenticationClass(UsersClass):
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
        
        logging.info("AuthenticationClass : get_db_connection : function called")
        return DB_OBJECT.database_connection()
    
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
                - 0 : Successful
                - 1 : Insertion Failed
                - 2 : Email id already exists
                - 3 : Unknown Error occurred
        '''

        logging.info("AuthenticationClass : register_user : execution start")
        
        try:
            #? Getting Database Connection
            connection,_ = self.get_db_connection()
            
            #? Checking if Some user exists with the same email address
            sql_command = f"select u.password from feasta.users u where email_id = '{email}'"
            password_df = DB_OBJECT.select_records(connection, sql_command)
            
            if not isinstance(password_df, pd.DataFrame):
                #! Function failed to select
                connection.close()
                logging.error(f"AuthenticationClass : register_user : function failed : Got Nonetype from Email selection query")
                return 3
            
            elif len(password_df) == 0:
                #? No user with the same email address
                
                #? Building data for insertion
                data = [(first_name,last_name,email,password,mobile_number)]
                table_name,cols = super().get_user_tbl_params()
                
                #? Inserting data
                status,user_id = DB_OBJECT.insert_records(connection, table_name, data, cols, index = 'user_id', Flag= 1)
                user_dict = super().get_user_details(user_id, connection)

                if isinstance(user_dict, str):
                    #? Failed to fetch user details
                    return 4

                else:
                    status = self.send_email(user_dict['first_name'],user_id)
                    
            else:
                #? User exists with the same email
                connection.close()
                logging.error(f"AuthenticationClass : register_user : execution stop : User Exists with the same Email")
                return 2
            
            logging.info(f"AuthenticationClass : register_user : execution stop : status = {str(status)}")
            
            connection.close()
            return status
        
        except Exception as e:
            
            connection.close()
            logging.info(f"AuthenticationClass : register_user : Function Failed : {str(e)}")
            return 3
    
    def send_email(self,user_name,user_id):
        template = render_to_string('./authentication_email.html',{'user_name': user_name, 'user_id': user_id})

        email = EmailMessage(
            'Confirm Regestration',
            template,
            EMAIL_HOST_USER,
            ["jayshukla0034@gmail.com"],
        )
        email.fail_silently = False
        email.send()
        return 0

    def email_validation(self, x):
        '''
            Validates the email syntex.
            
            Args:
            ----
            x (`String`): Email String
            
            Returns:
            -------
            flag (`Boolean`): Is it valid or not.
                - 0 : Valid
                - 1 : Invalid
        '''
        
        a=0
        y=len(x)
        dot=x.find(".")
        at=x.find("@")
        for i in range (0,at):
            if((x[i]>='a' and x[i]<='z') or (x[i]>='A' and x[i]<='Z')):
                a=a+1
        if(a>0 and at>0 and (dot-at)>0 and (dot+1)<y):
            return 0
        else:
            return 1
        
    def login_user(self, email, password):
        '''
            For user regestration.
            
            Args:
            ----
            email (`String`): Email of the user.
            password (`String`): Password of the user.
            
            Returns:
            --------
            Status (`Boolean`): Login Status.
        '''

        try:
            logging.info("AuthenticationClass : login_user : execution start")
            
            connection,_ = self.get_db_connection()
            
            sql_command = f"select u.password from feasta.users u where email_id = '{email}'"
            password_df = DB_OBJECT.select_records(connection, sql_command)
            
            if not isinstance(password_df, pd.DataFrame):
                    #? Function failed to select
                    
                    connection.close()
                    logging.error(f"AuthenticationClass : login_user : function failed : Got Nonetype from Email selection query")
                    return 2
                
            elif len(password_df) == 0:
                connection.close()
                return 1
            
            original_password = str(password_df['password'][0])
            
            if password == original_password:
                #? Success
                status = 0
            else:
                #? Incorrect Password
                status = 1
            
            logging.info(f"AuthenticationClass : login_user : execution stop : status = {str(status)}")
            
            connection.close()
            return status
        
        except Exception as e:
            connection.close()
            logging.info(f"AuthenticationClass : login_user : Function Failed : {str(e)}")
            return 2
