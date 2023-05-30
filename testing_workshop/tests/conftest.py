import pytest

from ..model import Metric

# Fixtures are a very useful abstraction in pytest, and one of the features that 
# makes it so powerful.
# 
# Fixtures are functions that are run before each test function to which it is applied.
# Fixtures are used to feed some data to the tests such as database connections, URLs 
# to test and some sort of input data.
# Fixtures are defined using a combination of the pytest.fixture decorator, along with
# a function definition.

# Fixture scope determines how often a fixture is invoked. The default scope is function,
# which means that the fixture is invoked once for each test function that uses it.
#
# Other scopes include:
# - module: once per test module
# - class: once per test class
# - session: once per test session

@pytest.fixture(scope="session")
def metrics():
    return [
        Metric(name="foo", value=11),
        Metric(name="bar", value=2),
        Metric(name="baz", value=3),
    ]

@pytest.fixture(scope="session")
def metrics_with_duplicate(metrics):
    return metrics + [Metric(name="foo", value=1)]