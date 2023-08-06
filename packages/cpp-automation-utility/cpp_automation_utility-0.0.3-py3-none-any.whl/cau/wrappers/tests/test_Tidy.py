"""
Tests for Linters
"""
import pytest

from ..Clang import PathCollection, Tidy
from ..Git import DiffCollection

#pylint: disable=too-few-public-methods
class TestTidy:
    """
    Tests for Tidy
    """
    linter = None

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        Setup of test fixtures
        """
        self.linter = Tidy()

    def test_sources(self, modified: DiffCollection, modified_sources: PathCollection):
        """
        Asserts all source files are found

        Args:
            modified (DiffCollection): collection of touched files

            modified_sources (PathCollection): expected source files
        """
        self.linter = Tidy(modified)
        assert self.linter.sources == modified_sources

    def test_headers(self, modified: DiffCollection, modified_headers: PathCollection):
        """
        Asserts all header files are found

        Args:
            modified (DiffCollection): collection of touched files

            modified_headers (PathCollection): expected source files
        """
        self.linter = Tidy(modified)
        assert self.linter.headers == modified_headers

    def test_headers_clear_of_included_headers(
        self, modified_real_files: DiffCollection, modified_real_headers: PathCollection
    ):
        """
        Asserts that if a source file includes a header, the header is not in the
        header collection

        Args:
            modified_real_files (DiffCollection): modified files on disk

            modified_real_headers (PathCollection): expected headers
        """
        self.linter = Tidy(modified_real_files)
        assert self.linter.headers == modified_real_headers

    @pytest.mark.usefixtures("successful_multiprocess")
    def test_lint_returns_true_if_successful(self, modified: DiffCollection):
        """
        Asserts that True is returned if lint was successful

        Args:
            modified (DiffCollection): modified file list
        """
        self.linter = Tidy(touched_files=modified)
        assert self.linter.lint()

    @pytest.mark.usefixtures("unsuccessful_multiprocess")
    def test_lint_returns_false_if_unsuccessful(self, modified: DiffCollection):
        """
        Asserts that False is returned if lint was not successful

        Args:
            modified (DiffCollection): modified file list
        """
        self.linter = Tidy(touched_files=modified)
        assert not self.linter.lint()
