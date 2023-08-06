from __future__ import annotations

import unittest
from unittest.mock import Mock, seal

from dataclasses import dataclass, field
from typing import Optional, Union

from dataclass_as_data import as_data, as_dict, as_tuple, from_data, from_dict, from_tuple, DataAsTuple


## Dataclasses for basic testing
@dataclass
class TestDataclassSimple:
    number: int


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
class RecursiveTestDataclassTuple(RecursiveTestDataclass, DataAsTuple):
    pass


@dataclass
class RecursiveTestDataClassWithContainers:
    numbers: list[int]
    objects: dict[str, TestDataclass]
    extra_objects: list[TestDataclassTuple] = field(default_factory=lambda: [TestDataclassTuple(2)])
    default_objects: tuple[TestDataclassTuple, ...] = (TestDataclassTuple(3), TestDataclassTuple(4))
    union_parameter: Union[int, str] = "pony"
    tuple_of_union: tuple[Union[int, str], ...] = (1, "pony", 2)
    tuple_of_dataclasses: tuple[Union[TestDataclass, RecursiveTestDataclass], ...] = (TestDataclass(0), RecursiveTestDataclass(1))


@dataclass
class TestDataclassWithStrictTuple:
    strict_tuple: tuple[int, str, TestDataclass]


@dataclass
class TestDataclassWithOptionalParameters:
    number: int
    size: Optional[int]
    colour: Optional[str] = None


@dataclass
class TestDataclassWithUnionParameter:
    number: int
    size: Union[int, tuple[int, int]]


converter = Mock()

@dataclass
class TestDataclassWithCustomConverter:
    convert: converter


@dataclass
class TestDataclassWithDataclassList:
    dataclass_list: list[TestDataclassSimple]


@dataclass
class TestDataclassWithUnionStartingWithStr:
    options: Union[str, int]


class LowerStr(str):
    def as_data(self):
        return self.lower()

    @classmethod
    def from_data(cls, data: str):
        return cls(data.lower())

@dataclass
class TestDataclassWithCustomClass:
    name: LowerStr


## Dataclasses for class polymorphism testing
@dataclass
class ContainerDataclass:
    dataclass: BaseDataclass


@dataclass
class BaseDataclass:
    first_name: str
    last_name: str


@dataclass
class SubDataclassA(BaseDataclass):
    pass


@dataclass
class SubDataclassB(BaseDataclass):
    favourite_number: int


@dataclass
class SubDataclassAsTuple(BaseDataclass, DataAsTuple):
    pass


@dataclass
class BaseDataclassWithDefault:
    id: int = 100


@dataclass
class SubDataclassAWithDefault(BaseDataclassWithDefault):
    pass


@dataclass
class SubDataclassBWithDefault(BaseDataclassWithDefault):
    max_value: int = 1_000


@dataclass
class SubDataclassWithDefaultAsTuple(BaseDataclassWithDefault, DataAsTuple):
    pass


@dataclass
class ContainerClassWithDefault:
    dataclass: BaseDataclassWithDefault = BaseDataclassWithDefault()


@dataclass
class ContainerClassWithUnionWithBaseClass:
    dataclass: Union[BaseDataclass, str]


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
        obj = RecursiveTestDataclassTuple(6)

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

    def test_as_data_with_optional_parameters(self):
        # Test 1
        obj = TestDataclassWithOptionalParameters(159, 21)

        data = as_data(obj)

        self.assertEqual(data, {
            'number': 159,
            'size': 21,
            'colour': None,
        })

        # Test 2
        obj = TestDataclassWithOptionalParameters(159, None, "red")

        data = as_data(obj)

        self.assertEqual(data, {
            'number': 159,
            'size': None,
            'colour': "red",
        })

    def test_as_tuple_with_optional_parameters(self):
        # Test 1
        obj = TestDataclassWithOptionalParameters(159, 21)

        data = as_tuple(obj)

        self.assertEqual(data, (159, 21, None))

        # Test 2
        obj = TestDataclassWithOptionalParameters(159, None, "red")

        data = as_tuple(obj)

        self.assertEqual(data, (159, None, "red"))

    def test_as_data_with_union_parameter(self):
        # Test 1
        obj = TestDataclassWithUnionParameter(789, 13)

        data = as_data(obj)

        self.assertEqual(data, {
            'number': 789,
            'size': 13,
        })

        # Test 2
        obj = TestDataclassWithUnionParameter(789, (3, 3))

        data = as_data(obj)

        self.assertEqual(data, {
            'number': 789,
            'size': (3, 3),
        })

    def test_as_tuple_with_union_parameter(self):
        # Test 1
        obj = TestDataclassWithUnionParameter(789, 13)

        data = as_tuple(obj)

        self.assertEqual(data, (789, 13))

        # Test 2
        obj = TestDataclassWithUnionParameter(789, (3, 3))

        data = as_tuple(obj)

        self.assertEqual(data, (789, (3, 3)))

    ## Tests with class polymorphism
    def test_as_data_with_subclass_member_correctly_adds_type_to_dict(self):
        obj = ContainerDataclass(SubDataclassA("Sigmath", "Bits"))

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': {
                '__type': "SubDataclassA",
                'first_name': "Sigmath",
                'last_name': "Bits",
            }
        })

    def test_as_data_with_subclass_member_as_tuple_correctly_adds_type_to_tuple(self):
        obj = ContainerDataclass(SubDataclassAsTuple("Sigmath", "Bits"))

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': ("Sigmath", "Bits", {'__type': "SubDataclassAsTuple"})
        })

    def test_as_data_with_base_class_member_doesnt_add_type_to_dict(self):
        obj = ContainerDataclass(BaseDataclass("Sigmath", "Bits"))

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': {
                'first_name': "Sigmath",
                'last_name': "Bits",
            }
        })

    def test_as_data_with_subclass_member_with_default_correctly_adds_type_to_dict(self):
        # Test 1
        obj = ContainerClassWithDefault(SubDataclassAWithDefault())

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': {
                '__type': "SubDataclassAWithDefault",
                'id': 100,
            }
        })

        # Test 2
        obj = ContainerClassWithDefault(SubDataclassBWithDefault())

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': {
                '__type': "SubDataclassBWithDefault",
                'id': 100,
                'max_value': 1_000,
            }
        })

    def test_as_data_with_subclass_member_as_tuple_with_default_correctly_adds_type_to_dict(self):
        obj = ContainerClassWithDefault(SubDataclassWithDefaultAsTuple())

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': (100, {'__type': "SubDataclassWithDefaultAsTuple"})
        })

    def test_as_data_with_union_with_subclass_member_correctly_adds_type_to_dict(self):
        obj = ContainerClassWithUnionWithBaseClass(SubDataclassA("Sigmath", "Bits"))

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': {
                '__type': "SubDataclassA",
                'first_name': "Sigmath",
                'last_name': "Bits",
            }
        })

    ## Remaining Tests
    def test_as_data_with_union_with_subclass_passing_non_subclass_member_correctly_doesnt_add_type(self):
        obj = ContainerClassWithUnionWithBaseClass("Sigmath Bits")

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': "Sigmath Bits"
        })

    def test_as_data_with_union_with_subclass_member_as_tuple_correctly_adds_type_to_dict(self):
        obj = ContainerClassWithUnionWithBaseClass(SubDataclassAsTuple("Rainbow", "Dash"))

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': ("Rainbow", "Dash", {'__type': "SubDataclassAsTuple"})
        })

    def test_as_data_functions_correctly_with_custom_converter(self):
        obj = TestDataclassWithCustomConverter(10)

        data = as_data(obj)

        self.assertDictEqual(data, {
            'convert': 10,
        })

    def test_as_data_with_dataclass_list_correctly_doesnt_add_type_to_dict(self):
        obj = TestDataclassWithDataclassList([TestDataclassSimple(6), TestDataclassSimple(7)])

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass_list': [
                {'number': 6},
                {'number': 7}
            ]
        })

    def test_as_data_with_custom_class_defining_as_data(self):
        obj = TestDataclassWithCustomClass(LowerStr("Derpy!"))

        data = as_data(obj)

        self.assertDictEqual(data, {
            'name': "derpy!"
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

    def test_from_tuple_using_from_data(self):
        obj = from_data(TestDataclass, (6, "ponies!", 6.0))

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
        obj = from_data(RecursiveTestDataclassTuple, (
            6, "ponies!", 6.0,
            {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0,
                "WRONG": "OOPS!",
            },
            (1, "ponies!", 6.0)
        ))

        self.assertEqual(obj, RecursiveTestDataclassTuple(6))

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
            'default_objects': ((3, "ponies!", 6.0), (4, "ponies!", 6.0)),
            'optional_parameter': 10_000,
        })

        dict_of_test_dataclasses = {
            'a': TestDataclass(0),
            'b': TestDataclass(1)
        }
        obj = RecursiveTestDataClassWithContainers([1, 2, 3], dict_of_test_dataclasses)

        self.assertEqual(obj_from_data, obj)

    def test_strict_tuple_converted_correctly(self):
        obj = from_data(TestDataclassWithStrictTuple, {
            'strict_tuple': (6, "pony", {'number': 9})
        })

        self.assertEqual(obj, TestDataclassWithStrictTuple((6, "pony", TestDataclass(9))))

    def test_strict_tuple_conversion_raises_type_error_with_incorrect_element_count(self):
        # Test 1
        with self.assertRaises(TypeError):
            _obj = from_data(TestDataclassWithStrictTuple, {
                'strict_tuple': (6, "pony", {'number': 9}, 10)
            })

        # Test 2
        with self.assertRaises(TypeError):
            _obj = from_data(TestDataclassWithStrictTuple, {
                'strict_tuple': (6, "pony")
            })

    def test_from_data_with_optional_parameters(self):
        # Test 1
        obj = from_data(TestDataclassWithOptionalParameters, {
            'number': 354,
            'size': 12,
        })

        self.assertEqual(obj, TestDataclassWithOptionalParameters(354, 12))

        # Test 2
        obj = from_data(TestDataclassWithOptionalParameters, {
            'number': 354,
            'size': None,
        })

        self.assertEqual(obj, TestDataclassWithOptionalParameters(354, None))

        # Test 3
        obj = from_data(TestDataclassWithOptionalParameters, {
            'number': 354,
            'size': None,
            'colour': "red",
        })

        self.assertEqual(obj, TestDataclassWithOptionalParameters(354, None, "red"))

    def test_from_tuple_with_optional_parameters(self):
        obj = from_tuple(TestDataclassWithOptionalParameters, (354, None, "red"))

        self.assertEqual(obj, TestDataclassWithOptionalParameters(354, None, "red"))

    def test_from_data_with_union_parameter(self):
        # Test 1
        obj = from_data(TestDataclassWithUnionParameter, {
            'number': 354,
            'size': 12,
        })

        self.assertEqual(obj, TestDataclassWithUnionParameter(354, 12))

        # Test 2
        obj = from_data(TestDataclassWithUnionParameter, {
            'number': 354,
            'size': (2, 5),
        })

        self.assertEqual(obj, TestDataclassWithUnionParameter(354, (2, 5)))

    def test_from_tuple_with_union_parameter(self):
        obj = from_data(TestDataclassWithUnionParameter, (354, (2, 5)))

        self.assertEqual(obj, TestDataclassWithUnionParameter(354, (2, 5)))

    def test_from_data_with_union_parameter_raises_type_error_if_doesnt_match_any_union_type(self):
        with self.assertRaises(TypeError):
            _obj = from_data(TestDataclassWithUnionParameter, {
                'number': 354,
                'size': "asd",
            })

    def test_from_data_converts_str_to_int_if_possible(self):
        obj = from_data(TestDataclass, {
            'number': "666",
        })

        self.assertEqual(obj, TestDataclass(666))

    def test_from_data_raises_type_error_if_conversion_from_str_to_int_not_possible(self):
        with self.assertRaises(TypeError):
            _obj = from_data(TestDataclass, {
                'number': "pony"
            })

    ## Tests with class polymorphism
    def test_from_data_with_subclass_member_uses_explicit_type(self):
        obj = from_data(ContainerDataclass, {
            'dataclass': {
                '__type': "SubDataclassA",
                'first_name': "Rainbow",
                'last_name': "Dash",
            }
        })

        self.assertEqual(obj, ContainerDataclass(SubDataclassA("Rainbow", "Dash")))

    def test_from_data_with_subclass_member_with_different_parameters_converts_incorrectly_without_explicit_type(self):
        obj = from_data(ContainerDataclass, {
            'dataclass': {
                'first_name': "Rainbow",
                'last_name': "Dash",
                'favourite_number': 6,
            }
        })

        self.assertNotIsInstance(obj.dataclass, SubDataclassB)

    def test_from_data_with_subclass_member_as_tuple_uses_explicit_type(self):
        obj = from_data(ContainerDataclass, {
            'dataclass': ("Rainbow", "Dash", {'__type': "SubDataclassAsTuple"})
        })

        self.assertEqual(obj, ContainerDataclass(SubDataclassAsTuple("Rainbow", "Dash")))

    def test_from_data_with_subclass_member_with_default_uses_explicit_type(self):
        # Test 1
        obj = from_data(ContainerClassWithDefault, {
            'dataclass': {
                '__type': "SubDataclassAWithDefault"
            }
        })

        self.assertEqual(obj, ContainerClassWithDefault(SubDataclassAWithDefault()))

        # Test 2
        obj = from_data(ContainerClassWithDefault, {
            'dataclass': {
                '__type': "SubDataclassBWithDefault"
            }
        })

        self.assertEqual(obj, ContainerClassWithDefault(SubDataclassBWithDefault()))

    def test_from_data_with_subclass_member_as_tuple_with_default_uses_explicit_type(self):
        obj = from_data(ContainerClassWithDefault, {
            'dataclass': ({'__type': "SubDataclassWithDefaultAsTuple"},)
        })

        self.assertEqual(obj, ContainerClassWithDefault(SubDataclassWithDefaultAsTuple()))

    def test_from_data_with_union_with_subclass_member_uses_explicit_type(self):
        obj = from_data(ContainerClassWithUnionWithBaseClass, {
            'dataclass': {
                '__type': "SubDataclassA",
                'first_name': "Rainbow",
                'last_name': "Dash",
            }
        })

        self.assertEqual(obj, ContainerClassWithUnionWithBaseClass(SubDataclassA("Rainbow", "Dash")))

    def test_from_tuple_with_union_with_subclass_member_uses_explicit_type(self):
        obj = from_data(ContainerClassWithUnionWithBaseClass, {
            'dataclass': ("Rainbow", "Dash", {'__type': "SubDataclassA"})
        })

        self.assertEqual(obj, ContainerClassWithUnionWithBaseClass(SubDataclassA("Rainbow", "Dash")))

    ## Remaining Tests
    def test_from_data_with_custom_converter_is_called(self):
        converter.return_value = 10

        # This is only allowed so long as it's the only use of converter, since `converter` is global
        # (The use of local converters is not supported)
        seal(converter)

        obj = from_data(TestDataclassWithCustomConverter, {'convert': "pony"})

        converter.assert_called_once_with("pony")
        self.assertEqual(obj, TestDataclassWithCustomConverter(10))

    def test_from_data_with_union_starting_with_str_converts_other_types_if_possible(self):
        obj = from_data(TestDataclassWithUnionStartingWithStr, {
            'options': 123,
        })

        self.assertEqual(obj, TestDataclassWithUnionStartingWithStr(123))

    def test_from_data_with_union_starting_with_str_converts_to_str_if_only_possibility(self):
        obj = from_data(TestDataclassWithUnionStartingWithStr, {
            'options': None,
        })

        self.assertEqual(obj, TestDataclassWithUnionStartingWithStr("None"))

    def test_from_data_with_custom_class_defining_from_data(self):
        obj = from_data(TestDataclassWithCustomClass, {
            'name': "Pony!"
        })

        self.assertEqual(obj, TestDataclassWithCustomClass(LowerStr("pony!")))


class TestAsDataFromData(unittest.TestCase):
    def test_dataclass_matches_after_as_data_from_data(self):
        # Test 1
        original_obj = TestDataclass(123)

        data = as_data(original_obj)

        obj = from_data(TestDataclass, data)

        self.assertEqual(original_obj, obj)

        # Test 2
        original_obj = TestDataclassTuple(123)

        data = as_data(original_obj)

        obj = from_data(TestDataclassTuple, data)

        self.assertEqual(original_obj, obj)

        # Test 3
        original_obj = TestDataclassWithStrictTuple((1, '2', TestDataclass(3)))

        data = as_data(original_obj)

        obj = from_data(TestDataclassWithStrictTuple, data)

        self.assertEqual(original_obj, obj)

    def test_recursive_dataclass_matches_after_as_data_from_data(self):
        # Test 1
        original_obj = RecursiveTestDataclass(123)

        data = as_data(original_obj)

        obj = from_data(RecursiveTestDataclass, data)

        self.assertEqual(original_obj, obj)

        # Test 2
        original_obj = RecursiveTestDataclassTuple(123)

        data = as_data(original_obj)

        obj = from_data(RecursiveTestDataclassTuple, data)

        self.assertEqual(original_obj, obj)

    def test_dataclass_with_optional_parameters_match_after_as_data_from_data(self):
        # Test 1
        original_obj = TestDataclassWithOptionalParameters(159, 21)

        data = as_data(original_obj)

        obj  = from_data(TestDataclassWithOptionalParameters, data)

        self.assertEqual(original_obj, obj)

        # Test2
        original_obj = TestDataclassWithOptionalParameters(159, None, "red")

        data = as_data(original_obj)

        obj  = from_data(TestDataclassWithOptionalParameters, data)

        self.assertEqual(original_obj, obj)

    def test_dataclass_with_union_parameter_match_after_as_data_from_data(self):
        # Test 1
        original_obj = TestDataclassWithUnionParameter(789, 13)

        data = as_data(original_obj)

        obj  = from_data(TestDataclassWithUnionParameter, data)

        self.assertEqual(original_obj, obj)

        # Test2
        original_obj = TestDataclassWithUnionParameter(789, (3, 3))

        data = as_data(original_obj)

        obj  = from_data(TestDataclassWithUnionParameter, data)

        self.assertEqual(original_obj, obj)

    def test_dataclass_with_subclass_member_matches_after_as_data_from_data(self):
        # Test 1
        original_obj = ContainerDataclass(SubDataclassB("Sigmath", "Bits", 6))

        data = as_data(original_obj)

        obj = from_data(ContainerDataclass, data)

        self.assertEqual(original_obj, obj)

        # Test 2
        original_obj = ContainerDataclass(SubDataclassAsTuple("Rainbow", "Dash"))

        data = as_data(original_obj)

        obj = from_data(ContainerDataclass, data)

        self.assertEqual(original_obj, obj)

    def test_dataclass_with_subclass_member_with_default_matches_after_as_data_from_data(self):
        # Test 1
        original_obj = ContainerClassWithDefault(SubDataclassAWithDefault())

        data = as_data(original_obj)

        obj = from_data(ContainerClassWithDefault, data)

        self.assertEqual(original_obj, obj)

        # Test 2
        original_obj = ContainerClassWithDefault(SubDataclassBWithDefault())

        data = as_data(original_obj)

        obj = from_data(ContainerClassWithDefault, data)

        self.assertEqual(original_obj, obj)

    def test_dataclass_with_union_with_subclass_member_matches_after_as_data_from_data(self):
        # Test 1
        original_obj = ContainerClassWithUnionWithBaseClass(SubDataclassA("Sigmath", "Bits"))

        data = as_data(original_obj)

        obj = from_data(ContainerClassWithUnionWithBaseClass, data)

        self.assertEqual(original_obj, obj)

        # Test 2
        original_obj = ContainerClassWithUnionWithBaseClass(SubDataclassAsTuple("Sigmath", "Bits"))

        data = as_data(original_obj)

        obj = from_data(ContainerClassWithUnionWithBaseClass, data)

        self.assertEqual(original_obj, obj)



if __name__ == '__main__':
    unittest.main()
