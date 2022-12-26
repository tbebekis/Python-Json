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