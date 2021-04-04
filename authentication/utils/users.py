
#* Importing Libraries
import pandas as pd

#* Relative Imports
from common.utils.database.db import DBClass

#* Initializing Logs
from common.utils.logging.logger import *
logger = LogClass().get_logger('authentication')

#* Defining Objects

DB_OBJECT = DBClass()

class UsersClass:
    '''
        For all the User related Functions.
            - Get User Details
            - Delete User
            - Update User
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

    def get_user_details(self, user_id, connection = None):
        '''
            Used to get User Specific Details.

            Args:
            -----
            user_id (`Intiger`): User's ID in the user table.
            connection (`pycopg2.connection` | default `None`): Postgres connection object.
            
            Returns:
            -------
            `Dictionary` : A dictionary containing below keys;
                - first_name (`String`)
                - last_name (`String`)
                - email_id (`String`)
                - password (`String`)
                - mobile_number (`String`)
        '''

        try:
            logging.info("Users : UsersClass : get_user_details : execution start")
        
            created_conn = False
            if connection == None:
                #? Getting Database Connection
                created_conn = True
                connection,_ = self.get_db_connection()

            #? Getting User Table Name
            table_name,cols = self.get_user_tbl_params()
            
            sql_command = f"select * from {table_name} u where u.user_id = '{user_id}'"
            logging.info("Sql_Command -> "+sql_command)
            user_details_df = DB_OBJECT.select_records(connection, sql_command)
            if created_conn: connection.close()
            
            #? Is dataframe returned Properly?
            if not isinstance(user_details_df, pd.DataFrame):
                #? Function failed to select
                logging.error(f"Users : UsersClass : get_user_details : execution failed : Got Nonetype from Email selection query")
                return "Nonetype Error"
            
            #? No data found?
            elif len(user_details_df) == 0:
                first_name = None
                last_name = None
                email_id = None
                password = None
                mobile_number = None
        
            #? Data found correctly
            else:
                first_name = user_details_df['first_name'][0]
                last_name = user_details_df['last_name'][0]
                email_id = user_details_df['email_id'][0]
                password = user_details_df['password'][0]
                mobile_number = user_details_df['mobile_number'][0]

            logging.info("Users : UsersClass : get_user_details : execution stop")

            return {
                'first_name' :first_name,
                'last_name' :last_name,
                'email_id' :email_id,
                'password' :password,
                'mobile_number' :mobile_number,
            }

        except Exception as e:
            
            logging.info(f"Users : UsersClass : get_user_details : execution failed : {str(e)}")
            return str(e)
    
