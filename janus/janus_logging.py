"""
Copyright (c) 2018, xamoom GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging

class janus_logger(object):

    __prefix = "JANUS: "
    enabled = True

    @classmethod
    def enable(cls):
        cls.enabled = True

    @classmethod
    def disable(cls):
        cls.enabled = False

    @classmethod
    def debug(cls, message):
        if cls.enabled: logging.debug(cls.__prefix + message)

    @classmethod
    def info(cls, message):
        if cls.enabled: logging.info(cls.__prefix + message)

    @classmethod
    def warning(cls, message):
        if cls.enabled: logging.warning(cls.__prefix + message)

    @classmethod
    def error(cls, message):
        if cls.enabled: logging.error(cls.__prefix + message)

    @classmethod
    def critical(cls, message):
        if cls.enabled: logging.critical(cls.__prefix + message)
