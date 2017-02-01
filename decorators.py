__author__ = "Bruno Hautzenberger"
__copyright__ = "Copyright 2015, xamoom GmbH"
__maintainer__ = "Bruno Hautzenberger"
__email__ = "bruno@xamoom.com"
__status__ = "Development"

"""
Copyright (c) 2015, xamoom GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""
decorator

contains all decorators of janus. See more in janus.py
spec: http://jsonapi.org/

"""
import traceback

from janus_logging import janus_logger
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
                    cached_get_hook=None,
                    cached_set_hook=None,
                    include_relationships=False,
                    options_hook=None,
                    nest_in_responses=False,
                    logging=False):
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
        self.cached_get_hook = cached_get_hook
        self.cached_set_hook = cached_set_hook
        self.nest_in_responses = nest_in_responses
        
        if logging:
            janus_logger.enable()
        else:
            janus_logger.disable()

    def __call__(self, f):
        def wrapped_f(*a, **ka):
            try:
                #first check if this is not a HTTP OPTIONS call using a method defined based on the  WS framework.
                #if it is one return empty array and do nothing else.
                if self.options_hook != None:
                    if self.options_hook() == True:
                        janus_logger.debug("This was an OPTIONS request.")
                        return {}
                    
                response_obj = f(*a, **ka)
                
                #first check if there is an response object
                #if not nothing to return so HTTP 204
                #otherwise process response
                if response_obj == None:
                    if self.before_send_hook != None:
                        self.before_send_hook(204,None,None)
                    
                    janus_logger.debug("Decorated function returned None. Nothing to map.")
                    return None
                else:
                    #check response object
                    if isinstance(response_obj,JanusResponse) == False:
                        #janus_logger.error("Expected JanusResponse got " + str(type(response_obj)))
                        #raise Exception('Return value has to be instance of JanusResponse')
                        janus_logger.info("Not a JanusResponse. Will return this as it is. No mapping.")
                        return response_obj
                    
                    message = None
                    
                    #caching
                    loaded_from_cache = False
                    
                    if self.cached_get_hook != None:
                        cached_object = self.cached_get_hook(response_obj)
                        if cached_object != None:
                            loaded_from_cache = True                            
                            message = cached_object #returned cached, already mapped, response
                            
                            janus_logger.info("Will return cached message: " + str(loaded_from_cache))
                    
                    if loaded_from_cache == False: #nothing in cache or cache deactivated
                        self.message = response_obj.message #get the message type to return
                        obj = response_obj.data #get the data to return
                        
                        data = DataMessage.from_object(obj,self.message,do_nesting=self.nest_in_responses) #generate data message with data
                        
                        #take care of includes
                        if response_obj.include_relationships != None: self.include_relationships = response_obj.include_relationships
                        included = None                        
                        
                        janus_logger.info("Should map included: " + str(self.include_relationships))
                        if self.include_relationships:
                            included = self.__load_included(data)
                            
                        #is there custome meta?
                        if response_obj.meta != None:
                            if self.meta == None:
                                self.meta = response_obj.meta
                            else:
                                self.meta.update(response_obj.meta)
                        
                        message = JsonApiMessage(data=data,included=included,meta=self.meta,do_nesting=self.nest_in_responses).to_json() #render json response
        
                        #caching
                        if self.cached_set_hook != None and loaded_from_cache == False:
                            janus_logger.debug("Caching message")
                            self.cached_set_hook(response_obj,message)
    
                    if self.before_send_hook != None: #fire before send hook
                        self.before_send_hook(self.success_status,message,response_obj)
    
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

                janus_logger.error("Traceback: " + tb)

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
                        self.before_send_hook(204,None,None)
                        
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
                        self.before_send_hook(self.success_status,message,None)
    
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
        
        
    

    
