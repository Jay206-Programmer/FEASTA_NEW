
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
from .admin import AdminsClass
from Feasta.settings import *

#* Initializing Logs
from common.utils.logging.logger import *
logger = LogClass().get_logger('authentication')

#* Defining Objects

DB_OBJECT = DBClass()

class AuthenticationClass(UsersClass,AdminsClass):
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

                    t1 = threading.Thread(target=self.send_email, args=(user_dict['first_name'],user_dict['email_id'],new_unique_id,'authentication/utils/authentication_email.html'))
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
    
    def send_email(self,user_name,email,unique_id,template_path):
        with open(template_path) as tmp:
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
            user_dict = super().get_user_details(user_id, connection)
            user_dict['user_id'] = user_id

            if isinstance(user_dict, str):
                #? Failed to fetch user details
                connection.close()
                return 3,None

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
            return status,user_dict
        
        except Exception as e:
            connection.close()
            logging.info(f"AuthenticationClass : login_user : Function Failed : {str(e)}")
            return 3,None

    def verify_uniqueid(self, u_id, flag = 0):
        '''
            Used to Verify the email id.

            Args:
            -----
            u_id (`String`): Unique id received from the url.
            flag (`String`): Who is verifying?
                - 0 : User
                - 1 : Admin

            Returns:
            -------
            Message (`String`): Message that will be shown when the user clicks the link in email.
        '''

        try:
            length = int(u_id[-1])
            u_id = u_id[:-1]
            user_id = u_id[len(u_id)-length:]
            u_id = u_id[:len(u_id)-length]
            
            if flag == 0:
                table_name = 'feasta.users'
                index = 'user_id'
            elif flag == 1:
                table_name = 'feasta.admins'
                index = 'admin_id'

            #? Getting Database Connection
            connection,_ = self.get_db_connection()

            sql_command = f"select case when u.verification_code = '{u_id}' then '1' else '0' end as status from {table_name} u  where u.{index} = '{user_id}'"
            status_df = DB_OBJECT.select_records(connection, sql_command)
            
            if not isinstance(status_df,pd.DataFrame):
                connection.close()
                return "Server Error! Retry Clicking on that link."
            status = str(status_df['status'][0])
            
            if status == "1":
                sql_command = f"update {table_name} set verification_status = '1' where {index} = '{user_id}';"
                update_status = DB_OBJECT.update_records(connection, sql_command)
                connection.close()
                return "Verification Successful, Now visit the site and Login."
            else:
                connection.close()
                return "Verification Failed! Use the correct Link."
            
            
        except Exception as e:
            connection.close()
            return str(e)

    def get_user_login_status(self, user_id):
        '''
            Used to get login status of the user.

            Args:
            ----
            user_id (`String | Int`): Id of the user.

            Return:
            ------
            status (`Integer`): Status of the login
                - 0 : User is not logged in. 
                - 1 : User is logged in.
                - -1 : No user found for that user id
                - -2 : Failed to fetch the data 
        '''
        try:
            #? Getting Database Connection
            connection,_ = self.get_db_connection()

            sql_command = f"select u.login_status from feasta.users u where u.user_id = '{str(user_id)}'"
            login_status_df = DB_OBJECT.select_records(connection, sql_command)
            connection.close()

            if not isinstance(login_status_df,pd.DataFrame):
                #? Failed To extract user data
                logging.info(f"get_user_login_status : Failed to extract login status for user {user_id}")
                return -2
            
            elif len(login_status_df) == 0:
                logging.info(f"get_user_login_status : No user for user_id {user_id}")
                return -1

            else:
                logging.info("get_user_login_status : Successfully fetched User login status")
                return int(login_status_df['login_status'][0])
        
        except Exception as e:
            logging.error(f"get_user_login_status : Exception Occurred : {str(e)}")
            return -2

    def register_admin(self, first_name, last_name, password, email, mobile_number, canteen_name):
        '''
            For user regestration.
            
            Args:
            ----
            first_name (`String`): First Name of the user.
            last_name (`String`): Last Name of the user.
            password (`String`): Password of the user.
            email (`String`): Email of the user.
            phone_number (`String`): Phone Number of the user.
            canteen_name (`String`): Name of the canteen.
            
            Returns:
            --------
            Status (`Boolean`): Status of Insertion.
                - 0 : Successful
                - 1 : Insertion Failed
                - 2 : Email id already exists
                - 3 : Unknown Error occurred
        '''

        logging.info("AuthenticationClass : register_admin : execution start")
        
        try:
            #? Getting Database Connection
            connection,_ = self.get_db_connection()
            
            #? Checking if Some user exists with the same email address
            sql_command = f"select a.password from feasta.admins a where email_id = '{email}'"
            password_df = DB_OBJECT.select_records(connection, sql_command)
            
            if not isinstance(password_df, pd.DataFrame):
                #! Function failed to select
                connection.close()
                logging.error(f"AuthenticationClass : register_admin : function failed : Got Nonetype from Email selection query")
                return 3
            
            elif len(password_df) == 0:
                #? No admin with the same email address
                
                #? Inserting Canteen Details
                area = None
                city = None

                data = [(canteen_name,area,city)]
                table_name = 'feasta.canteens'
                cols = 'canteen_name,area,city'
                status,canteen_id = DB_OBJECT.insert_records(connection, table_name, data, cols, index = 'canteen_id', Flag= 1)
                
                #? Building data for insertion
                data = [(canteen_id,first_name,last_name,email,password,mobile_number)]
                table_name,cols = super().get_admin_tbl_params()
                
                #? Inserting data
                status,admin_id = DB_OBJECT.insert_records(connection, table_name, data, cols, index = 'admin_id', Flag= 1)
                admin_dict = super().get_admin_details(admin_id, connection)

                if isinstance(admin_dict, str):
                    #? Failed to fetch user details
                    return 4

                else:
                    #? Creating unique id
                    unique_id = str(uuid.uuid1().int)
                    i = 0
                    temp = admin_id
                    while temp >= 1:
                        temp /= 10
                        i += 1
                    #? Embedding userid & length of userid
                    new_unique_id = unique_id+str(admin_id)+str(i)
                    
                    sql_command = f"update feasta.admins set verification_code = '{unique_id}' where admin_id = '{admin_id}'"
                    update_status = DB_OBJECT.update_records(connection, sql_command)

                    #? Sending Email
                    t1 = threading.Thread(target=self.send_email, args=(admin_dict['first_name'],admin_dict['email_id'],new_unique_id,'authentication/utils/Admin_Authentication_Mail.html'))
                    t1.start()
            else:
                #? User exists with the same email
                connection.close()
                logging.error(f"AuthenticationClass : register_admin : execution stop : User Exists with the same Email")
                return 2
            
            logging.info(f"AuthenticationClass : register_admin : execution stop : status = {str(status)}")
            
            connection.close()
            return status
        
        except Exception as e:
            
            connection.close()
            logging.info(f"AuthenticationClass : register_admin : Function Failed : {str(e)}")
            return 3
    
    def login_admin(self, email, password):
        '''
            For user regestration.
            
            Args:
            ----
            email (`String`): Email of the user.
            password (`String`): Password of the user.
            
            Returns:
            --------
            Status (`Boolean`): Login Status.
            admin_id (`String`): admin_id of the logged in admin.
        '''

        try:
            logging.info("AuthenticationClass : login_admin : execution start")
            
            connection,_ = self.get_db_connection()
            
            sql_command = f"select a.admin_id,a.password from feasta.admins a where email_id = '{email}'"
            password_df = DB_OBJECT.select_records(connection, sql_command)
            
            if not isinstance(password_df, pd.DataFrame):
                    #? Function failed to select
                    
                    connection.close()
                    logging.error(f"AuthenticationClass : login_admin : function failed : Got Nonetype from Email selection query")
                    return 3,None
                
            elif len(password_df) == 0:
                connection.close()
                return 1,None
            
            original_password = str(password_df['password'][0])
            admin_id = str(password_df['admin_id'][0])
            admin_dict = super().get_admin_details(admin_id, connection)
            admin_dict['admin_id'] = admin_id

            if isinstance(admin_dict, str):
                #? Failed to fetch admin details
                connection.close()
                return 3,None

            if password == original_password:
                #? Success
                status = 0
                sql_command = f"update feasta.admins set login_status = '1'  where admin_id = '{admin_id}';"
                update_status = DB_OBJECT.update_records(connection, sql_command)
                if update_status == 1: 
                    logging.error("AuthenticationClass : login user : function failed : Failed to update the login status")
                    status = 2
            else:
                #? Incorrect Password
                status = 1
            
            logging.info(f"AuthenticationClass : login_admin : execution stop : status = {str(status)}")
            
            connection.close()
            return status,admin_dict
        
        except Exception as e:
            connection.close()
            logging.info(f"AuthenticationClass : login_admin : Function Failed : {str(e)}")
            return 3,None
