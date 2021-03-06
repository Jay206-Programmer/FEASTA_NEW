
#* Importing Libraries
import pandas as pd

#* Relative Imports
from common.utils.database.db import DBClass

#* Initializing Logs
from common.utils.logging.logger import *
logger = LogClass().get_logger('authentication')

#* Defining Objects

DB_OBJECT = DBClass()

class AdminsClass:
    '''
        For all the Admin related Functions.
            - Get Admin Details
            - Delete Admin
            - Update Admin
    '''

    def get_db_connection(self):
        '''
            To get Database Connection object.
            
            Returns:
            --------
            connection (`object`): Postgres Connection Object.
            connection_string (`String`): Postgres Connection url.
        '''
        
        logging.info("AdminsClass : get_db_connection : function called")
        return DB_OBJECT.database_connection()
    
    def get_admin_tbl_params(self):
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
        
        logging.info("AdminsClass : get_admin_tbl_params : execution start")
        
        table_name = "feasta.admins"
        column_names = \
            "canteen_id, \
            first_name, \
            last_name, \
            email_id, \
            password, \
            mobile_number"
        
        logging.info("AdminsClass : get_admin_tbl_params : execution stop")
        
        return table_name, column_names

    def get_admin_details(self, admin_id, connection = None):
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
                - canteen_id (`String`)
                - canteen_name (`String`)
                - area (`String`)
                - city (`String`)
        '''

        try:
            logging.info("AdminsClass : get_admin_details : execution start")
        
            created_conn = False
            if connection == None:
                #? Getting Database Connection
                created_conn = True
                connection,_ = self.get_db_connection()

            #? Getting User Table Name
            table_name,cols = self.get_admin_tbl_params()
            
            sql_command = f"select a.*,c.canteen_name,c.area,c.city from {table_name} a ,feasta.canteens c where a.admin_id = '{admin_id}' and a.canteen_id = c.canteen_id "
            logging.info("Sql_Command -> "+sql_command)
            admin_details_df = DB_OBJECT.select_records(connection, sql_command)
            if created_conn: connection.close()
            
            #? Is dataframe returned Properly?
            if not isinstance(admin_details_df, pd.DataFrame):
                #? Function failed to select
                logging.error(f"AdminsClass : get_admin_details : execution failed : Got Nonetype from Email selection query")
                return "Nonetype Error"
            
            #? No data found?
            elif len(admin_details_df) == 0:
                first_name = None
                last_name = None
                email_id = None
                password = None
                mobile_number = None
                canteen_id = None
                canteen_name = None
                area = None
                city = None
        
            #? Data found correctly
            else:
                first_name = admin_details_df['first_name'][0]
                last_name = admin_details_df['last_name'][0]
                email_id = admin_details_df['email_id'][0]
                password = admin_details_df['password'][0]
                mobile_number = admin_details_df['mobile_number'][0]
                canteen_id = admin_details_df['canteen_id'][0]
                canteen_name = admin_details_df['canteen_name'][0]
                area = admin_details_df['area'][0]
                city = admin_details_df['city'][0]

            logging.info("AdminsClass : get_admin_details : execution stop")

            return {
                'first_name' :first_name,
                'last_name' :last_name,
                'email_id' :email_id,
                'password' :password,
                'mobile_number' :mobile_number,
                'canteen_id' : canteen_id,
                'canteen_name' : canteen_name,
                'area' : area,
                'city' : city
            }

        except Exception as e:
            
            logging.info(f"AdminsClass : get_admin_details : execution failed : {str(e)}")
            return str(e)
    
