from functools import reduce
import operator
import json

# https://stackoverflow.com/a/31033676/11578154
def find(element, json):
    return reduce(operator.getitem, element.split('.'), json)

class JsonObject(object):
    def __init__(self, json_data):
        self.json_data = json_data

    @classmethod
    def from_string(cls, json_string: str):
        return cls(json.loads(json_string))

# modeled after https://stackoverflow.com/a/17330273/11578154
class JsonProperty(object):
    def __init__(self, mapping=None, default=KeyError):
        self.mapping = mapping
        self.default = default

    def __call__(self, wrapped_function):
        self.wrapped_function = wrapped_function

        if "return" in wrapped_function.__annotations__:
            self.return_type = wrapped_function.__annotations__["return"]
        else:
            self.return_type = None

        return self

    def __get__(self, obj: JsonObject, objtype=None):
        if not isinstance(obj, JsonObject):
            raise Exception('No JsonObject')

        try:
            return_value = find(self.mapping, obj.json_data)
        except KeyError as er:
            if self.default is KeyError:
                raise er
            else:
                return self.default

        if self.return_type:
            return_value = (self.return_type)(return_value)

        return return_value

    def __str__(self):
        return f"<JsonProperty | mapping: {self.mapping}>"