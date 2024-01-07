import sys

class Log:
  """Log class to record log messages
  
  This class provides methods to:
  
  - Initialize a log
  - Add log records 
  - Get log record types
  - Get log records by type
  """

  def __init__(self):
    self.records = []
  
  def add_record(self, record_type : str, message : str):
    if {'type': record_type, 'message': message} not in self.records:
      self.records.append({'type': record_type, 'message': message})

  def get_types(self) -> list[str] :
    return list(set([record['type'] for record in self.records]))
  
  def get_records_by_type(self, record_type: str) -> list[str]:
    return [record['message'] for record in self.records if record['type'] == record_type]



# Utility functions

globalLog = Log()

def log(type, message):
    globalLog.add_record(type, message)

def report(type):
    records = globalLog.get_records_by_type(type)
    return records

import datetime

def print_report(logger : Log = globalLog, file=sys.stdout):
  types = logger.get_types()  
  for t in sorted(types):
    print(f"\n## {t}:\n", file=file)
    for record in logger.get_records_by_type(t):
      print(f'- {record}', file=file)


