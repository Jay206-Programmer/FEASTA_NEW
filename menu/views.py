
#* Importing Libraries
import json
import traceback
import uuid
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
    
    def get(self, request, format = None):
        
        try:
            logging.info("GetCategoryDetailsClass : Execution Start")
            
            #? Fatching parameters
            admin_id = request.query_params.get('admin_id')
            
            status, data = MENU_OBJ.get_category_details(admin_id)
            
            if status == 0:
                #? Successful Retrival
                
                logging.info("GetCategoryDetailsClass : Execution End : Successful Retrival")
                return Response({"status_code":200,"response_msg":"Successful Retrival", "data": data})
            elif status == 1:
                #? Retrival Unsuccessful
                
                logging.info("GetCategoryDetailsClass : Execution End : Retrival Unsuccessful")
                return Response({"status_code":500,"response_msg":"Retrival Unsuccessful"})
            
        except Exception as e:
            logging.error(f"GetCategoryDetailsClass : Execution failed : Error => {str(e)}")
            return Response({"status_code":500,"response_msg":str(e)})

class AddItemClass(APIView):
    
    def post(self, request, format = None):
        
        try:
            logging.info("AddItemClass : Execution Start")
            
            admin_id = request.POST.get('admin_id')
            item_name = request.POST.get('name')
            item_desc = request.POST.get('desc')
            category_id = request.POST.get('cate')
            quantity = request.POST.get('quant')
            price = request.POST.get('price')
            image_path = "/"
            
            image = request.FILES['image']
                
            
            status, category_id = MENU_OBJ.add_item(admin_id, item_name, \
                                            item_desc, category_id, \
                                            price, quantity, \
                                            image_path)
            
            if status == 0:
                #? Item Addition Successful
                
                logging.info("AddItemClass : Execution End : Item Addition Successful")
                return Response({"status_code":200,"response_msg":"Item Added Successfully", "item_id": f"{category_id}"})
            elif status == 1:
                #? Item Addition Unsuccessful
                
                logging.info("AddItemClass : Execution End : Item Addition Unsuccessful")
                return Response({"status_code":500,"response_msg":"Item Addition Unsuccessful, Please Retry!"})
            elif status == 2:
                #? Multiple Items with same name
                
                logging.info("AddItemClass : Execution End : Multiple items with same name")
                return Response({"status_code":500,"response_msg":"Multiple items with same name, choose a different name."})
            else:
                #? Unknown Error
                
                logging.info("AddItemClass : Execution End : Unknown Error")
                return Response({"status_code":500,"response_msg":"Unknown Error Occurred, Please Retry!"})
            
        except Exception as e:
            logging.error(f"AddItemClass : Execution failed : Error => {str(e)}")
            return Response({"status_code":500,"response_msg":str(e)})

    def put(self, request, format = None):
        
        try:
            logging.info("AddItemClass : Execution Start")
            
            admin_id = request.POST.get('admin_id')
            item_id = request.POST.get('item_id')
            item_name = request.POST.get('name')
            item_desc = request.POST.get('desc')
            category_id = request.POST.get('cate')
            quantity = request.POST.get('quant')
            price = request.POST.get('price')
            image_path = "/"
            
            status, item_id = MENU_OBJ.update_item(admin_id, item_id, \
                                            item_name, item_desc, \
                                            category_id, price, \
                                            quantity, image_path \
                                            )
            
            if status == 0:
                #? Item Updation Successful
                
                logging.info("AddItemClass : Execution End : Item Updation Successful")
                return Response({"status_code":200,"response_msg":"Item Updation Successful", "item_id": f"{item_id}"})
            elif status == 1:
                #? Item Updation Unsuccessful
                
                logging.info("AddItemClass : Execution End : Item Updation Unsuccessful")
                return Response({"status_code":500,"response_msg":"Item Updation Unsuccessful, Please Retry!"})
            elif status == 2:
                #? Multiple Items with same name
                
                logging.info("AddItemClass : Execution End : Multiple items with same name")
                return Response({"status_code":500,"response_msg":"There already exists an item with this name, choose a different one."})
            else:
                #? Unknown Error
                
                logging.info("AddItemClass : Execution End : Unknown Error")
                return Response({"status_code":500,"response_msg":"Unknown Error Occurred, Please Retry!"})
            
        except Exception as e:
            logging.error(f"AddItemClass : Execution failed : Error => {str(e)}")
            return Response({"status_code":500,"response_msg":str(e)})

class GetItemDetailsClass(APIView):
    
    def get(self, request, format = None):
        
        try:
            logging.info("GetItemDetailsClass : Execution Start")
            
            #? Fatching parameters
            admin_id = request.query_params.get('admin_id')
            try:
                item_id = request.query_params.get('item_id')
            except:
                item_id = None
            
            if item_id is None:
                status, data = MENU_OBJ.get_item_details(admin_id)
            else:
                status, data = MENU_OBJ.get_item_details(admin_id,item_id)
            
            if status == 0:
                #? Successful Retrival
                
                logging.info("GetItemDetailsClass : Execution End : Successful Retrival")
                return Response({"status_code":200,"response_msg":"Successful Retrival", "data": json.loads(data)})
            elif status == 1:
                #? Retrival Unsuccessful
                
                logging.info("GetItemDetailsClass : Execution End : Retrival Unsuccessful")
                return Response({"status_code":500,"response_msg":"Retrival Unsuccessful"})
            
        except Exception as e:
            logging.error(f"GetItemDetailsClass : Execution failed : Error => {str(e)}")
            return Response({"status_code":500,"response_msg":str(e)})
        
    def delete(self, request, format = None):
        
        try:
            logging.info("GetItemDetailsClass : Execution Start")
            
            #? Fatching parameters
            admin_id = request.query_params.get('admin_id')
            item_id = request.query_params.get('item_id')
            
            status, data = MENU_OBJ.delete_item(admin_id,item_id)
            
            if status == 0:
                #? Successful Deletion
                
                logging.info("GetItemDetailsClass : Execution End : Successful Deletion")
                return Response({"status_code":200,"response_msg":"Successfully Deleted the item", "data": json.loads(data)})
            elif status == 1:
                #? Retrival Unsuccessful
                
                logging.info("GetItemDetailsClass : Execution End : Deletion Unsuccessful")
                return Response({"status_code":500,"response_msg":"Deletion Unsuccessful"})
            
        except Exception as e:
            logging.error(f"GetItemDetailsClass : Execution failed : Error => {str(e)}")
            return Response({"status_code":500,"response_msg":str(e)})
        
