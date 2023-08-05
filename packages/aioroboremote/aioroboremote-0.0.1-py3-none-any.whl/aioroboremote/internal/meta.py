import enum
import inspect
import typing

from .convert import convert_parameters


class StrEnum(str, enum.Enum):
    pass


class KeywordAttr(StrEnum):
    name: str = '__ROBOT_KEYWORD_NAME__'
    parameters: str = '__ROBOT_KEYWORD_PARAMETERS__'
    return_type: str = '__ROBOT_KEYWORD_RETURN__'
    tags: str = '__ROBOT_KEYWORD_TAGS__'
    docs: str = '__ROBOT_KEYWORD_DOCS__'


class LibraryAttr(StrEnum):
    name: str = '__ROBOT_LIBRARY_NAME__'
    docs: str = '__ROBOT_LIBRARY_DOCS__'
    info: str = '__ROBOT_LIBRARY_INFO__'
    keywords: str = '__ROBOT_LIBRARY_KEYWORDS__'


class KeywordWrapper(object):
    def __init__(self, obj: typing.Callable):
        self._keyword = obj
        self._signature = inspect.signature(obj)
        self._is_coroutine = inspect.iscoroutinefunction(obj)

    @property
    def method_name(self):
        return getattr(self._keyword, KeywordAttr.name)

    @property
    def parameters(self):
        return getattr(self._keyword, KeywordAttr.parameters)

    @property
    def return_type(self):
        return getattr(self._keyword, KeywordAttr.return_type)

    @property
    def docs(self):
        return getattr(self._keyword, KeywordAttr.docs)

    @property
    def tags(self):
        return getattr(self._keyword, KeywordAttr.tags)

    @property
    def is_coroutine(self):
        return self._is_coroutine

    @property
    def signature(self):
        return self._signature

    @property
    def keyword(self):
        return self._keyword

    def __call__(self, *args, **kwargs):
        return self._keyword(*args, **kwargs)


class RoboLibraryMeta(type):
    def __new__(mcs, class_name, superclasses, attributedict):
        attributedict[LibraryAttr.keywords] = dict()

        for superclass in superclasses:
            attributedict[LibraryAttr.keywords].update(
                getattr(superclass, LibraryAttr.keywords, {}),
            )

        instance = super(RoboLibraryMeta, mcs).__new__(
            mcs, class_name, superclasses, attributedict,
        )

        keywords = getattr(instance, LibraryAttr.keywords, dict())
        library_info = getattr(instance, LibraryAttr.info, dict())

        for name in (name for name, kw in attributedict.items() if hasattr(kw, KeywordAttr.name)):
            # Get the value of the corresponding function
            kw = KeywordWrapper(getattr(instance, name))
            arg_defs, arg_types = convert_parameters(kw.parameters, kw.return_type)

            keywords[kw.method_name] = kw
            library_info[kw.method_name] = {
                'args': arg_defs,
                'types': arg_types,
                'doc': kw.docs,
                'tags': kw.tags,
            }

        if instance.__doc__:
            library_info['__intro__'] = {'doc': instance.__doc__}

        setattr(instance, LibraryAttr.keywords, keywords)
        setattr(instance, LibraryAttr.info, library_info)

        return instance
