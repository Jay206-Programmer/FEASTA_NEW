
#* Importing Libraries
import json
import logging
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response

#* Relative Imports
from .utils import authentication as auth

#* Initializing Logs
from common.utils.logging.logger import LogClass

user_name = 'admin'
log_enable = True
LogObject = LogClass(user_name,log_enable)
LogObject.log_setting()
logger = logging.getLogger('auth_views')

#* Defining Class Objects
AUTH_OBJECT = auth.AuthenticationClass()

class UserLoginClass(APIView):
        
        def get(self,request,format=None):
                
                try:
                    logging.info("Authentication : UserLoginClass : Execution Start")
                    logging.info("Authentication : UserLoginClass : Execution End")
                    return Response({"status_code":200,"response_msg":"LOGIN PAGE WORKING"})
                        
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
                    else:
                        #? User Regestration Failed
                        
                        logging.info("Authentication : UserRegestrationClass : Execution End : Regestration Unsuccessful")
                        return Response({"status_code":500,"response_msg":"Regestration Failed"})
                    
                    
                except Exception as e:
                    logging.error(f"Authentication : UserRegestrationClass : Execution Failed : Error : {str(e)}")
                    return Response({"status_code":500,"error_msg":str(e)})
        
