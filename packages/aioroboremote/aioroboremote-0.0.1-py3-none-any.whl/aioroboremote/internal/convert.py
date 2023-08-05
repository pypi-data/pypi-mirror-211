import inspect
import typing


def convert_parameters(parameters: typing.Dict[str, inspect.Parameter], return_annotation: typing.Optional[type]):
    defs = []
    types = {}

    for name, param in parameters.items():
        if param.default is param.empty:
            defs.append(param.name)
        else:
            # todo: convert custom-type default to RF-compatible value?
            defs.append((param.name, param.default))

        if param.annotation is param.empty:
            continue

        types[param.name] = _get_parameter_type(param.annotation)

    if return_annotation:
        types['return'] = _get_parameter_type(return_annotation)

    # todo: create type converters?
    return defs, types


def _robot_type_repr(p_type):
    if p_type is inspect.Parameter.empty:
        return ''
    if p_type is None or p_type is type(None):
        return 'None'
    if issubclass(p_type, bool):
        return 'bool'
    if issubclass(p_type, int):
        return 'int'
    if issubclass(p_type, float):
        return 'float'
    if issubclass(p_type, str):
        return 'str'
    if issubclass(p_type, bytes):
        return 'bytes'
    if issubclass(p_type, list):
        return 'list'
    if issubclass(p_type, tuple):
        return 'tuple'
    if issubclass(p_type, set):
        return 'set'
    if issubclass(p_type, dict):
        return 'dict'

    raise TypeError(f'unsupported annotation {p_type}')


def _get_parameter_type(p_type: type):
    # check for generic type
    origin = typing.get_origin(p_type)
    if origin is not None:
        # convert supported generics to underlying RF type
        if origin in (typing.List, list):
            return _robot_type_repr(list)
        if origin in (typing.Tuple, typing.NamedTuple, tuple):
            return _robot_type_repr(tuple)
        if origin in (typing.Set, typing.FrozenSet, set):
            return _robot_type_repr(set)
        if origin in (typing.Dict, typing.OrderedDict, typing.TypedDict, dict):
            return _robot_type_repr(dict)

        # other generics are not supported as robotframework does not provide a way to describe them
        raise TypeError(f'unsupported annotation {p_type}')

    return _robot_type_repr(p_type)

