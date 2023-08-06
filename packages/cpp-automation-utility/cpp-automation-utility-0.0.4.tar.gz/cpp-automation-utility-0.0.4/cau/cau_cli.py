"""
C++ Automation Utility (CAU)
"""
import logging
import pathlib
import sys

import click

import cau

cau_cli = click.Group()

sys.tracebacklimit = 1

logger = logging.getLogger("CAU")

restore_help = "Skip restoration of Conan sources"
build_directory_help = "Build directory of project"
build_type_help = "Build type (Debug|Release)"
platform_help = "Build platform (linux|win64)"

@cau_cli.command(help="Restores conan dependencies")
@click.option("-b", "--build-directory", default="build", help=build_directory_help)
@click.option("-t", "--build-type", default="Debug", help=build_type_help)
@click.option("-p", "--platform", default="linux", help=platform_help)
@cau.timer
def restore(build_directory: str, build_type: str, platform: str):
    """
    Restores conan dependencies
    """
    conan = cau.Conan(build_directory=build_directory, build_type=build_type, platform=platform)
    result = conan.restore()
    sys.exit(result.returncode)

@cau_cli.command(help="Runs clang-tidy to lint C++ source files.")
@click.option("-s", "--skip-restore", is_flag=True, default=False, help=restore_help)
@click.option("-b", "--build-directory", default="build", help=build_directory_help)
@cau.timer
def lint(skip_restore: bool, build_directory: str):
    """
    Lint command creates a lint object and calls the lint object
    """
    if not skip_restore:
        conan = cau.Conan(build_directory=build_directory)
        _ = conan.restore()

    logger.debug("Interrogating git for changed files")
    git = cau.Git()
    changes = git.changed_files()

    logger.debug("Performing lint operation")
    linter = cau.Tidy(touched_files=changes, compile_database_dir=build_directory)
    result = linter.lint()
    sys.exit(0 if result else 1)

@cau_cli.command(help="Build project via conan")
@click.option("-s", "--skip-restore", is_flag=True, default=False, help=restore_help)
@click.option("-b", "--build-directory", default="build", help=build_directory_help)
@click.option("-t", "--build-type", default="Debug", help=build_type_help)
@click.option("-p", "--platform", default="linux", help=platform_help)
@cau.timer
def build(skip_restore: bool, build_directory: str, build_type: str, platform: str):
    """
    Build command build the project via conan
    """
    conan = cau.Conan(build_directory=build_directory, build_type=build_type, platform=platform)
    if not skip_restore:
        conan.restore()
    result = conan.build()
    sys.exit(result.returncode)

@cau_cli.command(help="Cleans project build files")
@click.option("-b", "--build-directory", default="build", help=build_directory_help)
@click.option("-a", "--all-files", is_flag=True, default=False, help="Cleans build directory and conan directory")
@click.option("--only-build", is_flag=True, default=False, help="Only delete build directory")
@click.option("--only-conan", is_flag=True, default=False, help="Removes conan dependencies")
@cau.timer
def clean(build_directory: str, all_files: bool, only_build: bool, only_conan: bool):
    """
    Clean project of build files
    """
    conan = cau.Conan(build_directory=build_directory)
    if all_files:
        result = all(method() for method in (conan.clean_build, conan.clean_conan))
    elif only_build:
        result = conan.clean_build()
    elif only_conan:
        result = conan.clean_conan()
    else:
        sys.exit(0)
    sys.exit(0 if result else 1)

@cau_cli.command(help="Runs test executable and then collects coverage information")
@click.option("-p", "--project", required=True, type=str, help="Project name, will run test executable Test<Project>")
@click.option("-b", "--build-directory", default=pathlib.Path.cwd()/"build", help=build_directory_help)
@cau.timer
def coverage(project: str, build_directory: str):
    """
    Generates coverage information from project test executable.
    """
    coverage_wrapper = cau.Coverage(project, build_directory=build_directory)
    result = coverage_wrapper.run()
    sys.exit(result.returncode)

if __name__ == "__main__":
    cau_cli()
