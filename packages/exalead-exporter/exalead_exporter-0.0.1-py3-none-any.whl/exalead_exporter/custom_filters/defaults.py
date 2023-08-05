# -*- coding:utf-8 -*-
#************************************************************************
import sys

# import datetime, dateutil.parser, dateutil.relativedelta
import distutils.util

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
class UpdateFilter(Filter):

   #********************************
   def __init__(self, name):
      self.name = 'update'

   #********************************
   def filter(self, dest_dict, src_dict):

      if isinstance(dest_dict, dict) and isinstance(src_dict, dict):
         dest_dict.update( src_dict )

      return dest_dict

#************************************************************************
class KeysFilter(Filter):

   #********************************
   def __init__(self, name):
      self.name = 'keys'

   #********************************
   def filter(self, dict_obj):

      if isinstance(dict_obj, dict):
         return list( dict_obj.keys() )

      return []

#************************************************************************
class ValuesFilter(Filter):

   #********************************
   def __init__(self, name):
      self.name = 'values'

   #********************************
   def filter(self, dict_obj):

      if isinstance(dict_obj, dict):
         return list( dict_obj.values() )

      return []

#************************************************************************
class SplitFilter(Filter):

   #********************************
   def __init__(self, name):
      self.name = 'split'

   #********************************
   def filter(self, source_str, separator):

      if isinstance(source_str, str) and isinstance(separator, str):
         return list( source_str.split(separator) )

      return []

#************************************************************************
class BoolFilter(Filter):

   #********************************
   def __init__(self, name):
      self.name = 'bool'

   #********************************
   def filter(self, value):
      res = False

      if value is not None:
         if isinstance(value, bool):
            res = value
         elif isinstance(value, str):
            try:
               int_value = distutils.util.strtobool(value)
               if int_value != 0:
                  res = True
            except:
               pass
         elif isinstance(value, int):
            if value != 0:
               res = True
      return res

#************************************************************************
class Bool2intFilter(Filter):

   #********************************
   def __init__(self, name):
      self.name = 'bool2int'

   #********************************
   def filter(self, value):
      res = 0

      if value is not None:
         if isinstance(value, bool):
            res = value
         elif isinstance(value, str):
            try:
               int_value = distutils.util.strtobool(value)
               if int_value != 0:
                  res = 1
            except:
               pass
         elif isinstance(value, int):
            if value != 0:
               res = 1
      return res

#************************************************************************
# over