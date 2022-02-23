from typing import Any, Dict

from .ml_modeler import BaseModelType, MLModeler
from .modelable import MLModelable

from .predictive_model import PredictiveModel


class MLModel(MLModelable, PredictiveModel):
    """
    Base class for H1st Model.

    To create your own Machine Learning model, inherit `MLModel` class and implement `prepare_data`, 
    `train` and `predict` accordingly. Please refer to Tutorial for more details how to create a model.

    The framework allows you to persist and load model to the model repository.
    To persist the model, you can call `persist()`, and then `load_params()` to retrieve the model.
    See `persist()` and `load_params()` document for more detail.

        .. code-block:: python
            :caption: Model Persistence and Loading Example

            import os
            import tempfile
            from typing import Any, Dict

            from h1st.model.ml_model import MLModel
            from h1st.model.ml_modeler import MLModeler
            from sklearn.datasets import load_iris
            from sklearn.model_selection import train_test_split
            from sklearn.ensemble import RandomForestClassifie

            class MyMLModel(MLModel):
                def process(self, input_data: Dict) -> Dict:
            return {'predictions': self.base_model.predict(input_data['X'])}

            class MyMLModeler(MLModeler):
                def __init__(self):
                    self.model_class = MyMLModel

                def train_base_model(self, prepared_data: Dict[str, Any]) -> Any:
                    X, y = prepared_data['X'], prepared_data['y']
                    model = RandomForestClassifier(random_state=0)
                    model.fit(X, y)
                    return model

            X, y = load_iris(return_X_y=True)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
            prepared_data = {'X': X_train, 'y': y_train}
            my_modeler = MyMLModeler()
            my_model = my_modeler.build_model(prepared_data)

            y_pred = my_model.predict({'X': X_test})['predictions']
            accuracy = accuracy_score(y_test, y_pred)
            print("Accuracy (test): %0.1f%% " % (accuracy * 100))

            with tempfile.TemporaryDirectory() as path:
                # Set the model repository to the temporary directory
                os.environ['H1ST_MODEL_REPO_PATH'] = path
                my_model.persist('1st_version')

                # Load the model from the repo
                my_model_2 = MyMLModel()
                my_model_2.load_params('1st_version')
                y_pred = my_model_2.predict({'X': X_test})['predictions']
                accuracy = accuracy_score(y_test, y_pred)
                print("Accuracy (test): %0.1f%% " % (accuracy * 100))
    """

    def __init__(self, base_model: Any = None):
        self.base_model = base_model

    @classmethod
    def get_modeler(cls, base_model: Any = None) -> MLModeler:
        return MLModeler(cls, base_model)

#    def train_base_model(self, prepared_data: Dict[str, Any]) -> Any:
#        self.base_model.fit(prepared_data['features'], prepared_data['label'])
#        return self.base_model

    def predict(self, data: Dict = None) -> Dict:
        base_model_type = self.get_modeler().get_base_model_type(self)

        if base_model_type == BaseModelType.SCIKITLEARN:
            return self.base_model.predict(data['features'])
        
        elif base_model_type == BaseModelType.PYTORCH:
            pass
        
        elif base_model_type == BaseModelType.TENSORFLOW:
            pass

        else:
            pass