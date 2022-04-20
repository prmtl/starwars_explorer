import pytest


def test_that_tests_are_working():
    assert 1 == 1


@pytest.mark.xfail()
def test_that_test_are_failing_as_expected():
    assert 1 == 0
