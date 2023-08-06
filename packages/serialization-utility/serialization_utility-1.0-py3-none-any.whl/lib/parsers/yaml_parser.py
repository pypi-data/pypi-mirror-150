import yaml

from lib.parsers.parser import Serializer
import lib.util.serializer_core as core
from yaml import load, dump


class YamlSerializer(Serializer):
    def dumps(self, item):
        return dump(core.serialize(item))

    def loads(self, string):
        return core.deserialize(load(string, Loader=yaml.Loader))
