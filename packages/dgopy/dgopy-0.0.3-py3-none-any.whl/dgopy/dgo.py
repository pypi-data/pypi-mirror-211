import sys
import json
import os

INPUT = {}
ENV = {}
CONFIG = {}

def startup():    
    s = os.getenv('DGO_DATA_SIZE')
    if s is None or not s.isdigit():
        return
    
    n = int(s)
    if n < 0:
        return
    
    data = json.loads(sys.stdin.read(n))
    if 'INPUT' in data:
        global INPUT
        INPUT = data['INPUT']
    
    if 'ENV' in data:
        global ENV
        ENV = data['ENV']
    
    if 'CONFIG' in data:
        global CONFIG
        CONFIG = data['CONFIG']
    

