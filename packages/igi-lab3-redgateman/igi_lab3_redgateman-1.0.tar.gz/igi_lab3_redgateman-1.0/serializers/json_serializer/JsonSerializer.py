from ..src.serialization import serialize
from ..src.deserialization import deserialize
from .serialization_logic import serialize_to_json
from .serialization_logic import deserialize_json


class JsonSerializer:
    @staticmethod
    def dumps(obj) -> str:
        """
        Function:
        -----------
        Serializes to json string

        Parameters:
        -----------
            - obj: object to serialize

        Returns:
        -----------
            - string
        """
        serialized_obj = serialize(obj)
        return serialize_to_json(serialized_obj).replace('\n', '\\n')

    @staticmethod
    def dump(obj, file) -> None:
        """
        Function:
        -----------
        Serializes and writes to file

        Parameters:
        -----------
            - obj: object to serialize

        Returns:
        -----------
            - None
        """
        file.write(JsonSerializer.dumps(obj))

    @staticmethod
    def loads(obj: str):
        obj = deserialize_json(obj.replace("\\n", "\n"))
        return deserialize(obj)

    @staticmethod
    def load(file):
        return JsonSerializer.loads(file.read())