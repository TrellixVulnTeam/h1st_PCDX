import __init__
from typing import Dict
from h1st.model.model import Model

class MyModel(Model):
    def process(self, data:dict = None) -> dict:
        return {"key": "value"}

if __name__ == "__main__":
    modeler = MyModel.get_modeler()
    model = modeler.build_model()
    
    modeler.persist_model(model, 'my_model_id', "/Users/khoama/Workspace/Aitomatic")

    result = model.process()
    print(result)

    model = modeler.load_model('my_model_id')

    result = model.process()
    print(result)