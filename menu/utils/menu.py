
#* Importing Libraries
import logging
import traceback
import pandas as pd

#* Relative Imports
from common.utils.database.db import DBClass

#* Initializing Logs
from common.utils.logging.logger import LogClass
logger = LogClass().get_logger('menu')

#* Defining Objects

DB_OBJECT = DBClass()

class MenuClass:
    '''
        For managing menu related functionalities.
            - Add Category
            - Update Category
            - Delete Category
            - Add Menu Item
            - Update Menu Item
            - Delete Menu Item
            - Get Menu Details
    '''
    
    def get_db_connection(self):
        '''
            To get Database Connection object.
            
            Returns:
            --------
            connection (`object`): Postgres Connection Object.
            connection_string (`String`): Postgres Connection url.
        '''
        
        logging.info("Menu : MenuClass : get_db_connection : function called")
        return DB_OBJECT.database_connection()
    
    def get_category_tbl_params(self):
        '''
            To get category table related parameters.
            
            Args:
            ----
            None
            
            Returns:
            -------
            table_name (`String`): Name of the user table.
            column_names (`String`): String containing column names saperated by a ",".
        '''
        
        logging.info("Menu : MenuClass : get_category_tbl_params : execution start")
        
        table_name = "feasta.category"
        column_names = \
            "admin_id, \
            category_name, \
            category_desc, \
            image_path"
            
        logging.info("Menu : MenuClass : get_category_tbl_params : execution stop")
        
        return table_name, column_names
    
    def get_menu_tbl_params(self):
        '''
            To get menu table related parameters.
            
            Args:
            ----
            None
            
            Returns:
            -------
            table_name (`String`): Name of the user table.
            column_names (`String`): String containing column names saperated by a ",".
        '''
        
        logging.info("Menu : MenuClass : get_menu_tbl_params : execution start")
        
        table_name = "feasta.menu"
        column_names = \
            "item_name, \
            item_desc, \
            category_id, \
            price, \
            image_path"
            
        logging.info("Menu : MenuClass : get_menu_tbl_params : execution stop")
        
        return table_name, column_names
    
    def add_category(self, admin_id, category_name, category_desc, image_path):
        '''
            To add Food Category.
            
            Args:
            ----
            admin_id (`Integer`): Id of the admin.
            category_name (`String`): Name of the category.
            category_desc (`String`): Description for the category.
            image_path (`String`): Path where the image is stored.
            
            Returns:
            -------
            status (`Integer`): Status of the insertion.
            category_index (`Integer`): Index of the entry in the category table.
        '''

        logging.info("Menu : MenuClass : add_category : execution start")

        #? Getting Database Connection
        connection,_ = self.get_db_connection()
            
        #? Checking if Some user exists with the same email address
        sql_command = f"select c.category_id from feasta.category c where c.category_name  = '{category_name}'"
        category_df = DB_OBJECT.select_records(connection, sql_command)

        if not isinstance(category_df, pd.DataFrame):
            #? Function failed to select
            
            logging.error(f"Menu : MenuClass : add_category : function failed : Got Nonetype from Category Name selection query")
            return 3
            
        elif len(category_df) == 0:
            #? No category with the same name
                
            #? Building data for insertion
            data = [(admin_id,category_name,category_desc,image_path)]
            table_name,cols = self.get_category_tbl_params()
            
            #? Inserting data
            status,index = DB_OBJECT.insert_records(connection, table_name, data, cols, Flag=1)

        else:
            logging.error(f"Menu : MenuClass : add_category : function failed : More than one categories with the same name exists")
            return 2

        logging.info("Menu : MenuClass : add_category : execution stop")

        return status,index