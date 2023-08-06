"""

Meritous Example: Event Model


"""
from meritous import Model
from meritous.properties import UUIDProperty, StrProperty, DateProperty

from datetime import date

class EventModel(Model):

    _schema = {
        "id"          : UUIDProperty(),
        "title"       : StrProperty(),
        "date"        : DateProperty(),
        "description" : StrProperty(),
    }


event = EventModel()
event.title = 'Sample Event'
event.date = date.fromisoformat('2023-01-10')
print(event.id)
print(event.title)
print(event.date)
