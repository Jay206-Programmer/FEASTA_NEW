import json
import logging
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response

class CommonClass(APIView):
        
        def get(self,request,format=None):
                """ this class used to check the authorized user login data.

                Args   :
                        user_name[(String)] : [Name of user]
                        password [(String)] : [password value]
                Return :
                        status_code(500 or 200),
                        error_msg(Error message for login successfull & unsuccessfull),
                        Response(return false if failed otherwise true)
                """
                try:
                    return Response({"status_code":200,"error_msg":"PAGE WORKING","response":"false"})
                        
                except Exception as e:
                    return Response({"status_code":"500","error_msg":str(e),"response":"false"})
        
