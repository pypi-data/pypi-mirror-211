from __future__ import annotations

from collections.abc import Callable, MutableMapping
from hmac import new as hmac_new
from json import dumps as json_dumps
from typing import Any, Union

from mypy_extensions import trait


JSON_VALUE_TYPE = Union[str, int, float, bool, None]


@trait
class StringUtils:
    """
    A collection of methods for strings composition.
    """
    @staticmethod
    def simple_list(raw_list: list[Any]) -> str:
        """
        ['a', 'b'] => "['a', 'b']"
        Parameters
        ----------
        raw_list : list
            Any list.
        Returns
        -------
        result : str
            A string looking like a normal Python list with square brackets.
        """
        string_values = map(lambda x: f"'{x}'", raw_list)
        string_list = ', '.join(string_values)
        return f'[{string_list}]'

    @staticmethod
    def flatten_list(
        raw_list: list[Any],
        parent_key: str = ''
    ) -> dict[str, Any]:
        """
        ['a', ['b', 'c']] => {'[0]': 'a', '[1][0]': 'b', '[1][1]': 'c'}
        """
        items: list[tuple[str, Any]] = []
        for key, value in enumerate(raw_list):
            new_key = f'{parent_key}[{key}]' if parent_key else f'[{key}]'
            if isinstance(value, MutableMapping):
                items.extend(StringUtils.flatten_dict(value, new_key).items())
            elif isinstance(value, list):
                items.extend(StringUtils.flatten_list(value, new_key).items())
            else:
                items.append((new_key, value))
        return dict(items)

    @staticmethod
    def flatten_dict(
        dictionary: MutableMapping[str, Any],
        parent_key: str = ''
    ) -> dict[str, Any]:
        """
        {'a': 1, 'b': {'c': 2}} => {'[a]': 1, '[b][c]': 2}
        """
        items: list[tuple[str, Any]] = []
        for key, value in dictionary.items():
            new_key = f'{parent_key}[{key}]' if parent_key else f'[{key}]'
            if isinstance(value, MutableMapping):
                items.extend(StringUtils.flatten_dict(value, new_key).items())
            elif isinstance(value, list):
                items.extend(StringUtils.flatten_list(value, new_key).items())
            else:
                items.append((new_key, value))
        return dict(items)

    @staticmethod
    def str_from_list(items: list[Any]) -> str:
        """
        ['a', {'b': 'c'}] => "['a', 'b=c']"
        """
        strings: list[str] = []
        for value in items:
            if isinstance(value, MutableMapping):
                value = StringUtils.str_from_dict(value)
            elif isinstance(value, list):
                value = StringUtils.str_from_list(value)
            else:
                value = str(value)
            strings.append(value)
        return StringUtils.simple_list(strings)

    @staticmethod
    def str_from_dict(dictionary: MutableMapping[str, Any]) -> str:
        """
        {'key1': value1, 'key2': value2} => 'key1=value1&key2=value2'
        """
        strings: list[str] = []
        for key, value in dictionary.items():
            if isinstance(value, MutableMapping):
                value = StringUtils.str_from_dict(value)
            elif isinstance(value, list):
                value = StringUtils.simple_list(value)
            else:
                value = str(value)
            strings.append(f'{key}={value}')
        return '&'.join(sorted(strings))

    @staticmethod
    def stringify(items: list[Any]) -> str:
        return json_dumps(items, separators=(',', ':'))

    @staticmethod
    def sign(
        key: str,
        message: str = '',
        algorithm_name: str = 'sha256'
    ) -> str:
        """
        Signing a message with a key.

        Parameters
        ----------
        key : str
            A private key.
        message : str, optional
            A message to be sign, by default ''.
        algorithm_name : str, optional
            The name of an algorithm for signing, by default sha256.

        Returns
        -------
        str
            Signed message.
        """
        return hmac_new(
            key.encode(), message.encode(), digestmod=algorithm_name
        ).hexdigest()

    @staticmethod
    def apply_to_json(
        function: Callable[[str | int], JSON_VALUE_TYPE],
        source: MutableMapping[str, Any] | list[Any]
    ) -> dict[str, Any] | list[Any]:
        """
        Recursively appling a function to a JSON.

        Parameters
        ----------
        function : Callable[[str  |  int], JSON_VALUE_TYPE]
            A function to be applied.
        source : MutableMapping[str, Any]  |  list[Any]
            A JSON for the function to be applied to.

        Returns
        -------
        dict[str, Any]  |  list[Any]
            A JSON with the function applied to each element.
        """
        if isinstance(source, MutableMapping):
            return StringUtils.apply_to_dict(function, source)
        if isinstance(source, list):
            return StringUtils.apply_to_list(function, source)
        raise TypeError('Source must be a dict or a list.')

    @staticmethod
    def apply_to_list(
        function: Callable[[str | int], JSON_VALUE_TYPE],
        items: list[Any]
    ) -> list[Any]:
        """
        Recursively appling a function to a list.

        Parameters
        ----------
        function : Callable[[str  |  int], JSON_VALUE_TYPE]
            A function to be applied.
        items : list[Any]
            A list for the function to be applied to.

        Returns
        -------
        list[Any]
            A list with the function applied to each element.
        """
        new_items: list[Any] = []
        for value in items:
            if isinstance(value, MutableMapping):
                value = StringUtils.apply_to_dict(function, value)
            elif isinstance(value, list):
                value = StringUtils.apply_to_list(function, value)
            else:
                value = function(value)
            new_items.append(value)
        return new_items

    @staticmethod
    def apply_to_dict(
        function: Callable[[str | int], JSON_VALUE_TYPE],
        items: MutableMapping[str, Any]
    ) -> dict[str, Any]:
        """
        Recursively appling a function to a dict.

        Parameters
        ----------
        function : Callable[[str  |  int], JSON_VALUE_TYPE]
            A function to be applied.
        items : MutableMapping[str, Any]
            A dict for the function to be applied to.

        Returns
        -------
        dict[str, Any]
            A dict with the function applied to each element.
        """
        new_items: dict[str, Any] = {}
        for key, value in items.items():
            if isinstance(value, MutableMapping):
                value = StringUtils.apply_to_dict(function, value)
            elif isinstance(value, list):
                value = StringUtils.apply_to_list(function, value)
            else:
                value = function(value)
            new_items[key] = value
        return new_items
