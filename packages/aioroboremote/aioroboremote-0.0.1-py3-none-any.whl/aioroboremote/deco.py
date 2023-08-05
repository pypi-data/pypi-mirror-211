import inspect
import itertools
import typing

from aioroboremote.internal.meta import KeywordAttr


__slots__ = ['keyword']


def keyword(name=None, tags=()):
    def decorator(func):
        sig = inspect.signature(func)

        method_name = name or func.__name__
        parameters = {}

        # skip `self`
        for param in itertools.islice(sig.parameters.values(), 1, None):
            if param.annotation == 'Any':
                param.replace(annotation=typing.Any)
            parameters[param.name] = param

        return_annotation = sig.return_annotation
        if return_annotation == 'Any':
            return_annotation = typing.Any

        docs = inspect.getdoc(func)

        setattr(func, KeywordAttr.name, method_name)
        setattr(func, KeywordAttr.parameters, parameters)
        setattr(func, KeywordAttr.return_type, return_annotation)
        setattr(func, KeywordAttr.tags, tags)
        setattr(func, KeywordAttr.docs, docs)

        return func

    return decorator
