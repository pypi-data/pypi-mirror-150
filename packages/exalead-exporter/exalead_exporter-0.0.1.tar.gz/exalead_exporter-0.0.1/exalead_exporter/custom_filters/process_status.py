# -*- coding:utf-8 -*-
#************************************************************************
import sys

Filter = None
if 'Filter' in sys.modules:
   Filter = sys.modules['Filter']
elif 'filters' in sys.modules:
   Filter = sys.modules['filters'].Filter
elif 'exalead_exporter.filters' in sys.modules:
   Filter = sys.modules['exalead_exporter.filters'].Filter

if Filter is None:
   raise Exception('Filter module not loaded.')

#************************************************************************
class JobStatusFilter(Filter):

   #********************************
   def filter(self, value):
      if value is None or not isinstance(value, str):
         return value

      if value == "stopped":
         value = 0

      elif value == "started":
         value = 1

      else:
         value = -1

      return value

#************************************************************************
# over