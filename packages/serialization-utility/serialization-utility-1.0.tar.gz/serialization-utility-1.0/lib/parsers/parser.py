class Serializer:
    def dumps(self, item) -> str:
        pass

    def loads(self, string):
        pass

    def dump(self, item, filename):
        with open(filename, 'w') as file:
            file.write(self.dumps(item))

    def load(self, filename):
        with open(filename, 'r') as file:
            return self.loads(file.read())
