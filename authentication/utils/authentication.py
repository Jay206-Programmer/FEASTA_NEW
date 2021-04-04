
#* Importing Libraries
from re import template
import traceback
import pandas as pd
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import threading
import uuid

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
                    #? Creating unique id
                    unique_id = str(uuid.uuid1().int)
                    i = 0
                    temp = user_id
                    while temp >= 1:
                        temp /= 10
                        i += 1
                    #? Embedding userid & length of userid
                    new_unique_id = unique_id+str(user_id)+str(i)
                    
                    sql_command = f"update feasta.users set verification_code = '{unique_id}' where user_id = '{user_id}'"
                    update_status = DB_OBJECT.update_records(connection, sql_command)

                    t1 = threading.Thread(target=self.send_email, args=(user_dict['first_name'],user_dict['email_id'],new_unique_id))
                    t1.start()
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
    
    def send_email(self,user_name,email,unique_id):
        with open('authentication/utils/authentication_email.html') as tmp:
            template = tmp.read()

        template = template.replace('{{user_name}}', str(user_name))
        template = template.replace('{{user_id}}', str(unique_id))
        email = EmailMessage(
            'Confirm Regestration',
            template,
            EMAIL_HOST_USER,
            ["jayshukla0034@gmail.com"],
        )
        email.fail_silently = False
        email.send()
        return 0

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
            user_id (`String`): User_id of the logged in user.
        '''

        try:
            logging.info("AuthenticationClass : login_user : execution start")
            
            connection,_ = self.get_db_connection()
            
            sql_command = f"select u.user_id,u.password from feasta.users u where email_id = '{email}'"
            password_df = DB_OBJECT.select_records(connection, sql_command)
            
            if not isinstance(password_df, pd.DataFrame):
                    #? Function failed to select
                    
                    connection.close()
                    logging.error(f"AuthenticationClass : login_user : function failed : Got Nonetype from Email selection query")
                    return 3,None
                
            elif len(password_df) == 0:
                connection.close()
                return 1,None
            
            original_password = str(password_df['password'][0])
            user_id = str(password_df['user_id'][0])
            if password == original_password:
                #? Success
                status = 0
                sql_command = f"update feasta.users set login_status = '1'  where user_id = '{user_id}';"
                update_status = DB_OBJECT.update_records(connection, sql_command)
                if update_status == 1: 
                    logging.error("AuthenticationClass : login user : function failed : Failed to update the login status")
                    status = 2
            else:
                #? Incorrect Password
                status = 1
            
            logging.info(f"AuthenticationClass : login_user : execution stop : status = {str(status)}")
            
            connection.close()
            return status,user_id
        
        except Exception as e:
            connection.close()
            logging.info(f"AuthenticationClass : login_user : Function Failed : {str(e)}")
            return 3,None

    def verify_uniqueid(self, u_id):
        length = int(u_id[-1])
        u_id = u_id[:-1]
        user_id = u_id[len(u_id)-length:]
        u_id = u_id[:len(u_id)-length]
        return user_id,u_id