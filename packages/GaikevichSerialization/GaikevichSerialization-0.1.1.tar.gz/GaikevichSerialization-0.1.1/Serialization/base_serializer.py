from abc import ABC, abstractmethod


class BaseSerializer(ABC):
    """
    Abstract class that represents parser.
    It can serialize and deserialize objects.
    """

    @abstractmethod
    def dumps(self, obj) -> str:
        """
        Abstract method for serializing object to string
        :param obj: object to serialization
        :return: string representation of object
        """
        pass

    @abstractmethod
    def loads(self, string: str):
        """
        Deserializes string to object

        :param string: source string
        :return: deserialized object
        """
        pass

    def dump(self, obj, source_file):
        """
        Serializes object to chosen format and writes it to file
        :param obj: object to serialization
        :param source_file: file to writing
        """
        source_file.write(self.dumps(obj))

    def load(self, source_file):
        """
        Deserializes file content to object

        :param source_file: source file
        :return: deserialized object
        """
        return self.loads(source_file.read())
