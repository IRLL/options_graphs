# OptionGraph for explainable hierarchical reinforcement learning
# Copyright (C) 2021 Mathïs FEDERICO <https://www.gnu.org/licenses/>

""" Integration tests for the initial paper examples. """

import pytest
import pytest_check as check

from option_graph.metrics.complexity.histograms import nodes_histograms
from option_graph.metrics.complexity.complexities import learning_complexity
from option_graph import Action, Option, FeatureCondition, OptionGraph

class TestPaperBasicExamples:
    """Basic examples from the initial paper"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """ Initialize variables. """

        class Option0(Option):
            """Option 0"""
            def __init__(self) -> None:
                super().__init__('option 0')
            def build_graph(self) -> OptionGraph:
                graph = OptionGraph(self)
                feature = FeatureCondition('feature 0')
                graph.add_edge(feature, Action(0), index=False)
                graph.add_edge(feature, Action(1), index=True)
                return graph

        class Option1(Option):
            """Option 1"""
            def __init__(self) -> None:
                super().__init__('option 1')
            def build_graph(self) -> OptionGraph:
                graph = OptionGraph(self)
                feature_1 = FeatureCondition('feature 1')
                feature_2 = FeatureCondition('feature 2')
                graph.add_edge(feature_1, Option0(), index=False)
                graph.add_edge(feature_1, feature_2, index=True)
                graph.add_edge(feature_2, Action(0), index=False)
                graph.add_edge(feature_2, Action(2), index=True)
                return graph

        class Option2(Option):
            """Option 2"""
            def __init__(self) -> None:
                super().__init__('option 2')
            def build_graph(self) -> OptionGraph:
                graph = OptionGraph(self)
                feature_3 = FeatureCondition('feature 3')
                feature_4 = FeatureCondition('feature 4')
                feature_5 = FeatureCondition('feature 5')
                graph.add_edge(feature_3, feature_4, index=False)
                graph.add_edge(feature_3, feature_5, index=True)
                graph.add_edge(feature_4, Action(0), index=False)
                graph.add_edge(feature_4, Option1(), index=True)
                graph.add_edge(feature_5, Option1(), index=False)
                graph.add_edge(feature_5, Option0(), index=True)
                return graph

        self.actions = [Action(i) for i in range(3)]
        self.feature_conditions = [FeatureCondition(f"feature {i}") for i in range(6)]
        self.options = [Option0(), Option1(), Option2()]
        self.used_nodes_all = {
            self.options[0]: {
                self.actions[0]: 1,
                self.actions[1]: 1,
                self.options[0]: 1,
                self.feature_conditions[0]: 1,
            },
            self.options[1]: {
                self.actions[0]: 2,
                self.actions[1]: 1,
                self.actions[2]: 1,
                self.options[0]: 1,
                self.options[1]: 1,
                self.feature_conditions[0]: 1,
                self.feature_conditions[1]: 1,
                self.feature_conditions[2]: 1,
            },
            self.options[2]: {
                self.actions[0]: 6,
                self.actions[1]: 3,
                self.actions[2]: 2,
                self.options[0]: 3,
                self.options[1]: 2,
                self.options[2]: 1,
                self.feature_conditions[0]: 3,
                self.feature_conditions[1]: 2,
                self.feature_conditions[2]: 2,
                self.feature_conditions[3]: 1,
                self.feature_conditions[4]: 1,
                self.feature_conditions[5]: 1,
            },
        }

    def test_nodes_histograms(self):
        """should give expected nodes_histograms results. """

        expected_used_nodes_all = {
            self.options[0]: {
                self.actions[0]: 1,
                self.actions[1]: 1,
                self.options[0]: 1,
                self.feature_conditions[0]: 1,
            },
            self.options[1]: {
                self.actions[0]: 2,
                self.actions[1]: 1,
                self.actions[2]: 1,
                self.options[0]: 1,
                self.options[1]: 1,
                self.feature_conditions[0]: 1,
                self.feature_conditions[1]: 1,
                self.feature_conditions[2]: 1,
            },
            self.options[2]: {
                self.actions[0]: 6,
                self.actions[1]: 3,
                self.actions[2]: 2,
                self.options[0]: 3,
                self.options[1]: 2,
                self.options[2]: 1,
                self.feature_conditions[0]: 3,
                self.feature_conditions[1]: 2,
                self.feature_conditions[2]: 2,
                self.feature_conditions[3]: 1,
                self.feature_conditions[4]: 1,
                self.feature_conditions[5]: 1,
            },
        }

        used_nodes_all = nodes_histograms(self.options)
        check.equal(used_nodes_all, expected_used_nodes_all)

    def test_learning_complexity(self):
        """should give expected learning_complexity. """
        expected_learning_complexities = {
            self.options[0]: 3,
            self.options[1]: 7,
            self.options[2]: 11,
        }
        expected_saved_complexities = {
            self.options[0]: 0,
            self.options[1]: 0,
            self.options[2]: 10,
        }

        for option in self.options:
            c_learning, saved_complexity = learning_complexity(option,
                used_nodes_all=self.used_nodes_all)

            print(f"{option}: {c_learning}|{expected_learning_complexities[option]}"
                  f" {saved_complexity}|{expected_saved_complexities[option]}")
            check.equal(c_learning, expected_learning_complexities[option])
            check.equal(saved_complexity, expected_saved_complexities[option])

