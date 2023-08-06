from dataclasses import is_dataclass, fields
import functools
from typing import TypeVar, Union, Type, Callable, Any, get_origin, get_args, get_type_hints


__all__ = (
    'as_data', 'as_dict', 'as_tuple',
    'from_data', 'from_dict', 'from_tuple',

    # Classes
    'DataAsTuple',
)


T = TypeVar('T')
TT = TypeVar('TT', bound=type)


def _deep(func: Callable[..., Any]):
    """Makes a single-input function apply deeply to all values in a nested data structure"""
    @functools.wraps(func)
    def wrapper(data, **kwargs):
        if isinstance(data, dict):
            return {key: wrapper(val, **kwargs) for key, val in data.items()}
        if isinstance(data, list) or isinstance(data, tuple):
            return type(data)(wrapper(val, **kwargs) for val in data)
        return func(data, **kwargs)
    return wrapper


@_deep
def as_data(obj) -> Union[dict, tuple]:
    """Transforms the dataclass into a sequential data object (dict or tuple)
    Applies recursively to all parameters that are also dataclasses
    This behaviour can be overridden by defining a `as_data` method in your dataclass"""
    if hasattr(obj, 'as_data'):
        return obj.as_data()
    if is_dataclass(obj):
        return as_dict(obj)
    else:
        return obj


def as_dict(data_class_obj) -> dict:
    return {_field.name: as_data(getattr(data_class_obj, _field.name)) for _field in fields(data_class_obj) if _field.init}


def as_tuple(data_class_obj) -> tuple:
    return tuple(as_data(getattr(data_class_obj, _field.name)) for _field in fields(data_class_obj) if _field.init)


def from_data(data_class: Type[T], data: Union[dict, tuple, list]) -> T:
    """Constructs the given dataclass using the provided data performing conversions with dataclass type hints
    This behaviour can be overridden by defining a `from_data` method in your dataclass
    This only supports primitive types and containers (dict, list, tuple)"""
    return _from_data(data_class, data)


def _from_data(_type: Type[T], data: Union[dict, tuple, list]) -> T:
    if is_dataclass(_type):
        matching_types =  _matching_types(_type)
        for data_class in matching_types:
            try:
                if hasattr(data_class, 'from_data'):
                    return data_class.from_data(data)  # type: ignore [attr-defined]
                elif isinstance(data, dict):
                    return from_dict(data_class, data)
                elif isinstance(data, (list, tuple)):
                    return from_tuple(data_class, tuple(data))
            except TypeError as e:
                if len(matching_types) == 1:
                    raise TypeError(f"Cannot convert to dataclass {_type!r} from data {data!r}") from e

        raise TypeError(f"Cannot convert to dataclass {_type!r} from data {data!r}")

    if (origin := get_origin(_type)) is None or (args := get_args(_type)) is None:
        for a_type in _matching_types(_type):
            try:
                return a_type(data)  # type: ignore [call-arg]
            except TypeError:
                pass
        raise TypeError(f"Cannot convert to type {_type!r} or any of its subclasses from data {data!r}")

    if origin is list or origin is tuple:
        return _type(_from_data(args[0], value) for value in data)  # type: ignore [call-arg]
    elif origin is dict and isinstance(data, dict):
        return _type({_from_data(args[0], key): _from_data(args[1], value) for key, value in data.items()})  # type: ignore [call-arg]
    elif origin is Union:
        if type(None) in args and data is None:  # typing.Optional
            return None

        for arg in args:
            try:
                return _from_data(arg, data)
            except TypeError:
                pass
        raise TypeError(f"Data didn't match any of the types in {_type!r}: {data!r}")

    raise TypeError(f"Cannot handle conversions to {_type!r}")


def from_dict(data_class: Type[T], _dict: dict) -> T:
    type_hints = get_type_hints(data_class)
    fields_set = {_field.name for _field in fields(data_class)}
    return data_class(**{name: _from_data(type_hints[name], value) for name, value in _dict.items()
                         if name in fields_set})


def from_tuple(data_class: Type[T], _tuple: tuple) -> T:
    type_hints = get_type_hints(data_class)
    return data_class(*(_from_data(type_hints[_field.name], value) for value, _field in zip(_tuple, fields(data_class))))


def _matching_types(_type: TT) -> tuple[TT, ...]:
    if _type in {bool, int, float, str}:
        return _type,

    subclasses = _type.__subclasses__()
    if subclasses:
        return _type, *(a_type for subclass in subclasses for a_type in _matching_types(subclass))
    return _type, *subclasses


class DataAsTuple:
    def as_data(self):
        return as_tuple(self)

    @classmethod
    def from_data(cls, data):
        return from_tuple(cls, data)
