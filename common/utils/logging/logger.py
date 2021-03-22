import logging
import traceback

class LogClass:
    
    def __init__(self,user_name,log_enable):
        self.user_name = user_name
        self.log_enable = log_enable
        
    def log_setting(self):
        if self.user_name == 'admin' and self.log_enable ==True :
            logging.basicConfig(level=logging.DEBUG, filename= 'logs/' + self.user_name + '_debug.log', format='%(asctime)s %(module)s %(levelname)s:%(message)s')
      
            