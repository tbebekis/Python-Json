import inspect
import json
from datetime import date
from datetime import datetime
from dateutil import parser

class Json(object):
    """
    WARNING: do NOT use data-classes, i.e. classes marked with the @dataclass attribute.
    Use plain classes with an initializer for fields/properties
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
