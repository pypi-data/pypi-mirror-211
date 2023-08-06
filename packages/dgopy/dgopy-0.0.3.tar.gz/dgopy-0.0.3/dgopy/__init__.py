import sys
import json
import os

class DGOImpl:
    def __init__(self) -> None:
        self.INPUT = {}
        self.ENV = {}
        self.CONFIG = {}
        self.__original_stdout = None

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

    def setPrintUtf8(self):
        if self.__original_stdout is None:
            self.__original_stdout = sys.stdout
            sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf8')

    def unsetPrintUtf8(self):
        if not(self.__original_stdout is None):
            sys.stdout = self.__original_stdout
            self.__original_stdout = None

dgo = DGOImpl()