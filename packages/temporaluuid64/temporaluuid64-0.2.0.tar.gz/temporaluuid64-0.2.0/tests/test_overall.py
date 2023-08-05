from datetime import datetime
from functools import reduce
import random
import time

import uuid64


def test_basic():
    """Makes sure UUIDs are issued in a chronological sequence."""
    uuids = []
    for _ in range(25):
        uuid = uuid64.issue()
        uuids.append(uuid)
        time.sleep(random.random() * 0.1)

    res = map(lambda x, y: x < y, uuids[:-1], uuids[1:])
    assert reduce(lambda x, y: x and y, res)


def test_uuid64_fields():
    current_time = datetime.utcnow()
    uuid = uuid64.issue(current_time=current_time)
    timestamp, node_id = uuid64.uuid64_fields(uuid)
    assert abs(current_time.timestamp() - timestamp) < 0.01
    assert 0 <= node_id <= 0xFFFF
