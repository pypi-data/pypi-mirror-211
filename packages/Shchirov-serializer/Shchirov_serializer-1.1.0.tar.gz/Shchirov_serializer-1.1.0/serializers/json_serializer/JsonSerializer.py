# from ..base.serialization import get_serializer_function
# from ..base.deserialization import create_deserializer
# from .serialization_logic import serialize_to_json
# from .serialization_logic import deserialize_json

from typing import Any
from serializers.base.deserialization import Deserializer
from serializers.base.serialization import Serializer
from ..base.constants import (PRIMITIVES,
                         JsonRegularExpression as Expression)
import regex


class _JsonSerializer:
    # @staticmethod
    # def dumps(obj) -> str:
    #     """ 
    #     Function:
    #     -----------
    #     Serializes to json string

    #     Parameters:
    #     -----------
    #         - obj: object to serialize

    #     Returns:
    #     -----------
    #         - string
    #     """
    #     serialized_obj = get_serializer_function(obj)
    #     return serialize_to_json(serialized_obj).replace('\n', '\\n')

    # @staticmethod
    # def dump(obj, file) -> None:
    #     """ 
    #     Function:
    #     -----------
    #     Serializes and writes to file

    #     Parameters:
    #     -----------
    #         - obj: object to serialize

    #     Returns:
    #     -----------
    #         - None
    #     """
    #     file.write(JsonSerializer.dumps(obj))

    # @staticmethod
    # def loads(obj: str):
    #     obj = deserialize_json(obj.replace("\\n", "\n"))
    #     return create_deserializer(obj)

    # @staticmethod
    # def load(file):
    #     return JsonSerializer.loads(file.read())



    def dumps(self, obj: Any) -> str:
        """
        Convert an object to string of 'JSON' format.

        :param obj: Any python object.
        :type obj: Any

        :return: String of 'JSON' format.
        :rtype: str
        """

        packed: dict = Serializer.pack(obj)
        return self._convert(packed)

    def loads(self, string: str):
        """
        Convert string of 'JSON' format to object.

        :param string: String of 'JSON' format.
        :type string: str

        :return: Python object.
        :rtype: Any
        """

        packed: dict = self._deconvert(string)
        return Deserializer.unpack(packed)

    def _convert(self, obj: dict) -> str:
        """
        Convert dictionary that represents object
        to a string of 'JSON' format

        :param obj: Dictionary that represents object.
        :type obj: dict

        :return: String of 'JSON' format.
        :rtype: str
        """

        if isinstance(obj, PRIMITIVES):
            if isinstance(obj, str):
                return '"' + obj.replace("\\", "\\\\").replace('"', "\"").replace("'", "\'") + '"'
            else:
                return str(obj)

        if isinstance(obj, list):
            return '[' + ', '.join([self._convert(item) for item in obj]) + ']'

        if isinstance(obj, dict):
            return '{' + ', '.join([f'{self._convert(key)}: {self._convert(value)}'
                                    for key, value in obj.items()]) + '}'

    def _deconvert(self, string: str) -> dict:
        """
        Convert string of 'JSON' format to
        dictionary that represents object.

        :param string: String of 'JSON' format.
        :type string: str

        :return: Dictionary that represents object.
        :rtype: dict
        """

        string = string.strip()

        if regex.fullmatch(Expression.INT.value, string):
            return int(string)

        if regex.fullmatch(Expression.STR.value, string):
            string = string.replace("\\\\", "\\").replace(r"\"", '"').replace(r"\'", "'")
            return string[1:-1]

        if regex.fullmatch(Expression.FLOAT.value, string):
            return float(string)

        if regex.fullmatch(Expression.BOOL.value, string):
            return True if string == 'True' else False

        if regex.fullmatch(Expression.NONE.value, string):
            return None

        if string.startswith("[") and string.endswith("]"):
            string = string[1:-1]
            matches = regex.findall(Expression.ANY_VALUE.value, string)
            return [self._deconvert(match[0]) for match in matches]

        if string.startswith("{") and string.endswith("}"):
            string = string[1:-1]
            matches = regex.findall(Expression.ANY_VALUE.value, string)
            return {self._deconvert(matches[i][0]): self._deconvert(matches[i + 1][0])
                    for i in range(0, len(matches), 2)}
