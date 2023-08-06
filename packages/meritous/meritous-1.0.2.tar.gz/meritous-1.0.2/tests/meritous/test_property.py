

import pytest

import test_data as data

import meritous.core
import meritous.exceptions

def test_property_basics():
    p = meritous.core.Property(str, data.TEST_STR)
    assert p.default ==  data.TEST_STR
    assert p.type == str
    p.value = data.TEST_STR_ALT
    assert p.value == data.TEST_STR_ALT

def test_property_required():
    p = meritous.core.Property(str)
    assert p.is_required == True
    p = meritous.core.Property(str, required=False)
    assert p.is_required == False

def test_property_init_no_default():
    p = meritous.core.Property(str)
    assert p.default == None

def test_property_init_incorrect_default_type():
    with pytest.raises(meritous.exceptions.PropertyException):
        meritous.core.Property(str, data.TEST_INT)

def test_property_validate():
    p = meritous.core.Property(str, data.TEST_STR)
    assert p.validate(data.TEST_STR_ALT) == True
    assert p.validate(data.TEST_INT) == False
