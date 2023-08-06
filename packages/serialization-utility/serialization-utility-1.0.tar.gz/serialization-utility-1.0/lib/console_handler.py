import tests.test_data
from lib.fabric.fabric import SerializerFabric


def handle(source_file, source_type, output_file, output_type):
    if source_type == output_type:
        raise ValueError(f"Source type is the same as output type {source_type}, use different types!")

    source_serializer = SerializerFabric.create_serializer(source_type)
    output_serializer = SerializerFabric.create_serializer(output_type)

    source = source_serializer.load(source_file)
    output_serializer.dump(source, output_file)


# source_serializer = SerializerFabric.create_serializer('json')
# # source_serializer.dump(tests.test_data.TestClass, 'resources/entity.json')
# x = source_serializer.load('resources/entity.json')
# print(x({}).inner_func(5))
