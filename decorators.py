__author__ = "Bruno Hautzenberger"
__copyright__ = "Copyright 2015, xamoom GmbH"
__maintainer__ = "Bruno Hautzenberger"
__email__ = "bruno@xamoom.com"
__status__ = "Development"

"""
decorator

contains all decorators of janus. See more in janus.py
spec: http://jsonapi.org/

"""
import traceback

from janus import DataMessage
from janus import JsonApiMessage
from janus import ErrorMessage
from janus import JanusResponse

class jsonapi(object):

    def __init__(   self,
                    meta=None,
                    links=None,
                    included=None,
                    success_status=200,
                    before_send_hook=None,
                    include_traceback_in_errors=False,
                    error_hook=None,
                    include_relationships=False,
                    options_hook=None):
        self.meta = meta
        self.links = links
        self.included = included
        self.message = None #gets set with the JanusResponse passed from calling function
        self.success_status = success_status
        self.before_send_hook = before_send_hook
        self.include_traceback_in_errors = include_traceback_in_errors
        self.error_hook = error_hook
        self.include_relationships = include_relationships
        self.options_hook = options_hook

    def __call__(self, f):
        def wrapped_f(*a, **ka):
            try:
                #first check if this is not a HTTP OPTIONS call using a method defined based on the  WS framework.
                #if it is one return empty array and do nothing else.
                if self.options_hook != None:
                    if self.options_hook() == True: return {}
                    
                response_obj = f(*a, **ka)
                
                #first check if there is an response object
                #if not nothing to return so HTTP 204
                #otherwise process response
                if response_obj == None:
                    if self.before_send_hook != None:
                        self.before_send_hook(204,None)
                        
                    return None
                else:
                    #check response object
                    if isinstance(response_obj,JanusResponse) == False:
                        raise Exception('Return value has to be instance of JanusResponse')
                    
                    self.message = response_obj.message #get the message type to return
                    obj = response_obj.data #get the data to return
                    
                    data = DataMessage.from_object(obj,self.message) #generate data message with data
                    
                    #take care of includes
                    included = None
                    if self.include_relationships:
                        included = self.__load_included(data)
                        
                    #is there custome meta?
                    if response_obj.meta != None:
                        if self.meta == None:
                            self.meta = response_obj.meta
                        else:
                            self.meta.update(response_obj.meta)
                    
                    message = JsonApiMessage(data=data,included=included,meta=self.meta).to_json() #render json response
    
                    if self.before_send_hook != None: #fire before send hook
                        self.before_send_hook(self.success_status,message)
    
                    return message
            except Exception as e:
                err_msg = ErrorMessage.from_exception(e)
                tb = traceback.format_exc()

                if self.include_traceback_in_errors:
                    if err_msg.meta == None: err_msg.meta = {}
                    err_msg.traceback = tb

                if self.error_hook != None:
                    self.error_hook(int(err_msg.status),err_msg,tb)

                message = JsonApiMessage(errors=err_msg,meta=self.meta).to_json()

                return message


        return wrapped_f
    
    def __load_included(self, data_message):
        included = []
        if isinstance(data_message,list):
            for d in data_message:
                included = included + d.get_included()
        else:
             included = data_message.get_included()
             
        #clean dublicates from included
        clean_included = []
        for item in included:
            if (item in clean_included) == False:
                clean_included.append(item)
                
        return clean_included
    
class describe(object):

    def __init__(   self,
                    success_status=200,
                    before_send_hook=None,
                    include_traceback_in_errors=False,
                    error_hook=None):
        self.success_status = success_status
        self.before_send_hook = before_send_hook
        self.include_traceback_in_errors = include_traceback_in_errors
        self.error_hook = error_hook

    def __call__(self, f):
        def wrapped_f(*a, **ka):
            try:
                #if this decorator is used the function must return all messages that should be described as a list
                messages = f(*a, **ka) 
                
                #first check if there is an response object
                #if not nothing to return so HTTP 204
                #otherwise process response
                if messages == None:
                    if self.before_send_hook != None:
                        self.before_send_hook(204,None)
                        
                    return None
                else:
                    if isinstance(messages, (list, tuple)) == False:
                        raise Exception('Methods using the "describe" decorator have to return a list of subclasses of DataMessage to describe.')
                        
                    msg_descriptions = []
                    for msg in messages:
                        if issubclass(msg,DataMessage) == False:
                            raise Exception('All returned classes in the returned list have to be a subclass of DataMessage.')
                        
                        msg_descriptions.append(msg().describe())
                    
                    meta = {'message-types':msg_descriptions}
                    
                    message = JsonApiMessage(meta=meta).to_json() #render json response
    
                    if self.before_send_hook != None: #fire before send hook
                        self.before_send_hook(self.success_status,message)
    
                    return message
            except Exception as e:
                err_msg = ErrorMessage.from_exception(e)
                tb = traceback.format_exc()

                if self.include_traceback_in_errors:
                    if err_msg.meta == None: err_msg.meta = {}
                    err_msg.traceback = tb

                if self.error_hook != None:
                    self.error_hook(int(err_msg.status),err_msg,tb)

                message = JsonApiMessage(errors=err_msg).to_json()

                return message


        return wrapped_f
   
    
