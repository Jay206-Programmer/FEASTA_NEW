
#* Importing Libraries
import json
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

#* Relative Imports
from .utils import authentication as auth

#* Initializing Logs
from common.utils.logging.logger import *
logger = LogClass().get_logger('auth_views')

#* Defining Class Objects
AUTH_OBJECT = auth.AuthenticationClass()

class UserLoginClass(APIView):
        
        def post(self,request,format=None):
                
                try:
                    logging.info("UserLoginClass : Execution Start")
                    
                    #? Converting Json request from frontend into python dictionary
                    request_data = json.loads(request.body)
                    
                    #? Fatching parameters
                    email = request_data['email_id']
                    password = request_data['password']
                    
                    status,user_dict = AUTH_OBJECT.login_user(email,password)
                    
                    if status == 0:
                        #? User Regestration Successful
                        
                        logging.info("UserLoginClass : Execution End : Regestration Successful")
                        return Response({"status_code":200,"response_msg":"Login Successful","user_id":f"{user_dict['user_id']}","user_name":f"{user_dict['first_name']}"})
                    elif status == 1:
                        #? Wrong Password
                        
                        logging.info("UserLoginClass : Execution End : Incorrect Password")
                        return Response({"status_code":500,"response_msg":"Incorrect Email or Password"})
                    elif status == 2:
                        #? Login Status Update Failed                        
                        
                        logging.info("UserLoginClass : Execution End : Login Status Update Failed")
                        return Response({"status_code":500,"response_msg":"Login Status Update Failed"})
                    elif status == 4:
                        #? Email is not verified 

                        logging.info("UserLoginClass : Execution End : Email is not verified")
                        return Response({"status_code":500,"response_msg":"Please verify the email first!"})
                    elif status == 5:
                        #? Regestration remaining 

                        logging.info("AdminLoginClass : Execution End : User is not registered")
                        return Response({"status_code":500,"response_msg":"You are not registered yet, please register first!"})
                    else:
                        #? Unknown Error Occurred
                        
                        logging.info("UserLoginClass : Execution End : Unknown Error")
                        return Response({"status_code":500,"response_msg":"Unknown Error occurred while logging in"})
                        
                except Exception as e:
                    logging.error(f"UserLoginClass : Execution Failed : Error : {str(e)}")
                    return Response({"status_code":500,"error_msg":str(e)})
        
class UserRegestrationClass(APIView):
        
        def post(self,request,format=None):
                
                try:
                    logging.info("UserRegestrationClass : Execution Start")
                    
                    #? Converting Json request from frontend into python dictionary
                    request_data = json.loads(request.body)
                    
                    #? Fatching parameters
                    first_name = request_data['first_name']
                    last_name = request_data['last_name']
                    email = request_data['email_id']
                    password = request_data['password']
                    phone_number = request_data['phone_number']
                    
                    status = AUTH_OBJECT.register_user(first_name,last_name, \
                                                        password, email, \
                                                        phone_number )
                    
                    if status == 0:
                        #? User Regestration Successful
                        
                        logging.info("UserRegestrationClass : Execution End : Regestration Successful")
                        return Response({"status_code":200,"response_msg":"Regestration Successful"})
                    elif status == 1:
                        #? Table Insertion Failed
                        
                        logging.info("UserRegestrationClass : Execution End : Table Insertion Failed")
                        return Response({"status_code":500,"response_msg":"Table Insertion Failed"})
                    elif status == 2:
                        #? Multiple Users with same email id
                        
                        logging.info("UserRegestrationClass : Execution End : Multiple users with same email id")
                        return Response({"status_code":500,"response_msg":"Multiple users with same email id"})
                    elif status == 4:
                        #? Failed to get User Details
                        
                        logging.info("UserRegestrationClass : Execution End : Failed to get User Details")
                        return Response({"status_code":500,"response_msg":"Failed to get User Details"})
                    else:
                        #? Unknown Error
                        
                        logging.info("UserRegestrationClass : Execution End : Unknown Error")
                        return Response({"status_code":500,"response_msg":"Unknown Error"})
                    
                    
                except Exception as e:
                    logging.error(f"UserRegestrationClass : Execution Failed : Error : {str(e)}")
                    return Response({"status_code":500,"error_msg":str(e)})
        
def verify_user(request, unique_id):
    message = AUTH_OBJECT.verify_uniqueid(unique_id)
    return HttpResponse(message, content_type='text/html')

def verify_admin(request, unique_id):
    message = AUTH_OBJECT.verify_uniqueid(unique_id,flag = 1)
    return HttpResponse(message, content_type='text/html')

class LoginStatusClass(APIView):
        
        def post(self,request,format=None):
                
                try:
                    logging.info("LoginStatusClass : Execution Start")
                    
                    #? Converting Json request from frontend into python dictionary
                    request_data = json.loads(request.body)
                    
                    #? Fatching parameters
                    user_id = request_data['user_id']
                    
                    status = AUTH_OBJECT.get_user_login_status(user_id)
                    
                    if status == -1:
                        #? Can't find the user_id

                        logging.info("LoginStatusClass : Execution End : Can't Find User")
                        return Response({"status_code":200,"response_msg":"Can't Find the User","status":f"{status}"})
                    elif status == -2:
                        #? Failed to fetch
                        
                        logging.info("LoginStatusClass : Execution End : Failed to get data from the database")
                        return Response({"status_code":500,"response_msg":"Failed to get data from the database","status":f"{status}"})
                    else:
                        #? Successfully Fetched
                        
                        logging.info("LoginStatusClass : Execution End : Login Status Fetch Successful")
                        return Response({"status_code":200,"response_msg":"Fetch Successful","status": f"{status}"})
                        
                except Exception as e:
                    logging.error(f"LoginStatusClass : Execution Failed : Error : {str(e)}")
                    return Response({"status_code":500,"error_msg":str(e)})

class AdminRegestrationClass(APIView):
        
        def post(self,request,format=None):
                
                try:
                    logging.info("AdminRegestrationClass : Execution Start")
                    
                    #? Converting Json request from frontend into python dictionary
                    request_data = json.loads(request.body)
                    
                    #? Fatching parameters
                    canteen_name = request.data['canteen_name']
                    first_name = request_data['first_name']
                    last_name = request_data['last_name']
                    email = request_data['email_id']
                    password = request_data['password']
                    phone_number = request_data['phone_number']
                    
                    status = AUTH_OBJECT.register_admin(first_name,last_name, \
                                                        password, email, \
                                                        phone_number, canteen_name)
                    
                    if status == 0:
                        #? Admin Regestration Successful
                        
                        logging.info("AdminRegestrationClass : Execution End : Regestration Successful")
                        return Response({"status_code":200,"response_msg":"Regestration Successful"})
                    elif status == 1:
                        #? Table Insertion Failed
                        
                        logging.info("AdminRegestrationClass : Execution End : Table Insertion Failed")
                        return Response({"status_code":500,"response_msg":"Table Insertion Failed"})
                    elif status == 2:
                        #? Multiple Users with same email id
                        
                        logging.info("AdminRegestrationClass : Execution End : Multiple users with same email id")
                        return Response({"status_code":500,"response_msg":"Multiple users with same email id"})
                    elif status == 4:
                        #? Failed to get User Details
                        
                        logging.info("AdminRegestrationClass : Execution End : Failed to get User Details")
                        return Response({"status_code":500,"response_msg":"Failed to get User Details"})
                    else:
                        #? Unknown Error
                        
                        logging.info("AdminRegestrationClass : Execution End : Unknown Error")
                        return Response({"status_code":500,"response_msg":"Unknown Error"})
                    
                    
                except Exception as e:
                    logging.error(f"AdminRegestrationClass : Execution Failed : Error : {str(e)}")
                    return Response({"status_code":500,"error_msg":str(e)})

class AdminLoginClass(APIView):
        
        def post(self,request,format=None):
                
                try:
                    logging.info("AdminLoginClass : Execution Start")
                    
                    #? Converting Json request from frontend into python dictionary
                    request_data = json.loads(request.body)
                    
                    #? Fatching parameters
                    email = request_data['email_id']
                    password = request_data['password']
                    
                    status,admin_dict = AUTH_OBJECT.login_admin(email,password)
                    
                    if status == 0:
                        #? User Regestration Successful
                        
                        logging.info("AdminLoginClass : Execution End : Regestration Successful")
                        return Response({"status_code":200,"response_msg":"Login Successful","admin_id":f"{admin_dict['admin_id']}","user_name":f"{admin_dict['first_name']}"})
                    elif status == 1:
                        #? Wrong Password
                        
                        logging.info("AdminLoginClass : Execution End : Incorrect Password")
                        return Response({"status_code":500,"response_msg":"Incorrect Email or Password"})
                    elif status == 2:
                        #? Login Status Update Failed                        
                        
                        logging.info("AdminLoginClass : Execution End : Login Status Update Failed")
                        return Response({"status_code":500,"response_msg":"Login Status Update Failed"})
                    elif status == 4:
                        #? Email is not verified 

                        logging.info("AdminLoginClass : Execution End : Email is not verified")
                        return Response({"status_code":500,"response_msg":"Please verify the email first!"})
                    elif status == 5:
                        #? Regestration remaining 

                        logging.info("AdminLoginClass : Execution End : Admin is not registered")
                        return Response({"status_code":500,"response_msg":"You are not registered yet, please register first!"})
                    else:
                        #? Unknown Error Occurred
                        
                        logging.info("AdminLoginClass : Execution End : Unknown Error")
                        return Response({"status_code":500,"response_msg":"Unknown Error occurred while logging in"})
                        
                except Exception as e:
                    logging.error(f"AdminLoginClass : Execution Failed : Error : {str(e)}")
                    return Response({"status_code":500,"error_msg":str(e)})
        
