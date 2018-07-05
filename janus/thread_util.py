"""
Copyright (c) 2018, xamoom GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""
threading

contains helpers to map object to messages in threads

"""

from threading import Thread


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,**self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return


def mapper_task(msg_class, o, include_relationships, do_nesting):
    msg = msg_class()
    msg.map_object(o, include_relationships, do_nesting=do_nesting)
    return msg

import time,random


def do_something(i):
    time.sleep(random.randint(1,8))
    print("Done {}".format(i))
    return i


ts = []
for i in range(10):
    ts.append(ThreadWithReturnValue(target=do_something, args=(i,)))

for t in ts:
    t.start()

r = []
for t in ts:
    r.append(t.join())

for x in r:
    print(x)