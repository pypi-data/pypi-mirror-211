"""
meritous.core
====================================
Meritous provides simple python modules
"""
from .exceptions import PropertyException, SchemaException, ModelException


class Property:
    """
    Property is the core element of a Meritous Model and Schema. Each property represents a data element of the Model and is used to validate it's type and content. In general Property should be subclassed and the `validate` method overloaded.

    Parameters
    ----------
    type
        Valid Python type representing the expected type of this property
    default
        The default value for the property
    required
        Indicates weather this property is a required value
    """
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
        """
        Validate a property against a provided value


        Parameters
        ----------
        value
            Value to be tested against the set Property type
        """
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
    """
    Models are the main data container in Meritous. For each model you will define a Schema that contains a set of properties,

    The general way you will want to use Models is to subclass them and define the schema (as a dictionary of properties). This gives you a reusable, named Model to represent your data structure in your code.

    .. code-block:: python

      from meritous import Model
      from meritous.core import Property

      class MyModel(Model):

        _schema = {
          'property' : Property(str)
        }

    .. note:: In general you wouldn't reference `Property` directly.


    Parameters
    ----------
    _schema
        Optionally specify the schema in the class constructor to creation of Models in-line (see `In-line Models`_)

    """
    _schema = None
    _data = {}

    def __init__(self, _schema=None):
        self._schema = _schema if _schema else self._schema
        if type(self._schema) != dict:
            raise ModelException('Schema definition is not possible to be created for Model {0}'.format(self.__class__.__name__))
        self._schema = Schema(**self._schema)
        self._data = {name: property.default for name, property in  self._schema.items()}

    def marshall(self, store):
        """
            Marshall a model into a different representation (for storage or transport)

            Parameters
            ----------
            store
                The Store object used to marshall the properties of a Model
        """
        return {name: store.marshall(property) for name, property in self._data.items()}

    #def validate(self):
    #    """
    #        Validate the Model properties against the Schema
    #    """
    #    return self._schema.validate()

    def __getattr__(self, name):
        """
            Allows access to a Model's properties as a class attribute

            Parameters
            ----------
            name
                Name of attribute to access
        """
        if name in self._data:
            return self._data[name]

    def __setattr__(self, name, value):
        """
            Allows updating of a Model's properties via class attributes (e.g. Model.property_name = "some value")

            Parameters
            ----------
            name
                Name of attribute to update
            value
                Value to update
        """
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
