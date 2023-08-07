from dataclasses import is_dataclass, fields
from abc import ABC
from contextlib import suppress
import functools

from typing import TypeVar, Union, Type, Callable, Any, get_origin, get_args, get_type_hints


__all__ = (
    'as_data', 'as_dict', 'as_tuple',
    'from_data', 'from_dict', 'from_tuple',

    # Classes
    'DataAsTuple',
)


Data = Union[dict, tuple, list]

T = TypeVar('T')
TT = TypeVar('TT', bound=type)


class DataAsTuple(ABC):
    def as_data(self):
        return as_tuple(self)

    @classmethod
    def from_data(cls, data):
        return from_tuple(cls, data)


def _deep(func: Callable[..., Any]):
    """Makes a single-input function apply deeply to all values in a nested data structure of dicts, tuples, and lists"""
    @functools.wraps(func)
    def wrapper(data: Any, **kwargs):
        if isinstance(data, dict):
            return {key: wrapper(val, **kwargs) for key, val in data.items()}
        if isinstance(data, (tuple, list)):
            return type(data)(wrapper(val, **kwargs) for val in data)
        return func(data, **kwargs)
    return wrapper


def as_data(obj: Any, /) -> Data:
    """
    Transforms the dataclass into a sequential data object (dict or tuple).
    Applies recursively to all parameters that are also dataclasses.
    This behaviour can be overridden by defining an `as_data` method in your dataclass.
    This only supports other dataclasses, primitive types, and primitive containers (dict, list, tuple).
    @param obj: The dataclass object instance
    @return: The dataclass represented as a dict or tuple
    """
    return _as_data(obj)


@_deep
def _as_data(obj: Any, /, *, annotate=False) -> Data:
    """
    @param obj: The dataclass object instance
    @param annotate: Whether to annotate the dataclass type explicitly in the generated data.
    If True, `from_data` will use this when converting back as long as it is a compatible type.
    @return: The dataclass represented as a dict or tuple
    """
    if is_dataclass(obj):
        data = obj.as_data() if hasattr(obj, 'as_data') else as_dict(obj)
    else:
        return obj.as_data() if hasattr(obj, 'as_data') else obj

    if annotate:
        if isinstance(data, dict):
            data['__type'] = type(obj).__name__
        elif isinstance(data, (tuple, list)):
            data = (*data, {'__type': type(obj).__name__})

    return data


def as_dict(data_class_obj: Any, /) -> dict:
    """
    @param data_class_obj: The dataclass object
    @return: The dataclass represented as a dict
    """
    type_hints = get_type_hints(type(data_class_obj))
    return {_field.name: _as_data(obj := getattr(data_class_obj, _field.name),
                                  annotate=not _exactly_matches_type_hint(type_hints[_field.name], obj))
            for _field in fields(data_class_obj) if _field.init}


def as_tuple(data_class_obj: Any, /) -> tuple:
    """
    @param data_class_obj: The dataclass object
    @return: The dataclass represented as a tuple
    """
    type_hints = get_type_hints(type(data_class_obj))
    return tuple(_as_data(obj := getattr(data_class_obj, _field.name),
                          annotate=not _exactly_matches_type_hint(type_hints[_field.name], obj))
                 for _field in fields(data_class_obj) if _field.init)


def from_data(data_class: Type[T], /, data: Data) -> T:
    """
    Constructs the given dataclass using the provided data performing conversions with dataclass type hints.
    This behaviour can be overridden by defining a `from_data` class method in your dataclass.
    This only supports other dataclasses, primitive types, and primitive containers (dict, list, tuple).
    @param data_class: The dataclass to create
    @param data: The data to convert in the form of a dict, tuple, or list
    @return: The dataclass object instance
    """
    return _from_data(data_class, data)


def _from_data(_type: Type[T], /, data: Data) -> T:
    """
    @param _type: The type to create
    @param data: The data to convert in the form of a dict, tuple, or list
    @return: The type instance constructed from the data
    """
    if is_dataclass(_type):
        matching_types = _matching_types(_type)

        # Handle explicit typing
        type_name = data.get('__type') if isinstance(data, dict) else data[-1].get('__type') if isinstance(data[-1], dict) else None
        if type_name is not None:
            if isinstance(data, (tuple, list)):
                data = data[:-1]

            with suppress(StopIteration):
                matching_types = [next(t for t in matching_types if t.__name__ == type_name)]

        exception = None
        for data_class in matching_types:
            try:
                if hasattr(data_class, 'from_data'):
                    return data_class.from_data(data)  # type: ignore [attr-defined]
                elif isinstance(data, dict):
                    return from_dict(data_class, data)
                elif isinstance(data, (list, tuple)):
                    return from_tuple(data_class, tuple(data))
            except (TypeError, ValueError) as e:
                if exception is None:
                    exception = e  # Capture first error

        raise TypeError(f"Cannot convert to dataclass {_type!r} from data {data!r}") from exception


    if (origin := get_origin(_type)) is None or (args := get_args(_type)) is None:
        # Plain type conversion
        matching_types = _matching_types(_type) if isinstance(_type, type) else [_type]
        for a_type in matching_types:
            with suppress(TypeError, ValueError):
                if hasattr(a_type, 'from_data'):
                    return a_type.from_data(data)  # type: ignore [attr-defined]
                else:
                    return a_type(data)  # type: ignore [call-arg]

        raise TypeError(f"Cannot convert to type {_type!r} or any of its subclasses from data {data!r}")


    if origin is list:
        return [_from_data(args[0], value) for value in data]  # type: ignore [return-value]
    elif origin is tuple:
        if len(args) > 1 and args[1] is Ellipsis:
            return tuple(_from_data(args[0], value) for value in data)  # type: ignore [return-value]

        if len(args) != len(data):
            raise TypeError(f"Incorrect number of elements to convert to type {_type!r} from data {data!r}")

        return tuple(_from_data(arg, value) for arg, value in zip(args, data))  # type: ignore [return-value]
    elif origin is dict and isinstance(data, dict):
        return {_from_data(args[0], key): _from_data(args[1], value) for key, value in data.items()}  # type: ignore [return-value]
    elif origin is Union:
        if type(None) in args and data is None:  # typing.Optional
            return None

        args = args if str not in args else tuple((*(arg for arg in args if arg is not str), str))

        for arg in args:
            with suppress(TypeError):
                return _from_data(arg, data)

        raise TypeError(f"Data didn't match any of the types in {_type!r}: {data!r}")

    raise TypeError(f"Cannot handle conversions to {_type!r}")


def from_dict(data_class: Type[T], _dict: dict, /) -> T:
    """
    @param data_class: The dataclass to create
    @param _dict: The dict representation of the dataclass
    @return: A dataclass instance construction from the dict data
    """
    type_hints = get_type_hints(data_class)
    fields_set = {_field.name for _field in fields(data_class)}
    return data_class(**{name: _from_data(type_hints[name], value) for name, value in _dict.items()
                         if name in fields_set})


def from_tuple(data_class: Type[T], _tuple: tuple, /) -> T:
    """
    @param data_class: The dataclass to create
    @param _tuple: The tuple representation of the dataclass
    @return: A dataclass instance constructed from the tuple data
    """
    type_hints = get_type_hints(data_class)
    return data_class(*(_from_data(type_hints[_field.name], value) for value, _field in zip(_tuple, fields(data_class))))


def _exactly_matches_type_hint(type_hint: type, obj: Any) -> bool:
    """
    Checks if an instance of an object exactly matches a type hint, disallowing matching any subclasses
    Only works for raw types and list, tuple, dict, and Union generics
    @param type_hint: The type hint
    @param obj: The object instance to check
    @return: Whether the object instance matches the type hint exactly
    """
    if (origin := get_origin(type_hint)) is None or (args := get_args(type_hint)) is None:
        return type(obj) is type_hint

    if origin is list:
        return type(obj) is list and all(_exactly_matches_type_hint(args[0], entry) for entry in obj)
    elif origin is tuple:
        if len(args) > 1 and args[1] is Ellipsis:
            return type(obj) is tuple and all(_exactly_matches_type_hint(args[0], entry) for entry in obj)

        return type(obj) is tuple and len(obj) == len(args) \
               and all(_exactly_matches_type_hint(arg, entry) for arg, entry in zip(args, obj))
    elif origin is dict and isinstance(obj, dict):
        return type(obj) is dict and all(_exactly_matches_type_hint(args[0], key) and _exactly_matches_type_hint(args[1], value)
                                         for key, value in obj.items())
    elif origin is Union:
        if type(None) in args and obj is None:  # typing.Optional
            return True

        for arg in args:
            if _exactly_matches_type_hint(arg, obj):
                return True
        else:
            return False

    return False


def _matching_types(_type: TT, /) -> list[TT]:
    """
    Return all types matching `_type`, starting with `_type`, then all its subclasses, then all their subclasses, etc.
    @param _type: The type
    @return: A list of all the types matching `_type`
    """
    if _type in {bool, int, float, complex, str, dict, list, tuple}:  # Primitives are treated purely as-is
        return [_type]

    matching_types = [_type]
    subclasses = _type.__subclasses__()
    while subclasses:
        matching_types.extend(subclasses)
        subclasses = [sub_subclass for subclass in subclasses for sub_subclass in subclass.__subclasses__()]

    return matching_types
