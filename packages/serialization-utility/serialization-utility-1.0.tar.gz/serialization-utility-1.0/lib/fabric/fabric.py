from lib.parsers.json_parser import JsonSerializer
from lib.parsers.toml_parser import TomlSerializer
from lib.parsers.yaml_parser import YamlSerializer
from lib.constants import serializer_types


class SerializerFabric:
    @staticmethod
    def create_serializer(serializer_type: str):
        serializer_type = serializer_type.strip().lower()

        if serializer_type == serializer_types.JSON:
            return JsonSerializer()

        if serializer_type == serializer_types.YAML:
            return YamlSerializer()

        if serializer_type == serializer_types.TOML:
            return TomlSerializer()

        raise ValueError(f"Format {serializer_type} is not supported")
