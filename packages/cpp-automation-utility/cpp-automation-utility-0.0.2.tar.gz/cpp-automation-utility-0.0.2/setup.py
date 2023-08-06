"""
Setup script for CAU
"""
import os
import pathlib
import setuptools

with open(pathlib.Path(__file__).parent/".gitlab"/"requirements.txt", encoding="utf-8") as req:
    requirements = req.readlines()

with open(pathlib.Path(__file__).parent/"README.md", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="cpp-automation-utility",
    version=os.environ.get("CI_COMMIT_TAG", "0.0.2"),
    author="AldridgeSoftwareDesigns",
    author_email="aldridge.robert.james@gmail.com",
    description="CLI utility to assist C++ in a devops environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/aldridgesoftwaredesigns/cau",
    packages=setuptools.find_packages(),
    py_modules=["cau"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "cau = cau.cau_cli:cau_cli"
        ]
    },
    install_requires=requirements,
    python_requires=">=3.7.0",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ]
)#yapf: disable
