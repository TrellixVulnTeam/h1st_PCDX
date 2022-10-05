from typing import Any, Dict
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from h1st.model.ml_modeler import MLModeler
from h1st.model.oracle.student_models import RandomForestModel, LogisticRegressionModel


class RandomForestModeler(MLModeler):
    '''
    Knowledge Generalization Modeler backed by a RandomForest algorithm.
    '''
    def __init__(self, model_class=None):
        self.stats = {}
        self.model_class = model_class if model_class is not None else RandomForestModel

    def _preprocess(self, data):
        self.stats["scaler"] = StandardScaler()
        return self.stats["scaler"].fit_transform(data)

    def train_base_model(self, prepared_data: Dict[str, Any]) -> Any:
        X = self._preprocess(prepared_data['X'])
        y = prepared_data['y']
        model = RandomForestClassifier(max_depth=20, random_state=1)
        model.fit(X, y)
        return model


class LogisticRegressionModeler(MLModeler):
    '''
    Knowledge Generalization Modeler backed by a Logistic Regression algorithm
    '''
    def __init__(self, model_class=None):
        self.stats = {}
        self.model_class = model_class if model_class is not None else LogisticRegressionModel

    def _preprocess(self, data):
        self.stats["scaler"] = StandardScaler()
        return self.stats["scaler"].fit_transform(data)

    def train_base_model(self, prepared_data: Dict[str, Any]) -> Any:
        X = self._preprocess(prepared_data['X'])
        y = prepared_data['y']
        model = LogisticRegression()
        model.fit(X, y)
        return model
