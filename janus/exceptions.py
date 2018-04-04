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
exceptions

contains all decorators of janus. See more in janus.py
spec: http://jsonapi.org/

"""

import hashlib
import time

class JanusException(Exception):
    """
    contains additional information to exceptions to return as much information as possible
    using an ErrorMessage object as specified in jsonapi.
    """

    id = None #a unique identifier for this particular occurrence of the problem.

    #the HTTP status code applicable to this problem, expressed as a string value.
    #if we get no specificerror code (derived Exceptions will set their own) we use 503 (internal server error).
    status = 503

    #an application-specific error code, expressed as a string value. (will be set by derived exceptions or by the one raising the exception)
    code = -1

    #get's set while raising the exception. a short, human-readable summary of the problem that SHOULD NOT change from occurrence to occurrence of the problem, except for purposes of localization.
    title = ""

    #get's set while raising the exception. a human-readable explanation specific to this occurrence of the problem.
    detail = None

    #get's set while raising the exception. a meta object containing non-standard meta-information about the error.
    #this has to be none or a dict of primitive types.
    #TODO verify that
    meta = None

    def __init__(self,title="",detail="",status="",code=-1,meta=None):
        Exception.__init__(self,self.title)

        self.title = title
        self.detail = detail
        self.status = status
        self.code = code
        self.meta = meta

        #we use a string representation of all we got in details plus timestamp as hash to identify this error.
        #So we can search for it in the logs, if we need to.
        self.id = hashlib.sha1(
                                str(time.time()) +
                                str(self.title) +
                                str(self.detail) +
                                str(self.status) +
                                str(self.code) +
                                str(self.meta)
                              ).hexdigest()

class BadRequestException(JanusException):
    """
    represents a Bad Request exception (HTTP 400)
    """
    def __init__(self, detail=None, code=-1, meta = None):
        JanusException. __init__(self,
            title="The web server was unable to understand the request and process it.",
            detail=detail,
            status=400,
            code=code,
            meta=meta)

class UnauthorizedException(JanusException):
    """
    represents a Unauthorized exception (HTTP 401)
    """
    def  __init__(self, detail=None, code=-1, meta = None):
        #just call super with some prefilled information fitting this special type of exception
        JanusException. __init__(self,
            title="The request can not be process, because authorization is missing.",
            detail=detail,
            status=401,
            code=code,
            meta=meta)

class ForbiddenException(JanusException):
    """
    represents a Forbidden exception (HTTP 403)
    """
    def  __init__(self, detail=None, code=-1, meta = None):
        #just call super with some prefilled information fitting this special type of exception
        JanusException. __init__(self,
            title="You are not allowed to access this resource.",
            detail=detail,
            status=403,
            code=code,
            meta=meta)

class NotFoundException(JanusException):
    """
    represents a not found exception (HTTP 404)
    """
    def  __init__(self, detail=None, code=-1, meta = None):
        #just call super with some prefilled information fitting this special type of exception
        JanusException. __init__(self,
            title="The requested resource could not be found but may be available again in the future. Subsequent requests by the client are permissible.",
            detail=detail,
            status=404,
            code=code,
            meta=meta)

class DeveloperException(JanusException):
    """
    represents an Exception caused by Developer Error
    """
    def  __init__(self, title="Developer Error", detail=None, code=-1, meta = None, status = 500):
        #just call super with some prefilled information fitting this special type of exception
        JanusException. __init__(self,
            title=title,
            detail=detail,
            status=500,
            code=code,
            meta=meta)

class InternalServerErrorException(JanusException):
    """
    represents a Internal Server Error exception (HTTP 500)
    """
    def  __init__(self, detail=None, meta = None):
        #just call super with some prefilled information fitting this special type of exception
        JanusException. __init__(self,
            title="Internal Server Error",
            detail=detail,
            status=500,
            code="42", #this is always error 42, because this should never happen on production.
            meta=meta)
