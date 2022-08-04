import numpy as np

from h1st.model.fuzzy import FuzzyLogicModeler, FuzzyLogicModel, FuzzyLogicRules


def build_fuzzy_model():
    flr = FuzzyLogicRules()
    flr.add_variable(
        range_=np.arange(0, 10, 0.5),
        name='sensor1',
        membership_funcs=[('normal', flr.GAUSSIAN, [3, 3.3]),
                        ('abnormal', flr.TRIANGLE, [8, 15, 15])],
        type_='antecedent'
    )
    flr.add_variable(
        range_=np.arange(0, 10, 0.5),
        name='sensor2',
        membership_funcs=[('normal', flr.GAUSSIAN, [3, 3.3]),
                        ('abnormal', flr.TRIANGLE, [8, 15, 15])],
        type_='antecedent'
    )
    flr.add_variable(
        range_=np.arange(0, 10, 0.5),
        name='problem1',
        membership_funcs=[('no', flr.TRAPEZOID, [0, 0, 4, 6]),
                        ('yes', flr.TRAPEZOID, [4, 6, 10, 10])],
        type_='consequent'
    )
    flr.add_rule(
        'rule1',
        if_=flr.vars['sensor1']['abnormal'] & flr.vars['sensor2']['abnormal'],
        then_=flr.vars['problem1']['yes'])
    flr.add_rule(
        'rule2',
        if_=flr.vars['sensor1']['normal'],
        then_=flr.vars['problem1']['no'])
    flr.add_rule(
        'rule2',
        if_=flr.vars['sensor2']['normal'],
        then_=flr.vars['problem1']['no'])

    modeler = FuzzyLogicModeler()
    model = modeler.build_model(flr)
    return model

if __name__ == "__main__":
    fuzzy_model = build_fuzzy_model()
    sensor_input = {
            'sensor1': 7,
            'sensor2': 10
        }
    prediction = fuzzy_model.predict(sensor_input)
    print("prediction['problem1']: ", prediction['problem1'])
