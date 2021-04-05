
#* Importing Libraries
import json
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

#* Relative Imports
from .utils import menu

#* Initializing Logs
from common.utils.logging.logger import *
logger = LogClass().get_logger('menu_views')

#* Defining Class Objects
MENU_OBJ = menu.MenuClass()

class AddCategoryClass(APIView):
    
    def post(self, request, format = None):
        
        try:
            logging.info("AddCategoryClass : Execution Start")
            
            #? Converting Json request from frontend into python dictionary
            request_data = json.loads(request.body)
            
            #? Fatching parameters
            admin_id = request_data['admin_id']
            category_name = request_data['category_name']
            category_desc = ''
            image_path = ''
            
            status, category_id = MENU_OBJ.add_category(admin_id, category_name, \
                                            category_desc, image_path \
                                            )
            
            if status == 0:
                #? Category Addition Successful
                
                logging.info("AddCategoryClass : Execution End : Category Addition Successful")
                return Response({"status_code":200,"response_msg":"Category Addition Successful", "category_id": f"{category_id}"})
            elif status == 1:
                #? Category Addition Unsuccessful
                
                logging.info("AddCategoryClass : Execution End : Category Addition Unsuccessful")
                return Response({"status_code":500,"response_msg":"Category Addition Unsuccessful"})
            elif status == 2:
                #? Multiple categories with same name
                
                logging.info("AddCategoryClass : Execution End : Multiple categories with same name")
                return Response({"status_code":500,"response_msg":"Multiple categories with same name, choose a different one."})
            else:
                #? Unknown Error
                
                logging.info("AddCategoryClass : Execution End : Unknown Error")
                return Response({"status_code":500,"response_msg":"Unknown Error Occurred, Please Retry!"})
            
        except Exception as e:
            logging.error(f"AddCategoryClass : Execution failed : Error => {str(e)}")
            return Response({"status_code":500,"response_msg":str(e)})

class GetCategoryDetailsClass(APIView):
    
    def post(self, request, format = None):
        
        try:
            logging.info("GetCategoryDetailsClass : Execution Start")
            
            #? Converting Json request from frontend into python dictionary
            request_data = json.loads(request.body)
            
            #? Fatching parameters
            admin_id = request_data['admin_id']
            
            status, data = MENU_OBJ.get_category_details(admin_id)
            
            if status == 0:
                #? Successful Retrival
                
                logging.info("GetCategoryDetailsClass : Execution End : Successful Retrival")
                return Response({"status_code":200,"response_msg":"Successful Retrival", "data": json.dumps(data)})
            elif status == 1:
                #? Retrival Unsuccessful
                
                logging.info("GetCategoryDetailsClass : Execution End : Retrival Unsuccessful")
                return Response({"status_code":500,"response_msg":"Retrival Unsuccessful"})
            
        except Exception as e:
            logging.error(f"GetCategoryDetailsClass : Execution failed : Error => {str(e)}")
            return Response({"status_code":500,"response_msg":str(e)})
        