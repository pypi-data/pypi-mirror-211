![Codecov](https://img.shields.io/codecov/c/github/errant/meritous?style=for-the-badge)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/errant/meritous?style=for-the-badge)

# Meritous


Meritous is an absurdly simply approach to "Models" in Python.

It came about because there is no modern, framework agnostic approach to modelling data.

On the face of it the usage is very trivial; but the intent is that Meritous is a building block for more complex data models. Essentially, it provides a simple Model class which can contain data to be used in Python applications. It then sets out a standard practice for transforming that data for storage or transport.

```python
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
```
