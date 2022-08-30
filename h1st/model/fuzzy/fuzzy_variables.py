import logging
from typing import Any

import skfuzzy
from skfuzzy import control as skctrl

from h1st.model.fuzzy.enums import FuzzyMembership as fm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FuzzyVariables:
    def __init__(self) -> None:
        self.vars = {}

    def add(
        self, var_name: str, var_type: str, var_range: list, membership_funcs: list
    ) -> None:
        """
        Add a fuzzy variable with their type and membership functions.

        :param range_: the range of variable
        :param name: the name of variable
        :param membership_funcs: this is the list of tuple(membership_func_name, membership_func_type, membership_func_range)
            There are four different kinds of membership_func_type that are supported and their membership_func_range should follow the following formats.
            GAUSSIAN: [mean, sigma]
            SIGMOID: [offset, width]
            TRIANGLE: [a, b, c] where a <= b <= c
            TRAPEZOID: [a, b, c, d] where a <= b <= c <= d
        :param type_: the varilable type should be either consequent or antecedent

        .. code-block:: python
            :caption: example
            vars = FuzzyVariables()
            vars.add(
                var_name='var1',
                var_type='antecedent',
                var_range=np.arange(0, 15+1e-5, 0.5),
                membership_funcs=[('normal', fm.GAUSSIAN, [3, 3.3]),
                                  ('abnormal', fm.TRIANGLE, [8, 15, 15])]
            )
        """
        # Check variable type.
        if var_type == "antecedent":
            fuzzy_var = skctrl.Antecedent(var_range, var_name)
        elif var_type == "consequent":
            fuzzy_var = skctrl.Consequent(var_range, var_name)
        else:
            logger.error(f"{var_type} is not supported type")
            raise ValueError(f"{var_type} is not supported type")

        # Add membership function and its values.
        for mem_func_name, mem_func_type, mem_func_vals in membership_funcs:
            if mem_func_type == fm.TRIANGLE:
                if len(mem_func_vals) != 3:
                    raise ValueError(
                        (
                            f"TRIANGLE membership function needs 3 "
                            f"values. Provided {len(mem_func_vals)} values."
                        )
                    )
                fuzzy_var[mem_func_name] = skfuzzy.trimf(
                    fuzzy_var.universe, mem_func_vals
                )
            elif mem_func_type == fm.TRAPEZOID:
                if len(mem_func_vals) != 4:
                    raise ValueError(
                        (
                            f"TRAPEZOID membership function needs 4 "
                            f"values. Provided {len(mem_func_vals)} values."
                        )
                    )
                fuzzy_var[mem_func_name] = skfuzzy.trapmf(
                    fuzzy_var.universe, mem_func_vals
                )
            elif mem_func_type == fm.GAUSSIAN:
                if len(mem_func_vals) != 2:
                    raise ValueError(
                        (
                            f"GAUSSIAN membership function needs 2 "
                            f"values. Provided {len(mem_func_vals)} values."
                        )
                    )
                fuzzy_var[mem_func_name] = skfuzzy.gaussmf(
                    fuzzy_var.universe, mem_func_vals[0], mem_func_vals[1]
                )
            elif mem_func_type == fm.SIGMOID:
                if len(mem_func_vals) != 2:
                    raise ValueError(
                        (
                            f"SIGMOID membership function needs 2 "
                            f"values. Provided {len(mem_func_vals)} values."
                        )
                    )
                fuzzy_var[mem_func_name] = skfuzzy.sigmf(
                    fuzzy_var.universe, mem_func_vals[0], mem_func_vals[1]
                )
            else:
                raise ValueError(f"{mem_func_type} is not supported.")

        self.vars[var_name] = fuzzy_var

    def remove(self, var_name: str) -> None:
        if var_name in self.vars:
            self.vars.pop(var_name)
        else:
            raise KeyError(f"variable name {var_name} does not exist.")

    def get(self, var_name: str) -> Any:
        if var_name in self.vars:
            return self.vars[var_name]
        else:
            raise KeyError('variable name is not existed')

    def visualize(self) -> None:
        print("=== Antecedents & Consequents ===")
        for v in self.vars.values():
            if isinstance(v, skfuzzy.control.Antecedent):
                v.view()
        for v in self.vars.values():
            if isinstance(v, skfuzzy.control.Consequent):
                v.view()
