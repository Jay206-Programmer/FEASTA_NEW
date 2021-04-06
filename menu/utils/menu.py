
#* Importing Libraries
import pandas as pd

#* Relative Imports
from common.utils.database.db import DBClass

#* Initializing Logs
from common.utils.logging.logger import *
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
        
        logging.info("MenuClass : get_db_connection : function called")
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
        
        logging.info("MenuClass : get_category_tbl_params : execution start")
        
        table_name = "feasta.category"
        column_names = \
            "admin_id, \
            category_name, \
            category_desc, \
            image_path"
            
        logging.info("MenuClass : get_category_tbl_params : execution stop")
        
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
        
        logging.info("MenuClass : get_menu_tbl_params : execution start")
        
        table_name = "feasta.menu"
        column_names = \
            "item_name, \
            item_desc, \
            category_id, \
            price, \
            image_path"
            
        logging.info("MenuClass : get_menu_tbl_params : execution stop")
        
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

        logging.info("MenuClass : add_category : execution start")

        #? Getting Database Connection
        connection,_ = self.get_db_connection()
            
        #? Checking if Some user exists with the same email address
        sql_command = f"select c.category_id from feasta.category c where c.category_name  = '{category_name}' and c.admin_id = '{admin_id}'"
        category_df = DB_OBJECT.select_records(connection, sql_command)

        if not isinstance(category_df, pd.DataFrame):
            #? Function failed to select
            
            logging.error(f"MenuClass : add_category : function failed : Got Nonetype from Category Name selection query")
            connection.close()
            return 3, None
            
        elif len(category_df) == 0:
            #? No category with the same name
                
            #? Building data for insertion
            data = [(admin_id,category_name,category_desc,image_path)]
            table_name,cols = self.get_category_tbl_params()
            
            #? Inserting data
            status,index = DB_OBJECT.insert_records(connection, table_name, data, cols, index= 'category_id',Flag=1)

        else:
            logging.error(f"MenuClass : add_category : function failed : More than one categories with the same name exists")
            connection.close()
            return 2, None

        connection.close()
        logging.info("MenuClass : add_category : execution stop")

        return status,index
    
    def get_category_details(self,admin_id):
        '''
            Get all the categories for given admin.
            
            Args:
            -----
            admin_id (`String | Int`): Id of the admin.
            
            Returns:
            -------
            status (`Integer`): Status of the retrival
                - 0 : Successful
                - 1 : Unsuccessful
            data (`Array of Dictionary`): Category Data
        '''
        try:
            logging.info("MenuClass : get_category_details : execution start")
            
            #? Getting Database Connection
            connection,_ = self.get_db_connection()
            
            #? Getting Data from the database
            sql_command = f"select * from feasta.category c where c.admin_id = '{admin_id}'"
            category_df = DB_OBJECT.select_records(connection, sql_command)
            connection.close()
            
            if not isinstance(category_df, pd.DataFrame):
                logging.error("MenuClass : get_category_details : Failed to fetch the Dataframe")
                return 1,None
            
            else:
                logging.info(f"MenuClass : get_category_details : execution stop : categories => {str(category_df)}")
                data = []
                for i,dta in category_df.iterrows():
                    dic = {}
                    dic['category_id'] = dta['category_id']
                    dic['category_name'] = dta['category_name']
                    data.append(dic)

                return 0,data
        
        except Exception as e:
            logging.error(f"MenuClass : get_category_details : Function Failed : error => {str(e)}")
            return 1,None
        
    def add_item(self, admin_id, item_name, item_desc, category_id, price, image_path):
        '''
            To add Item to the database.
            
            Args:
            ----
            item_name (`String`): Name of the item.
            item_desc (`String`): Description of the item.
            category_id (`String | Int`): Id of the category
            price (`String | Int`): Price of the product.
            image_path (`String`): Path where the image is stored.
            
            Returns:
            -------
            status (`Integer`): Status of the insertion.
            item_id (`Integer`): Index of the entry in the category table.
        '''

        try:
            logging.info("MenuClass : add_item : execution start")

            #? Getting Database Connection
            connection,_ = self.get_db_connection()
                
            #? Checking if Some item exists with the name for same admin
            sql_command = f"select count(*) from feasta.menu m,feasta.category c where c.admin_id = '{str(admin_id)}' and m.category_id = c.category_id and m.item_name = '{item_name}'"
            item_name_df = DB_OBJECT.select_records(connection, sql_command)

            if not isinstance(item_name_df, pd.DataFrame):
                #? Function failed to select
                
                logging.error(f"MenuClass : add_item : function failed : Got Nonetype from Category Name selection query")
                connection.close()
                return 3, None
                
            elif int(item_name_df['count'][0]) == 0:
                #? No item with the same name
                    
                #? Building data for insertion
                data = [(item_name,item_desc,category_id,price,image_path)]
                table_name = "feasta.menu"
                cols = "item_name,item_desc,category_id,price,image_path"
                
                #? Inserting data
                status,index = DB_OBJECT.insert_records(connection, table_name, data, cols, index= 'item_id',Flag=1)
                connection.close()
                
            else:
                logging.error(f"MenuClass : add_item : function failed : More than one items with the same name exists")
                connection.close()
                return 2, None

            logging.info("MenuClass : add_item : execution stop")

            return  status,index
        
        except Exception as e:
            logging.error(f"MenuClass : add_item : execution failed : Error : {str(e)}")
            connection.close()
            return 3, None
        
    def get_item_details(self,admin_id, item_id = -1, size = -1):
        '''
            Get all the items for given admin.
            
            Args:
            -----
            admin_id (`String | Int`): Id of the admin.
            item_id (`String | Int`): Id of the item.
            
            Returns:
            -------
            status (`Integer`): Status of the retrival
                - 0 : Successful
                - 1 : Unsuccessful
            data (`Array of Dictionary`): Item Data
        '''
        try:
            logging.info("MenuClass : get_item_details : execution start")
            
            #? Getting Database Connection
            connection,_ = self.get_db_connection()
            
            #? Getting Data from the database
            sql_command = f"""
            select m.item_id,m.item_name,m.item_desc,c.category_name,m.price,m.image_path 
            from feasta.menu m,feasta.category c 
            where c.admin_id = '{admin_id}' 
            and m.category_id = c.category_id 
            order by m.item_name asc ;
            """
            logging.info(f"Get Item Sql Command -> {sql_command}")
            item_df = DB_OBJECT.select_records(connection, sql_command)
            connection.close()
            
            if not isinstance(item_df, pd.DataFrame):
                logging.error("MenuClass : get_item_details : Failed to fetch the Dataframe")
                return 1,None
            
            else:
                logging.info(f"MenuClass : get_item_details : execution stop")
                data = item_df.to_json(orient = 'records')
                
                return 0,data
        
        except Exception as e:
            logging.error(f"MenuClass : get_item_details : Function Failed : error => {str(e)}")
            return 1,None
        
    