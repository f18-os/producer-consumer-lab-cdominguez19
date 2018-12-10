#!/usr/bin/env python3
class Queue:
    def __init__(self, initArray = []):
        self.a = []
        #self.a = [x for x in initArray]
    def put(self, item):
        self.a.append(item)
    def get(self):
        a = self.a
        item = a[0]
        del a[0]
        return item
    def isEmpty():
        return self.a == []
    def __repr__(self):
        return "Q(%s)" % self.a
