import inspect
import sys
import traceback
import typing

import aiohttp.web
import aiohttp_xmlrpc.handler

from aioroboremote.library import RoboLibraryBase
from aioroboremote.internal.interceptor import StreamInterceptor


class KeywordExecutor(object):
    def __init__(self, keyword_name: str, library: RoboLibraryBase):
        self._keyword_name = keyword_name
        self._library = library

    async def __call__(self, *args, **kwargs):
        log_interceptor = StreamInterceptor()
        try:
            keyword = self._library.robot_library_keywords[self._keyword_name]
            ba = keyword.signature.bind(self._library, *args, **kwargs)
            args, kwargs = ba.args, ba.kwargs

            with log_interceptor:
                if keyword.is_coroutine:
                    result = await keyword(*args, **kwargs)
                else:
                    result = keyword(*args, **kwargs)

            return self._make_success_result(result, output=log_interceptor.output)
        except Exception:
            return self._make_error_result(*sys.exc_info(), output=log_interceptor.output)

    def _make_success_result(self, value: typing.Optional[typing.Any] = None, output=None):
        data = {
            'status': 'PASS',
        }

        if value is not None:
            data['return'] = value

        if output:
            data['output'] = output

        return data

    def _make_error_result(self, error_type, error_value, error_traceback=None, output=None):
        name = error_type.__name__
        message = str(error_value)

        if message:
            error_info = f'{name}: {message}'
        else:
            error_info = name

        data = {
            'status': 'FAIL',
            'error': error_info,
        }

        if error_traceback:
            entries = traceback.extract_tb(error_traceback)[1:]
            tb_text = ''.join(traceback.format_list(entries))
            data['traceback'] = f'Traceback (most recent call last):\n{tb_text}'

        if output:
            data['output'] = output

        return data


class XmlRpcView(aiohttp_xmlrpc.handler.XMLRPCView):
    def __init__(self, library: RoboLibraryBase, request: aiohttp.web.Request):
        super().__init__(request)
        self._library = library

    def rpc_get_library_information(self):
        return self._library.robot_library_info

    def rpc_get_keyword_names(self):
        return tuple(self._library.robot_library_keywords.keys())

    def rpc_get_keyword_arguments(self, name: str):
        return self._library.robot_get_keyword_arguments(name)

    def rpc_get_keyword_types(self, name):
        return self._library.robot_get_keyword_types(name)

    def rpc_get_keyword_tags(self, name):
        return self._library.robot_get_keyword_tags(name)

    def rpc_get_keyword_documentation(self, name):
        return self._library.robot_get_keyword_documentation(name)

    async def rpc_run_keyword(self, name: str,
                              args: typing.Sequence[typing.Any],
                              kwargs: typing.Optional[typing.Dict[str, typing.Any]] = None):
        kwargs = kwargs or {}

        executor = KeywordExecutor(name, self._library)
        return await executor(*args, **kwargs)
