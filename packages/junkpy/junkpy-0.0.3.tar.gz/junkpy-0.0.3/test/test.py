#!/usr/bin/env python3

from junkpy import Junkpy, JunkpyDataClass
from junkpy.extensions import *


FILE = "testfile.junk"
#FILE = "ext_test.junk"


class CustomClass:
	def __init__(self, value):
		self.a = value
		self.b = value * 2
		self.c = value / 2
		
	def __repr__(self):
		return f"CustomClass({self.a}, {self.b}, {self.c})"
		
		

class CustomDataClass(JunkpyDataClass):
	CLASS = CustomClass
	KEYWORD = "custom"
	
	@classmethod
	def load(cls, value, **kwargs):
		obj = super().load(value, **kwargs)
		obj.a *= kwargs.get("test1", 1)
		obj.b *= kwargs.get("test2", 1)
		obj.c *= kwargs.get("test3", 1)
		return obj


junk = Junkpy([
	CustomDataClass,
	JunkpyMassDataClass,
	JunkpyDistanceDataClass
])

loaded_data = junk.load_file(FILE)

print(loaded_data)

