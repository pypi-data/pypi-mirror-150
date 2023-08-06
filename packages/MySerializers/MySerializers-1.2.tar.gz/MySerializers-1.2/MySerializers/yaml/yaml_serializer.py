from MySerializers.json import parser
from MySerializers.src import serialize, deserialize


class YamlSerializer:

    @staticmethod
    def dumps(item):
        return str(serialize(item)).replace("\n", "\\n")

    @staticmethod
    def dump(item, file):
        file.write(YamlSerializer.dumps(item))

    @staticmethod
    def loads(item):
        return deserialize(parser.json_parser(item.replace("\\n", "\n")))

    @staticmethod
    def load(file):
        return YamlSerializer.loads(file.read())
