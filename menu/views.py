#* Importing Libraries
import json
import logging
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response

#* Relative Imports
# from .utils import authentication as auth

#* Initializing Logs
from common.utils.logging.logger import LogClass
logger = LogClass().get_logger('menu_views')

#* Defining Class Objects
# AUTH_OBJECT = auth.AuthenticationClass()
