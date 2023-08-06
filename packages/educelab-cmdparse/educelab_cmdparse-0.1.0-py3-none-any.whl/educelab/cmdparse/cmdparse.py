import itertools
from typing import List


def parse(cmd_list: List[str], namespace):
    commands = []
    for cmd_str in cmd_list:
        key, sep, val = cmd_str.lstrip('-').partition("=")
        try:
            kwargs = getattr(namespace, key)(sep, val)
        except AttributeError as e:
            raise ValueError(f'No parser for command: \'{cmd_str}\'') from e
        commands.append((key, kwargs))
    return commands


def parse_parameter_list(param_str, keys: List[str], types, sep=',',
                         num_required=None, mode='*'):
    if num_required is None and mode == '+':
        raise ValueError(
            'Specified nargs_mode \'+\' but nargs_required not provided')

    if num_required is not None and num_required > len(keys):
        raise ValueError(
            'nargs_required is larger than number of parseable parameters')

    # container for parsed params
    params = {}
    if len(param_str) == 0:
        if mode == '+':
            raise ValueError(
                f'Too few arguments: expected {num_required}, got 0')
        return params

    # split on separators
    vals = param_str.split(sep)

    # too many parameters
    if len(vals) > len(keys):
        raise ValueError(
            f'Too many arguments: expected at most {len(keys)}, got {len(vals)}')

    # too few parameters
    if len(vals) and num_required is not None and len(vals) < num_required:
        raise ValueError(
            f'Too few arguments: expected {num_required}, got {len(vals)}')

    # parse each parameter
    for key, type_fn, val in itertools.zip_longest(keys, types, vals):
        if val is not None and len(val):
            params[key] = type_fn(val)
    return params
