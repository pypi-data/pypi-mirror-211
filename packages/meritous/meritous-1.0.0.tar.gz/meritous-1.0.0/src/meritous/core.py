
from .exceptions import PropertyException, SchemaException, ModelException


class Property:
    _type = None
    _default = None
    _required = None

    def __init__(self, type, default=None, required=True):
        self._type = type
        self._required = required

        if default and not self.validate(default):
            raise PropertyException("{0} default value has incorrect type {1}".format(self.__class__.__name__,type(default)))

        self._default = default


    def validate(self, value):
        return type(value) == self._type

    @property
    def is_required(self):
        return self._required

    @property
    def default(self):
            return self._default

    @property
    def type(self):
            return self._type

class Schema(dict):

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    #def validate(self):
    #    for property_name, property in self.items():
    #        if not isinstance(property, Property):
    #            raise SchemaException('Property {0} is not an instance of Property class'.format(property_name))
    #        if not property.validate():
    #            raise PropertyException("{0} has value {1} which doesn't match property type {2}".format(property.__class__.__name__, property._value, property._type))


class Model:
    _schema = None
    _data = {}

    def __init__(self, _schema=None):
        self._schema = _schema if _schema else self._schema
        if type(self._schema) != dict:
            raise ModelException('Schema definition is not possible to be created for Model {0}'.format(self.__class__.__name__))
        self._schema = Schema(**self._schema)
        self._data = {name: property.default for name, property in  self._schema.items()}

    def marshall(self, store):
        return {name: store.marshall(property) for name, property in self._data.items()}

    def validate(self):
        return self._schema.validate()

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]

    def __setattr__(self, name, value):
        if name != '_data' and name in self._data:
            print(self._schema[name])
            if not self._schema[name].validate(value):
                raise PropertyException("{0} attempted to set value {1} which doesn't match property type {2}".format(self.__class__.__name__, value, self._type,  self._schema[name]._type))
            self._data[name] = value
        else:
            self.__dict__[name] = value


class Store:

    def save(self, **kwargs):
        pass

    def marshall(self, value):
        return str(value)

    @staticmethod
    def load(self, **kwargs):
        pass
