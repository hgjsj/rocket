import json
import yaql
class Parser(object):
    def __init__(self, file_path):
        self.file = file_path

class JsonParser(Parser):
    def __init__(self, file_path):
        super(JsonParser, self).__init__(file_path)
        with open(file_path) as f:
            self.data_source = json.loads(f.read())
            #self.data_source.

        self.engine = yaql.factory.YaqlFactory().create()
    
    def evaluate(self, query):
        return self.engine(query).evaluate(data=self.data_source)


if __name__ == "__main__":

    print(2*2)
    #print(JsonParser("data.json").evaluate("$.services"))
    