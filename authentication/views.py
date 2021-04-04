
#* Importing Libraries
import json
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response

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
                    logging.info("Authentication : UserLoginClass : Execution Start")
                    
                    #? Converting Json request from frontend into python dictionary
                    request_data = json.loads(request.body)
                    
                    #? Fatching parameters
                    email = request_data['email_id']
                    password = request_data['password']
                    
                    status = AUTH_OBJECT.login_user(email,password)
                    
                    if status == 0:
                        #? User Regestration Successful
                        
                        logging.info("Authentication : UserLoginClass : Execution End : Regestration Successful")
                        return Response({"status_code":200,"response_msg":"Login Successful"})
                    elif status == 1:
                        #? Wrong Password
                        
                        logging.info("Authentication : UserLoginClass : Execution End : Incorrect Password")
                        return Response({"status_code":500,"response_msg":"Incorrect Password"})
                    else:
                        #? Unknown Error Occurred
                        
                        logging.info("Authentication : UserLoginClass : Execution End : Unknown Error")
                        return Response({"status_code":500,"response_msg":"Unknown Error occurred while logging in"})
                        
                except Exception as e:
                    logging.error(f"Authentication : UserLoginClass : Execution Failed : Error : {str(e)}")
                    return Response({"status_code":500,"error_msg":str(e)})
        
class UserRegestrationClass(APIView):
        
        def post(self,request,format=None):
                
                try:
                    logging.info("Authentication : UserRegestrationClass : Execution Start")
                    
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
                        
                        logging.info("Authentication : UserRegestrationClass : Execution End : Regestration Successful")
                        return Response({"status_code":200,"response_msg":"Regestration Successful"})
                    elif status == 1:
                        #? Table Insertion Failed
                        
                        logging.info("Authentication : UserRegestrationClass : Execution End : Table Insertion Failed")
                        return Response({"status_code":500,"response_msg":"Table Insertion Failed"})
                    elif status == 2:
                        #? Multiple Users with same email id
                        
                        logging.info("Authentication : UserRegestrationClass : Execution End : Multiple users with same email id")
                        return Response({"status_code":500,"response_msg":"Multiple users with same email id"})
                    elif status == 4:
                        #? Failed to get User Details
                        
                        logging.info("Authentication : UserRegestrationClass : Execution End : Failed to get User Details")
                        return Response({"status_code":500,"response_msg":"Failed to get User Details"})
                    else:
                        #? Unknown Error
                        
                        logging.info("Authentication : UserRegestrationClass : Execution End : Unknown Error")
                        return Response({"status_code":500,"response_msg":"Unknown Error"})
                    
                    
                except Exception as e:
                    logging.error(f"Authentication : UserRegestrationClass : Execution Failed : Error : {str(e)}")
                    return Response({"status_code":500,"error_msg":str(e)})
        
