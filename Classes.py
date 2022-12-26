from datetime import datetime 
 
class Inner(object):
    def __init__(self) -> None:
        self.List = ['One', 2, 'Three']  
        self.Dic = { 'key': 'value', 'key2': False, 'key3': 456.78 }      

class Outer(object):
    def __init__(self) -> None:
        self.String = 'Python'         
        self.Integer = 1234
        self.Decimal = 123.45
        self.Boolean = True
        self.DateTime = datetime.now()     
        self.Inner = Inner()
 
