import json
from datetime import datetime 

class WithDate(object):
    def __init__(self) -> None:
        self.DT = datetime.now()

D = WithDate()
JsonText = json.dumps(D)
print(JsonText)

# -----------------------------------------------
import json
from datetime import datetime 

JsonText = """{ "Language": "Python", "Cool": true }""" 
Result = json.loads(JsonText)
print(type(Result)) # prints <class 'dict'>

# -----------------------------------------------

from datetime import date
from datetime import datetime
from dateutil import parser  

class MyClass(object):
    def __init__(self) -> None:
        self.String = 'Python'         
        self._DateTime = datetime.now()    

    @property
    def DateTime(self):
        if isinstance(self._DateTime, str):
            self._DateTime = parser.parse(self._DateTime)
        return self._DateTime
    
    @DateTime.setter
    def DateTime(self, v):
        if isinstance(v, str):
            v = parser.parse(v)
        self._DateTime = v

# -----------------------------------------------
from Json import Json
from datetime import timedelta
from Classes import Outer

print('1. ======== Serialize ')
Obj = Outer()
JsonText = Json.Serialize(Obj)
print(JsonText)

print('2. ======== Modify the object and Serialize again ')
Obj.String += ' is cool'
Obj.Integer -= 500
Obj.Decimal *= 20
Obj.Boolean = False
Obj.DateTime += timedelta(weeks=2)

JsonText2 = Json.Serialize(Obj)
print(JsonText2)

print('3. ======== Deserialize using the first JSON text (populate properties of an existing object) ')
Obj = Json.Deserialize(JsonText, Obj)
JsonText3 = Json.Serialize(Obj)
print(JsonText3)

print('4. ======== Deserialize using the first JSON text (create new object using a class) ')
Obj = Json.Deserialize(JsonText, Outer)
JsonText = Json.Serialize(Obj)
print(JsonText)