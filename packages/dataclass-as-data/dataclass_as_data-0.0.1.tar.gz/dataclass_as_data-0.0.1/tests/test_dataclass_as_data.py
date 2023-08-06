from __future__ import annotations

import unittest

from dataclasses import dataclass, field
from typing import Optional, Union

from dataclass_as_data import as_data, as_dict, as_tuple, from_data, from_dict, from_tuple, DataAsTuple


@dataclass
class TestDataclass:
    number: int
    string: str = "ponies!"
    decimal: float = field(default=6.0, repr=False)

    _private: str = field(default="Shhh", repr=False, init=False)

    CONSTANT = "PONY"


@dataclass
class TestDataclassTuple(TestDataclass, DataAsTuple):
    pass


@dataclass
class RecursiveTestDataclass:
    number: int
    string: str = "ponies!"
    decimal: float = field(default=6.0, repr=False)

    test_dataclass: TestDataclass = TestDataclass(0)
    test_dataclass_tuple: TestDataclassTuple = TestDataclassTuple(1)

    _private: str = field(default="Shhh", repr=False, init=False)

    CONSTANT = "PONY"


@dataclass
class RecursiveTestDataclasssTuple(RecursiveTestDataclass, DataAsTuple):
    pass


@dataclass
class RecursiveTestDataClassWithContainers:
    numbers: list[int]
    objects: dict[str, TestDataclass]
    extra_objects: list[TestDataclassTuple] = field(default_factory=lambda: [TestDataclassTuple(2)])
    default_objects: tuple[TestDataclassTuple] = (TestDataclassTuple(3), TestDataclassTuple(4))
    optional_parameter: Optional[int] = None
    union_parameter: Union[int, str] = "pony"
    tuple_of_union: tuple[Union[int, str]] = (1, "pony", 2)
    tuple_of_dataclasses: tuple[Union[TestDataclass, RecursiveTestDataclass]] = (TestDataclass(0), RecursiveTestDataclass(1))


class TestAsData(unittest.TestCase):
    def test_as_data(self):
        obj = TestDataclass(6)

        data = as_data(obj)

        self.assertDictEqual(data, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0
        })

    def test_as_dict(self):
        obj = TestDataclass(6)

        data = as_dict(obj)

        self.assertDictEqual(data, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0
        })

    def test_as_tuple(self):
        obj = TestDataclass(6)

        data = as_tuple(obj)

        self.assertTupleEqual(data, (6, "ponies!", 6.0))

    def test_as_data_tuple_dataclass(self):
        obj = TestDataclassTuple(6)

        data = as_data(obj)

        self.assertTupleEqual(data, (6, "ponies!", 6.0))

    def test_recursive_as_data(self):
        obj = RecursiveTestDataclass(6)

        data = as_data(obj)

        self.assertDictEqual(data, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0,
            'test_dataclass': {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0
            },
            'test_dataclass_tuple': (1, "ponies!", 6.0)
        })

    def test_recursive_as_dict(self):
        obj = RecursiveTestDataclass(6)

        data = as_dict(obj)

        self.assertDictEqual(data, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0,
            'test_dataclass': {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0
            },
            'test_dataclass_tuple': (1, "ponies!", 6.0)
        })

    def test_recursive_as_tuple(self):
        obj = RecursiveTestDataclass(6)

        data = as_tuple(obj)

        self.assertTupleEqual(data, (
            6, "ponies!", 6.0,
            {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0
            },
            (1, "ponies!", 6.0)
        ))

    def test_recursive_as_data_tuple_dataclass(self):
        obj = RecursiveTestDataclasssTuple(6)

        data = as_data(obj)

        self.assertTupleEqual(data, (
            6, "ponies!", 6.0,
            {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0
            },
            (1, "ponies!", 6.0)
        ))

    def test_recursive_as_data_with_containers(self):
        dict_of_test_dataclasses = {
            'a': TestDataclass(0),
            'b': TestDataclass(1)
        }
        obj = RecursiveTestDataClassWithContainers([1, 2, 3], dict_of_test_dataclasses)

        data = as_data(obj)

        self.assertDictEqual(data, {
            'numbers': [1, 2, 3],
            'objects': {
                'a': {
                    'number': 0,
                    'string': "ponies!",
                    'decimal': 6.0
                },
                'b': {
                    'number': 1,
                    'string': "ponies!",
                    'decimal': 6.0
                },
            },
            'extra_objects': [(2, "ponies!", 6.0)],
            'default_objects': ((3, "ponies!", 6.0), (4, "ponies!", 6.0)),
            'optional_parameter': None,
            'union_parameter': "pony",
            'tuple_of_union': (1, "pony", 2),
            'tuple_of_dataclasses':
                ({
                     'number': 0,
                     'string': "ponies!",
                     'decimal': 6.0
                 },
                 {
                     'number': 1,
                     'string': "ponies!",
                     'decimal': 6.0,
                     'test_dataclass': {
                         'number': 0,
                         'string': "ponies!",
                         'decimal': 6.0
                     },
                     'test_dataclass_tuple': (1, "ponies!", 6.0)
                 })
        })


class TestFromData(unittest.TestCase):
    def test_from_data(self):
        obj = from_data(TestDataclass, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0,
            'WRONG': "OOPS"
        })

        self.assertEqual(obj, TestDataclass(6))

    def test_from_dict(self):
        obj = from_dict(TestDataclass, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0,
            'WRONG': "OOPS"
        })

        self.assertEqual(obj, TestDataclass(6))

    def test_from_tuple(self):
        obj = from_tuple(TestDataclass, (6, "ponies!", 6.0))

        self.assertEqual(obj, TestDataclass(6))

    def test_from_data_tuple_dataclass(self):
        obj = from_data(TestDataclassTuple, (6, "ponies!", 6.0))

        self.assertEqual(obj, TestDataclassTuple(6))

    def test_recursive_from_data(self):
        obj = from_data(RecursiveTestDataclass, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0,
            "WRONG": "OOPS!",
            'test_dataclass': {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0,
                "WRONG": "OOPS!",
            },
            'test_dataclass_tuple': (1, "ponies!", 6.0)
        })

        self.assertEqual(obj, RecursiveTestDataclass(6))

    def test_recursive_from_dict(self):
        obj = from_dict(RecursiveTestDataclass, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0,
            "WRONG": "OOPS!",
            'test_dataclass': {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0,
                "WRONG": "OOPS!",
            },
            'test_dataclass_tuple': (1, "ponies!", 6.0)
        })

        self.assertEqual(obj, RecursiveTestDataclass(6))

    def test_recursive_from_tuple(self):
        obj = from_tuple(RecursiveTestDataclass, (
            6, "ponies!", 6.0,
            {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0,
                "WRONG": "OOPS!",
            },
            (1, "ponies!", 6.0)
        ))

        self.assertEqual(obj, RecursiveTestDataclass(6))

    def test_recursive_from_data_tuple_dataclass(self):
        obj = from_data(RecursiveTestDataclasssTuple, (
            6, "ponies!", 6.0,
            {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0,
                "WRONG": "OOPS!",
            },
            (1, "ponies!", 6.0)
        ))

        self.assertEqual(obj, RecursiveTestDataclasssTuple(6))

    def test_recursive_from_data_with_containers(self):
        obj_from_data = from_data(RecursiveTestDataClassWithContainers, {
            'numbers': [1, 2, 3],
            'objects': {
                'a': {
                    'number': 0,
                    'string': "ponies!",
                    'decimal': 6.0
                },
                'b': {
                    'number': 1,
                    'string': "ponies!",
                    'decimal': 6.0
                },
            },
            'extra_objects': [(2, "ponies!", 6.0)],
            'default_objects': ((3, "ponies!", 6.0), (4, "ponies!", 6.0))
        })

        dict_of_test_dataclasses = {
            'a': TestDataclass(0),
            'b': TestDataclass(1)
        }
        obj = RecursiveTestDataClassWithContainers([1, 2, 3], dict_of_test_dataclasses)

        self.assertEqual(obj_from_data, obj)


if __name__ == '__main__':
    unittest.main()
