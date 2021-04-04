
#? Python library imports
import psycopg2
import psycopg2.extras as extras
import pandas as pd 
import numpy as np
import json
import logging
import traceback
from sqlalchemy import create_engine

#? Class Imports
from ..logging.logger import LogClass

#? Relative Imports
from ..Exceptions.common_exceptions.common_exception import *

#? Credential Import
# from .db_credentials import *
from .heroku_db_creds import *

#? Initializing logger
logger = LogClass().get_logger('database')

class DBClass:
    '''
        For Database Related Functionalities.
            - Selection
            - Insertion
            - Updation
            - Deletion
            - Table Creation
            - Schema Creation
    '''

    def read_data(self,file_path):
        """This function is used read data from server file and load into dataframe.

        Args:
            file_path ([string]): [relative path of the file of server.]

        Returns:
            [dataframe]: [it will return read csv file data in the form of dataframe.]
        """

        read_df=pd.read_csv(file_path) #  Read csv file and load data into dataframe.
        
        column_name_list = read_df.columns.values.tolist()
    
        column_list = []
        for name in column_name_list:
            if read_df.dtypes.to_dict()[name] == 'object':
                column_list.append(name)
        read_df=pd.read_csv(file_path,parse_dates=column_list) #  Read csv file and load data into dataframe.
        return read_df
    
    def database_connection(self):
        """This function is used to make connection with database.

        Args:
            database ([string]): [name of the database.],
            user ([string]): [user of the database.],
            password ([string]): [password of the database.],
            host ([string]): [host ip or name where database is running.],
            port ([string]): [port number in which database is running.]

        Returns:
            [object,string]: [it will return connection object well as connection string.]
        """
        try:
            connection_string = "postgresql://" + user + ":" + password + "@" + host + ":" + port + "/" + database # Make database connection string.
            connection = psycopg2.connect(database = database, user = user , password = password, host = host, port = port) #Get connection object by initializing connection to database. 
        except:
            return None,None
            
        return connection,connection_string
    
    def close_connection(self, connection):
        '''
            Used to Close the connection after its use is done.
            
            Args:
            ----
            connection (`Object`): Postgres Connection Object.
            
            Returns:
            -------
            None
        '''
        connection.close()
        return

    def create_sequence(self,connection):
        '''
            Used to auto generate indexes.
        '''
        
        cursor = connection.cursor()
        try:
            sql_command = 'CREATE SEQUENCE dataset_sequence INCREMENT 1 START 1;'
            cursor.execute(sql_command)
            connection.commit()
            cursor.close()
            return 0
        except (Exception,psycopg2.DatabaseError) as error:
            connection.rollback() # Rollback the changes.
            cursor.close() # Close the cursor
            return 1 # If failed.

    def get_sequence(self,connection):
        sql_command = "select nextval('dataset_sequence')"
        data = self.select_records(connection, sql_command)
        return data

    def is_exist_sequence(self,connection,seq_name):
        '''
            Checking if the sequence with the same name exists.
        '''
        sql_command = "SELECT * FROM information_schema.sequences where sequence_name ='"+ seq_name +"'"
        data=self.select_records(connection,sql_command) #call select_records which return data if found else None
        if len(data) == 0: # check whether length of data is empty or not
            data = self.create_sequence(connection)
            if data == 0:
                return "True"
            else :
                return "False"
        else:
            return "True"

    #v1.3
    def create_schema(self,connection,user_name = None):
        """This function is used to create schema.

        Args:
            connection ([object]): [connection for database],
            user_name ([string]): [user name]

        Returns:
            [integer]: [status of create schema. if successfully then 0 else 1.]
        """
        if user_name == None :
            schema_name = "Feasta"
        else:
            schema_name = user_name.lower() # Get schema name.
            
        cursor = connection.cursor() # Open cursor for database.
        try:
            cursor.execute('CREATE Schema '+ schema_name +';') # Excute create schema query.
            connection.commit() # Commit the changes.
            return 0 # If successfully created.
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback() # Rollback the changes.
            cursor.close() # Close the cursor
            return 1 # If failed.
        
    def create_table(self,connection,table_name,schema):
        """This function is used to  create table into database.

        Args:
            connection ([object]): [object of the connection to the database.],
            table_name ([string]): [name of the table.],
            schema ([string]): [structure of the table.]

        Returns:
            [integer]: [it will return status of the table creation. if successfully the 0 else 1.]
        """
        cursor = connection.cursor() # Open cursor for database.
        try:
            cursor.execute('CREATE TABLE '+table_name+' ('+schema+');') # Excute create table query.
            connection.commit() # Commit the changes.
            return 0 # If successfully created.
        except (Exception, psycopg2.DatabaseError) as error:
            logging.info(str(error))
            connection.rollback() # Rollback the changes.
            cursor.close() # Close the cursor
            return 1 # If failed.
        
    def insert_records(self,connection,table_name,row_tuples,cols,index ='index',Flag=0):
        """This function is used to insert data into database table.

        Args:
            connection ([object]): [object of the database connection.],
            table_name ([string]): [name of the table.],
            row_tuples ([list]): [list of the tuple of record.],
            cols ([string]): [column names in the form of strings.]

        Returns:
            [integer]: [it will return status of the data insertion. if successfully then 0 else 1.]
        """
        


        cols = cols # Get columns name for database insert query.
        tuples = row_tuples # Get record for database insert query.


        cursor = connection.cursor() # Open cursor for database.
        try:
            if Flag == 0 :
                query = "INSERT INTO %s(%s) VALUES %%s " % (table_name, cols) # Make query
                extras.execute_values(cursor, query, tuples) # Excute insert query.
                index = 0
            else:
                query = "INSERT INTO %s(%s) VALUES %%s RETURNING %s" % (table_name, cols, index) # Make query
                extras.execute_values(cursor, query, tuples) # Excute insert query.
                index = [row[0] for row in cursor.fetchall()][0]
            
            status = 0
            connection.commit() # Commit the changes.
            cursor.close()
            return status,index # If successfully inserted.
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback() # Rollback the changes.
            cursor.close() # Close the cursor.
            logging.error(str(error))
            return 1,None # If failed.

    def select_records(self,connection,sql_command):
        """This function is used to retrieve data from database table into dataframe.

        Args:
            connection ([object]): [object of the database connection.],
            sql_command ([string]): [select sql command.]

        Returns:
            [dataframe]: [it will return dataframe of the selected data from the database table.]
        """
        sql_command = str(sql_command).replace('%',"%%") # Get sql command.
        try :
        
            connection_string = "postgresql://" + user + ":" + password + "@" + host + ":" + port + "/" + database # Make database connection string.
            engine = create_engine(connection_string) # Create database engine.
            data = pd.read_sql_query(sql_command, engine) #method of sqlalchemy
    
            return data   
        except(Exception, psycopg2.DatabaseError) as error:
            logging.info(str(error) + "check")
            return None
        
       

    def delete_records(self,connection,sql_command):
        """This function is used to delete data from database table.

        Args:
            connection ([object]): [connection object of the database class.],
            sql_command ([string]): [delete sql command]

        Returns:
            [integer]: [it will return stauts of deleted record. if successfully then 0 else 1.]
        """
        
        cursor = connection.cursor() # Open the cursor.
        sql_command = sql_command # Get delete query
        try:
            cursor.execute(sql_command) # Execute the delete query.
            connection.commit() # Commit the changes.
            status = 0 # If Successfully.
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback() # Rollback the changes.
            cursor.close() # Close the cursor.
            status = 1 # If failed
            logger.info(str(error) + " Error in delete record function")
        return status

    def update_records(self,connection,sql_command):
        """This function is used to update records into database.

        Args:
            connection ([object]): [connection for database],
            sql_command ([string]): [query string for update command]

        Returns:
            [integer]: [status of updated records. if successfully then 1 else 0.]
        """
        
        cursor = connection.cursor() # Open the cursor.
        sql_command = sql_command # Get update query
        try:
            cursor.execute(sql_command) # Execute the update query.
            connection.commit() # Commit the changes.
            cursor.close() # Close the cursor.
            status = 0 # If Successfully.
            
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback() # Rollback the changes.
            cursor.close() # Close the cursor.
            status = 1 # If failed
            
            logging.error(str(error))
        return status

    def load_df_into_db(self,connection_string,table_name,file_data_df,user_name):
        """This function is used to load csv data  into database table.

        Args:
            connection_string ([object]): [connection string of the database connection.],
            table_name ([string]): [name of the table.],
            file_data_df ([dataframe]): [dataframe of the file data.],
            user_name ([string]): [name of the user.]

        Returns:
            [integer]: [it will return status of loaded data into database table. if successfully then 0 else 1.]
        """
    
        engine = create_engine(connection_string) # Create database engine.
        schema_name = user_name.lower()
        try :
            
            file_data_df.to_sql(table_name,engine,schema=schema_name,) # Load data into database with table structure.
            
            status = 0 # If successfully.
        except Exception as e:
            logging.error("Exception: "+str(e))
            status = 1 # If failed.
            
        return status

    def is_existing_table(self,connection,table_name,schema):
        """ function used to check the table is Exists or Not in database

        Args:
                table_name[(String)] : [Name of the table]
                schema[String] : [Name of the Schema]
        Return : 
            [String] : [return the True if record found else False]
        """
        sql_command = "SELECT 1 FROM information_schema.tables WHERE table_schema ='"+schema+"' AND table_name = '"+table_name+"'"
        data=self.select_records(connection,sql_command) #call select_records which return data if found else None
        print(str(data) + "checking")
        if len(data) == 0: # check whether length of data is empty or not
            self.create_schema(connection)
            return "False"
        else:
            return "True"
    
    def user_authentication(self,connection,user_name,password):
        """[summary]

        Args:
            connection ([String]): [connection String]
            user_name ([String]): [User Name]
            password ([String]): [password]

        Raises:
            UserAuthenticationFailed: [User authentication failed]
        Returns:
            [String]: [if user authenticated then it return True]
        """
        try:
            sql_command = "SELECT user_name from feasta.user_auth_tbl where user_name='"+ str(user_name) +"' and password='"+ str(password) +"'"
            user_df = self.select_records(connection,sql_command)
            if user_df is None:
                raise UserAuthenticationFailed(500)          
            if len(user_df) > 0 :
                return True
            else:
                raise UserAuthenticationFailed(500)
        except UserAuthenticationFailed as exc:
            return exc.msg
  
    