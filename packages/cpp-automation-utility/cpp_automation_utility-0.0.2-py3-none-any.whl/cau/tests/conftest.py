"""
Test fixtures
"""
import logging

import pytest

import cau

logger = logging.getLogger("CAU")

#pylint: disable=too-few-public-methods
#pylint: disable=missing-class-docstring
#pylint: disable=missing-function-docstring
@pytest.fixture()
def mock_conan(monkeypatch: pytest.MonkeyPatch):
    """
    Mocks Conan wrapper

    Args:
        monkeypatch (pytest.MonkeyPatch): monkeypatch fixture
    """

    class MockProcess:
        returncode: int = 0

    class MockConan:

        def __init__(self, *args, **kwargs) -> None:
            pass

        def restore(self):
            print("Restored Conan")
            return MockProcess()

        def build(self):
            print("Build successful")
            return MockProcess()

        def clean_build(self):
            print("Cleaned out build directory")
            return True

        def clean_conan(self):
            print("Cleaned out conan directory")
            return True

    monkeypatch.setattr(cau, "Conan", lambda *args, **kwargs: MockConan(args, kwargs))

@pytest.fixture()
def mock_git(monkeypatch: pytest.MonkeyPatch):
    """
    Mocked git wrapper

    Args:
        monkeypatch (pytest.MonkeyPatch): monkeypatch fixture
    """

    class MockGit():

        def changed_files(self):
            print("Got changes from git")
            return []

    monkeypatch.setattr(cau, "Git", MockGit)

@pytest.fixture()
def mock_tidy(monkeypatch: pytest.MonkeyPatch):
    """
    Mocked tidy wrapper

    Args:
        monkeypatch (pytest.MonkeyPatch): monkeypatch fixture
    """

    class MockTidy:

        def __init__(self, *args, **kwargs) -> None:
            pass

        def lint(self):
            print("Lint was successful")
            return True

    monkeypatch.setattr(cau, "Tidy", lambda *args, **kwargs: MockTidy(args, kwargs))

@pytest.fixture()
def mock_coverage(monkeypatch: pytest.MonkeyPatch):
    """
    Mocks coverage wrapper

    Args:
        monkeypatch (pytest.MonkeyPatch): monkey patch fixture
    """

    class MockProcess:
        returncode: int = 0

    class MockCoverage:

        def __init__(self, *args, **kwargs) -> None:
            pass

        def run(self):
            print("Running coverage")
            return MockProcess()

    monkeypatch.setattr(cau, "Coverage", MockCoverage)
