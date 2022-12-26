# Python Json: Serialize/Deserialize objects and complex objects

Source code can be fount at [Github](https://github.com/tbebekis/Python-Json).

## Introduction
[Json](https://en.wikipedia.org/wiki/JSON) is a language independent way to represent objects as text and reconstruct objects from text. 

Json is a lightweight data interchange text format. Using Json an application may save or load objects to/from a medium such as a file or a database blob field, and event post or get objects to/from a [web service](https://en.wikipedia.org/wiki/Representational_state_transfer).

## Python support for Json

Python [supports Json](https://docs.python.org/3/library/json.html) by providing a set of functions and classes, found in the `json` package. 

- The `dumps()` function serializes an object to a Json formatted string.
- The `loads()` function deserializes a Json string into a Python dictionary.

## Serialization considerations

There are many answers that can be found by searching the internet on "*how to do json serialization in Python*". Most of them suggest the following:

`json.dumps(MyObject, default=lambda o: o.__dict__, indent=4)`

Regarding the `default` parameter the documentation states: "*If specified, default should be a function that gets called for objects that can’t otherwise be serialized. It should return a JSON encodable version of the object or raise a TypeError. If not specified, TypeError is raised.*"

The proposed solution is fine as long as the object being serialized, and any of its inner objects, provide an internal `__dict__`. 

The `date` and `datetime` are types without a `__dict__`. Furthermore the `dumps()` function does **not** handle those two types the way it handles other primitives such as strings and integers.

The following code results in the runtime error: "*Object of type WithDate is not JSON serializable*". That's because the `dumps()` function doesn't know what to do with the `datetime` type.

```
import json
from datetime import datetime 

class WithDate(object):
    def __init__(self) -> None:
        self.DT = datetime.now()

D = WithDate()
JsonText = json.dumps(D)
print(JsonText)
```
## Deserialization considerations

Deserialization is the reverse of serialization, that is converts a Json string into an object. 

The `loads()` function performs the convertion according to this [table](https://docs.python.org/3/library/json.html#json-to-py-table). The table cleary states that a Json object is converted to a Python Dictionary.

Consider the following code.

```
import json
from datetime import datetime 

JsonText = """{ "Language": "Python", "Cool": true }""" 
Result = json.loads(JsonText)
print(type(Result)) # prints <class 'dict'>
```

In most of the cases the requirements in an application is to convert Json text to an instance of a custom class, say `Customer` or `Invoice` or something like that. Not to a Dictionary.

Another serious issue is, again, the `date` and `datetime` values. These, according to Json specification, are serialized to strings. 

Which is ok as long as they deserialized back to `date` and `datetime` values. But that does not happen automatically.

When it comes to deserialization, there is no way to know if the value being deserialized should be converted to `date` or `datetime` value. The only thing that maybe is useful is to examine the format of the string value.


## The source code

Following are the source code files used in this exercise.<!--more-->

### The `Json.py` file

This file contains the `Json`, `JsonEncoder` and `JsonDecoder` classes.

These classes is all that is needed in order to serialize/deserialize Python objects to/from Json string data. And even complex objects too. 

They are described later.

> In case of an import error regarding the `dateutil.parser` use ```pip install python-dateutil```

```
import inspect
import json
from datetime import date
from datetime import datetime
from dateutil import parser

class Json(object):
    """
    WARNING: do NOT use data-classes, i.e. classes marked with the @dataclass attribute.
    User plain classes with an initializer for fields/properties
    """    

    def Serialize(Instance):
        """ Serializes a specified instance and returns the json text formatted """
        return json.dumps(Instance, cls=JsonEncoder, indent=4)   

    def Deserialize(JsonText: str, ClassOrInstance = None):
        """ Deserializes a specified json text.
            If ClassOrInstance is not specified returns the dictionary the json.loads() produces.
            If ClassOrInstance is a class creates an instance of the class and returns that instance.
            If ClassOrInstance is an instance it just populates the fields/properties of the instance.
            NOTE: This function deserializes complex objects too, i.e. objects containing other objects as nested.
            NOTE: Complex object deserializations assumes that 
            1. the specified class provides a default constructor, i.e. without parameters other than the self
            2. any nested object instance is not null (None) after the constructor call.
        """      
 
        Dic = json.loads(JsonText, cls=JsonDecoder) # loads function deserializes into a dictionary

        if ClassOrInstance != None:
            if inspect.isclass(ClassOrInstance):
                ClassOrInstance = ClassOrInstance()
                
            ClassOrInstance.__dict__.update(Dic)
            return ClassOrInstance

        return Dic

class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, '__dict__'):
            return o.__dict__     

        if isinstance(o, (datetime, date)):
            return o.isoformat()           
 
        return super().default(o) 

class JsonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parse_string = JsonDecoder.Parse
        self.scan_once = json.scanner.py_make_scanner(self)     # Use the python version as the C version do not use the new parse_string

    def Parse(s, end, strict=True):
        """ json.JSONDecoder.parse_string() replacement
            adapted from: https://gist.github.com/setaou/ff98e82a9ce68f4c2b8637406b4620d1
            If the specified string looks like a Date or DateTime value (ISO or not)
            converts the string into Date/DateTime and returns the value
            else returns the string as it was.
            NOTE: The json package sends strings only here, not numbers, booleans, etc.
        """
        (s, end) = json.decoder.scanstring(s, end, strict)
        try:        
            s = parser.parse(s, fuzzy=True)     # fuzzy: True means ignore unknown tokens in string
        except:
            pass

        return (s, end) 

class Serializable(object):
    """ To be used as the base class for the top class of a class tree of serializable classes """
    def ToJson(self):
        return Json.Serialize(self)
    def FromJson(self, JsonText: str):
        Json.Deserialize(JsonText, self)        


```

### The `Classes.py` file

Contains two sample classes used in demonstrating Json serialization/deserialization. The `Outer` class is a complex one as one of its properties is an instance of the `Inner` class.

```
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
```

### The `main.py` file

This file is just a sample on how to serialize and deserialize objects of compex classes using the `Json` class of the `Json.py` module.

```
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
```

The following is the output of the above.

```
1. ======== Serialize 
{
    "String": "Python",
    "Integer": 1234,
    "Decimal": 123.45,
    "Boolean": true,
    "DateTime": "2022-12-26T14:11:11.580494",
    "Inner": {
        "List": [
            "One",
            2,
            "Three"
        ],
        "Dic": {
            "key": "value",
            "key2": false,
            "key3": 456.78
        }
    }
}
2. ======== Modify the object and Serialize again
{
    "String": "Python is cool",
    "Integer": 734,
    "Decimal": 2469.0,
    "Boolean": false,
    "DateTime": "2023-01-09T14:11:11.580494",
    "Inner": {
        "List": [
            "One",
            2,
            "Three"
        ],
        "Dic": {
            "key": "value",
            "key2": false,
            "key3": 456.78
        }
    }
}
3. ======== Deserialize using the first JSON text (populate properties of an existing object)
{
    "String": "Python",
    "Integer": 1234,
    "Decimal": 123.45,
    "Boolean": true,
    "DateTime": "2022-12-26T14:11:11.580494",
    "Inner": {
        "List": [
            "One",
            2,
            "Three"
        ],
        "Dic": {
            "key": "value",
            "key2": false,
            "key3": 456.78
        }
    }
}
4. ======== Deserialize using the first JSON text (create new object using a class)
{
    "String": "Python",
    "Integer": 1234,
    "Decimal": 123.45,
    "Boolean": true,
    "DateTime": "2022-12-26T14:11:11.580494",
    "Inner": {
        "List": [
            "One",
            2,
            "Three"
        ],
        "Dic": {
            "key": "value",
            "key2": false,
            "key3": 456.78
        }
    }
}
```

## Discussion

The `Json` class passes a custom [JSONEncoder](https://docs.python.org/3/library/json.html#json.JSONEncoder) when calling the `dumps()` function and a custom [JSONDecoder](https://docs.python.org/3/library/json.html#json.JSONDecoder) when calling the `loads()` function, in the `cls` parameter. 

### Custom Serialization

The custom `JsonEncoder` inherits from the built-in `json.JSONEncoder` and overrides the `default()` method.

About the `default()` method the documentation states: "*Implement this method in a subclass such that it returns a serializable object for o, or calls the base implementation (to raise a TypeError).*".

The `default()` method of the custom `JsonEncoder` returns the internal `__dict__` of the object being serialized, when that object has such an attribute.

When the object being serialized is an instance of the `date` or `datetime` types, it returns a string representation of the value.

Otherwise calls the base implementation.


### Custom Deserialization

The custom `JsonDecoder` inherits from the built-in `json.JSONDecoder` and assings the `parse_string` attribute of the base class with a custom `Parse()` function.

When the passed-in string looks like a Date or DateTime value, ISO or not, the custom `Parse()` function  converts the string into a `date` or `datetime` and returns that value. Else returns the string as it was.

The glitchy point in the above is that the `JsonDecoder` always assume that if the passed-in string looks like a Date or DateTime, then it actually **is** a `date` or `datetime`. Which is not always true.

Furthermore the `Json.Deserialize()` method does a few more things. Its signature is as following:

``` def Deserialize(JsonText: str, ClassOrInstance = None)```

The caller may pass a class or an instance of a class as the argument in the second parameter. 

Passing such an argument is an indication that the caller wishes to use the passed-in Json string to either construct a new instance of the specified class or populate the properties of the specified instance.

When that second parameter is `None` then the `Deserialize()` returns the Python `dict` as it is returned by the `loads()`.

The `Deserialize()` method deserializes **complex objects** too, i.e. objects containing other objects as nested.

 Complex object deserializations assumes that 
 - the specified class provides a default constructor, i.e. without parameters other than the self
 - any nested object instance is not null (None) after the constructor call.


