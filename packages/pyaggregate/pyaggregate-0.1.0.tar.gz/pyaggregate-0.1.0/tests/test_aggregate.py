import pytest
from aggregate import Aggregate


def test_add_max_count():
    tests = [
        {
            "test": ["foo"],
            "expected": True,
        },
        {
            "test": ["foo", "bar", "baz"],
            "expected": True,
        },
        {
            "test": ["foo", "bar", "baz", "qux", "quux"],
            "expected": False,
        },
    ]

    for x in tests:
        agg = Aggregate(4, 10 * 10)

        ok = None
        for data in x.get("test"):
            ok = agg.add(data)

        assert ok == x.get("expected")


def test_add_max_size():
    tests = [
        {
            "test": ["foo"],
            "expected": True,
        },
        {
            "test": ["foo", "bar", "baz"],
            "expected": True,
        },
        {
            "test": ["foo", "bar", "baz", "qux", "quux"],
            "expected": False,
        },
    ]

    for x in tests:
        agg = Aggregate(10, 15)

        ok = None
        for data in x.get("test"):

            ok = agg.add(data)

        assert ok == x.get("expected")


def test_count():
    tests = [
        {
            "test": ["foo"],
            "expected": 1,
        },
        {
            "test": [b"foo", b"bar", b"baz"],
            "expected": 3,
        },
        {
            "test": [{"foo": "bar"}, {"baz": "qux"}],
            "expected": 2,
        },
    ]

    for x in tests:
        agg = Aggregate(10, 10 * 10)

        for data in x.get("test"):
            agg.add(data)

        assert agg.count == x.get("expected")


def test_size():
    tests = [
        {
            "test": ["foo"],
            "expected": 3,
        },
        {
            "test": ["foo", "bar", "baz"],
            "expected": 9,
        },
        {
            "test": [b"foo", b"bar", b"baz", b"qux", b"quux"],
            "expected": 16,
        },
        {
            "test": [{"foo": "bar", "baz": {"qux": "quux"}}],
            "expected": 38,
        },
    ]

    for x in tests:
        agg = Aggregate(10, 10 * 10)

        for data in x.get("test"):
            agg.add(data)

        assert agg.size == x.get("expected")


def test_get():
    tests = [
        {
            "test": ["foo"],
        },
        {
            "test": [b"foo", b"bar", b"baz"],
        },
        {
            "test": [{"foo": "bar"}, {"baz": "qux"}],
        },
    ]

    for x in tests:
        agg = Aggregate(10, 10 * 10)

        test = x.get("test")
        for data in test:
            agg.add(data)

        for idx, p in enumerate(agg.items):
            assert p == test[idx]


def test_reset():
    tests = [
        {
            "test": ["foo"],
            "expected": 0,
        },
    ]

    for x in tests:
        agg = Aggregate(100, 100 * 100)

        for data in x.get("test"):
            agg.add(data)

        agg.reset()

        assert agg.count == x.get("expected")
        assert agg.size == x.get("expected")


def test_add_invalid():
    tests = [
        {
            "test": [1, 2, 3],
            "expected": True,
        },
    ]

    with pytest.raises(ValueError):
        for x in tests:
            agg = Aggregate(4, 10 * 10)

            for data in x.get("test"):
                ok = agg.add(data)
