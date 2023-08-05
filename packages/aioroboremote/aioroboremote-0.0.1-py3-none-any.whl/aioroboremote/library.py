import typing

from aioroboremote.internal.meta import KeywordWrapper, LibraryAttr, RoboLibraryMeta


__slots__ = ['RoboLibraryBase']


class RoboLibraryBase(metaclass=RoboLibraryMeta):
    @property
    def robot_library_keywords(self) -> dict[str, KeywordWrapper]:
        return getattr(self, LibraryAttr.keywords)

    @property
    def robot_library_info(self) -> dict[str, typing.Any]:
        return getattr(self, LibraryAttr.info)

    def robot_get_keyword_arguments(self, name: str):
        return self.robot_library_info[name]['args']

    def robot_get_keyword_types(self, name):
        return self.robot_library_info[name]['types']

    def robot_get_keyword_tags(self, name):
        return self.robot_library_info[name]['tags']

    def robot_get_keyword_documentation(self, name):
        return self.robot_library_info[name]['doc']
