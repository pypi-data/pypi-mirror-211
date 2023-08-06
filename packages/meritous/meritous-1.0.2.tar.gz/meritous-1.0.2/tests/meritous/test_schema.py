

import pytest

import test_data as data

from meritous import Schema
from meritous.core import Property
import meritous.exceptions

def test_schema_init():
    s = Schema(**{})


#def test_schema_invalid_property():
#    s = Schema(**{ data.TEST_STR : data.TEST_INT })
#    with pytest.raises(meritous.exceptions.SchemaException):
#        s.validate()


def test_schema_valid_property_invalid_value():
    pass
