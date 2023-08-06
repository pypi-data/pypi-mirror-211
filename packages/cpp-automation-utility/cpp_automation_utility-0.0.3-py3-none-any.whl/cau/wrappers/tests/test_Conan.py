"""
Tests Conan wrapper class
"""
import os
import pathlib
import shutil
import subprocess

import pytest

from ..Conan import Conan

class TestConan():
    """
    Tests for conan cli wrappers
    """
    conan = None

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        Setup of test fixtures
        """
        self.conan = Conan()

    def test_conan_home_is_set_on_init(self):
        """
        Asserts CONAN_HOME environment variable is properly set on init
        """
        assert os.environ.get("CONAN_HOME") == str(self.conan.home)

    def test_conan_home_is_set_via_setter(self):
        """
        Asserts CONAN_HOME is properly set via setter
        """
        self.conan.home = pathlib.Path("someawkwardpath")
        assert os.environ.get("CONAN_HOME") == str(self.conan.home)

    @pytest.mark.usefixtures("successful_process")
    def test_restore(self):
        """
        Asserts that if the restore was successful, error code of 0 is returned
        """
        result = self.conan.restore()
        assert result.returncode == 0

    @pytest.mark.usefixtures("failed_process")
    def test_restore_raises_exception_if_not_successful(self):
        """
        Asserts that an exception is raised if process call not successful
        """
        with pytest.raises(subprocess.CalledProcessError):
            _ = self.conan.restore()

    def test_profile(self):
        """
        Asserts that the conan profile property is properly constructed
        """
        assert self.conan.profile == "linuxDebug"

    @pytest.mark.usefixtures("successful_process")
    def test_build(self):
        """
        Asserts that if build was successful, error code of 0 is returned
        """
        result = self.conan.build()
        assert result.returncode == 0

    @pytest.mark.usefixtures("failed_process")
    def test_build_raises_exception_if_not_successful(self):
        """
        Asserts that if build failed, an exception is raised
        """
        with pytest.raises(subprocess.CalledProcessError):
            _ = self.conan.build()

    def test_clean_build_is_successful(self, monkeypatch: pytest.MonkeyPatch):
        """
        Asserts true is returned if clean build is successful

        Args:
            monkeypatch (pytest.Monkeypatch): monkeypatch fixture
        """
        monkeypatch.setattr(shutil, "rmtree", lambda *args, **kwargs: None)
        assert self.conan.clean_build()

    def test_clean_build_is_unsuccessful(self, monkeypatch: pytest.MonkeyPatch):
        """
        Asserts False is returned if clean build is unsuccessful

        Args:
            monkeypatch (pytest.MonkeyPatch): _description_
        """

        def _raise(*args, **kwargs):
            raise OSError

        monkeypatch.setattr(shutil, "rmtree", _raise)
        assert not self.conan.clean_build()

    def test_clean_conan_is_successful(self, monkeypatch: pytest.MonkeyPatch):
        """
        Asserts true is returned if clean conan is successful

        Args:
            monkeypatch (pytest.Monkeypatch): monkeypatch fixture
        """
        monkeypatch.setattr(shutil, "rmtree", lambda *args, **kwargs: None)
        assert self.conan.clean_conan()

    def test_clean_conan_is_unsuccessful(self, monkeypatch: pytest.MonkeyPatch):
        """
        Asserts False is returned if clean conan is unsuccessful

        Args:
            monkeypatch (pytest.MonkeyPatch): _description_
        """

        def _raise(*args, **kwargs):
            raise OSError

        monkeypatch.setattr(shutil, "rmtree", _raise)
        assert not self.conan.clean_conan()
