import sys
import json
import os

class DGOImpl:
    def __init__(self) -> None:
        self.INPUT = {}
        self.ENV = {}
        self.CONFIG = {}

        s = os.getenv('DGO_DATA_SIZE')
        if s is None or not s.isdigit():
            return
        
        n = int(s)
        if n < 0:
            return
        
        data = json.loads(sys.stdin.buffer.read(n))
        if 'INPUT' in data:
            self.INPUT = data['INPUT']
        
        if 'ENV' in data:
            self.ENV = data['ENV']
        
        if 'CONFIG' in data:
            self.CONFIG = data['CONFIG']

dgo = DGOImpl()