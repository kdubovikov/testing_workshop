from ..metrics import insert_metrics, find_metric_by_name, insert_metric_normalized_name, find_and_square_metric

# Mocking in Python is the act of replacing a real object with a fake or mock object.
# Mocking is a powerful technique to isolate code during unit testing.

# Testing data driven applications
# region
# Testing data driven apps can be a challenging task. The code is highly dependent on the
# data, and the data is often stored in a database. This means that in order to test the
# code, we need to have a database with the correct data in it.
# 
# There are a few ways to handle this:

# - Use a test database. This is the most common approach, but it has some drawbacks:
#   - It requires a database to be set up and running
#   - It requires the test database to be populated with the correct data
#   - It requires the test database to be cleaned up after the tests are run

# - Use a mock database. This is a good approach if you don't want to set up a database,
#   but it has some drawbacks:
#   - It requires a mock database to be set up and running. Like in-memory SQLite.
#   - Mock database may not behave exactly like a real database

# - Use a fixture. This approach is very convenient for unit testing because it allows
#   you to inject test data into your tests without having to set up a database or a mock
#   database. It also allows you to test your code without having to worry about the
#   database being in a certain state.
#   There are a few drawbacks to this approach:
#   - Your database connectivity code is not tested and bugs can leak in
#   - Tests are quite fragile. Due to heavy reliance on mocking, schema changes can
#     be left unattended in tests. Mocked return values are also prone to change, but
#     can easily be forgotten to be updated in the test code.
#   To mitigate these drawbacks, it is avised to use static type checker like mypy or pylance.
# endregion

# pytest-mock
# region 
# Is a plugin for pytest that provides a set of fixtures and a mocker
# object that you can use to mock objects.
#
# The mocker object is a thin-wrapper around the patching API provided by the unittest mock
# package. It provides a simple way to create objects that can stand in for other
# objects in your tests.
# This plugin can be installed with pip:
# pip install pytest-mock

# The mocker fixture provides the following methods:
# - mocker.patch: patch an object in the module under test
# - mocker.spy: spy on an object in the module under test
# - mocker.mock: create a mock object
# - mocker.stub: create a stub object
# - mocker.MagicMock: create a mock object with magic methods
# - mocker.call_count: get the number of times a mock object was called
# - mocker.call_args: get the arguments a mock object was called with
# - mocker.call_args_list: get the arguments a mock object was called with, as a list
#endregion

# let's see how we can inject test data with fixtures
#region
def test_fixture(metrics):
    print("Data from fixture:")
    print(metrics)
# endregion

# using fixtures that depend on other fixtures is not a problem
#region
def test_fixture_with_dependency(metrics_with_duplicate):
    print("Data from fixture with dependency:")
    print(metrics_with_duplicate)
#endregion

# we can also use fixtures to inject mocks
#region
def test_insert_with_mocked_session(metrics, mocker):
    # mocker.patch() is used to replace an object in the module 
    # under test with a mock object.
    session_patch = mocker.patch("testing_workshop.metrics.Session")
    insert_metrics(metrics)

    # assert_called_once() is a method on a mock object that verifies
    # that the mock object was called exactly once.
    session_patch.assert_called_once()

    # we can also assert that session add was called
    # with the metrics we passed in
    assert session_patch.return_value.add.call_count == len(metrics)

    # asssert that we have called add on each of the metrics
    for metric in metrics:
        session_patch.return_value.add.assert_any_call(metric)

    # we can also assert that session commit was called
    assert session_patch.return_value.commit.call_count == 1

    # return_value is a property on a mock object that allows us to
    # access the return value of the mock object when it is called as a function.
#endregion

# if you write testable code, you can also easily
# test complex methods that do many things with mocking!
#region
def test_find_and_square_metric(metrics, mocker):
    original_metric_val = metrics[0].value
    # let's mock the find_metric_by_name function
    find_metric_by_name_patch = mocker.patch("testing_workshop.metrics.find_metric_by_name")
    # we will conveniently make it return the first metric from our metrics fixture
    find_metric_by_name_patch.return_value = metrics[0]

    # let's mock the insert_metric_normalized_name function
    insert_metric_normalized_name_patch = mocker.patch("testing_workshop.metrics.insert_metric_normalized_name")

    # now, let's call the method we want to test
    result = find_and_square_metric("metric1")

    # assert that find_metric_by_name was called once
    find_metric_by_name_patch.assert_called_once_with("metric1")

    # assert that insert_metric_normalized_name was called once
    insert_metric_normalized_name_patch.assert_called_once()

    # assert that the metric was squared
    assert result.value == original_metric_val ** 2
#endregion

# PyTest CLI magic
#region
# pytest CLI test runner has a lot of useful flags that can help you:
# - -k EXPRESSION: only run tests that match the given substring expression
# - -s / --capture=no: disable output capture, your print statements will now work
# - --pdb / --pdbcls: start the interactive Python debugger on errors
# - -m MARKEXPR: only run tests that match the given marker expression
# - --lf: only run the tests that failed last time
# - --vv: increase verbosity
#endregion