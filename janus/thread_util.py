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
from multiprocessing import Process, Manager

def mapper_task(result_list,pos,msg_class, o, include_relationships, do_nesting):
    msg = msg_class()
    msg.map_object(o, include_relationships, do_nesting=do_nesting)
    result_list[pos] = msg

""" TEST 
import time,random

def do_something(i,l):
    time.sleep(random.randint(1,8))
    print("Done {}".format(i))
    l[i] = "x"*i

manager = Manager()
l = manager.list(range(10))

ts = []
for i in range(10):
    ts.append(Process(target=do_something, args=(i, l)))

for t in ts:
    t.start()

for t in ts:
    t.join()

for x in l:
    print(x)
"""