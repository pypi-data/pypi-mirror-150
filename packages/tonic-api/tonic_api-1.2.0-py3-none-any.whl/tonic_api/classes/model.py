class Model:
    def __init__(self, id, model_json):
        self.id = id
        self.name = model_json['name']
        self.query = model_json['query']
        self.parameters = model_json['nnModelConfig']
        self.encodings = model_json['columnEncodings']

    def describe(self):
        print("Model: " + self.name + " [" + self.id + "]")
        print("Query: " + self.query)
        print("Parameters: " + str(self.parameters))
        print("Column Encodings: " + str(self.encodings))
