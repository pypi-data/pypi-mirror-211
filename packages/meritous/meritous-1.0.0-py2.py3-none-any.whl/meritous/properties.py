
from meritous.core import Property

import uuid
import datetime


class StrProperty(Property):

    def __init__(self, **kwargs):
        super().__init__(str, **kwargs)


class UUIDProperty(StrProperty):

    def __init__(self, required=True):
        default = str(uuid.uuid4())
        super(StrProperty, self).__init__(str, required=required, default=default)

    def validate(self, value):
        if not super(Property, self).validate(value):
            return False
        try:
            uuid_obj = UUID(value, version=version)
        except ValueError:
            return False
        return True


class DateProperty(Property):

    def __init__(self, **kwargs):
        super().__init__(datetime.date, **kwargs)
