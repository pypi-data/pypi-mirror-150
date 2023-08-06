"""Aggregate can be used to buffer bytes, strings, or dictionaries (JSON objects) to a maximum count or total size.

An aggregate can be used to temporarily buffer data (bytes, strings, or dictionaries representing JSON objects) up to a limit, which is either a maximum count of items in the aggregate (e.g., 1000 items) or a maximum size of all items in the aggregate (e.g., 1000 bytes). After setting the maximum count and size, items can be added until the aggregate is full; once full, the items should be retrieved and the aggregate reset for further use.

Typical usage example:
    # create an aggregate with a max_count of 2 items and max_size of 100 bytes
    agg = Aggregate(2, 10*10)

    # add items to the aggregate until it is full (ok == False)
    for x in ["foo","bar","baz"]:
        ok = agg.add(x)
        if not ok:
            # retrieve the items, reset the aggregate, and re-add missed item
            items = agg.items
            agg.reset()
            agg.add(x)

    # retrieve any remaining items
    if agg.count > 0:
        items = agg.items
"""

import json


class Aggregate(object):
    """Aggregates bytes, strings, or dictionaries (JSON objects).

    Args:
      max_count: Maximum number of items in the aggregate.
      max_size: Maximum size of all items in the aggregate.

    Raises:
      ValueError: If invalid data is added to the aggregate.
    """

    def __init__(self, max_count, max_size):
        self.max_count = max_count
        self.max_size = max_size
        self.count = 0
        self.size = 0
        self.items = []

    def reset(self):
        self.count = 0
        self.size = 0
        self.items = []

    def add(self, data) -> bool:
        if not isinstance(data, (str, bytes, dict)):
            raise ValueError(f"added invalid data type: {type(data)}")

        new_count = self.count + 1
        if new_count > self.max_count:
            return False

        length = 0
        if isinstance(data, dict):
            length = len(json.dumps(data))
        else:
            length = len(data)

        new_size = self.size + length
        if new_size > self.max_size:
            return False

        self.items.append(data)
        self.count = new_count
        self.size = new_size

        return True
